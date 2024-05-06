import sys, os
import ramer

def open_file(filename):
    with open(filename, "r") as f:
        l = f.readlines()
    return l

def get_args(ram, line, instr):
    l_str_args = line.replace(instr,"")[1:].replace(")","").split(",")
    l_args = []

    def is_int(el):
        return el.isdigit() or (el[0]=="-" and el[1:].isdigit())
        
    for arg in l_str_args:
        if is_int(arg):
            l_args.append(int(arg))
            l_args.append(None)
        elif '@' in arg:
            tmp = arg.split("@")

            var = ram.find(tmp[0])
            if var == None:
                assert is_int(tmp[0]), f"In line `{line}`, @ is used incorrectly"
                var = int(tmp[0])

            adr = ram.find(tmp[1])
            if adr == None:
                assert is_int(tmp[1]), f"In line `{line}`, @ is used incorrectly"
                adr = int(tmp[1])

            l_args.append(var)
            l_args.append(adr)
        else:
            tmp = ram.find(arg)
            assert tmp!=None, f"incorrect line: `{line}`"
            l_args.append(tmp)
            l_args.append(None)
    return l_args


def get_instruction(ram, line):
    """get instruction from a line"""

    # parse the instruction type
    if line[:4] in ("add(", "sub("):
        instr = line[:3]
        var1, adr1, var2, adr2, var3, adr3 = get_args(ram, line, instr)
        return ramer.MathOP(var1, var2, var3, adr1, adr2, adr3, instr)
    elif line[:5] == "mult(":
        instr = line[:4]
        var1, adr1, var2, adr2, var3, adr3 = get_args(ram, line, instr)
        return ramer.MathOP(var1, var2, var3, adr1, adr2, adr3, instr)
    elif line[:5] == "div2(":
        instr = line[:4]
        var1, adr1 = get_args(ram, line, instr)
        return ramer.Div2(var1, adr1)
    elif line[:3] in ("je(","jl(","jg("):
        instr = line[:2]
        var1, adr1, var2, adr2, value, _ = get_args(ram, line, instr)
        return ramer.JumpLike(var1, var2, adr1, adr2, value, instr)
    elif line[:5] == "jump(":
        instr = line[:4]
        l_args = get_args(ram, line, instr)
        instr = ramer.Jump(int(l_args[0]))
    else: return None

    return instr


def open_ram(filename="", verbose="0", question=False):
    if not question:
        # open file of ram code
        filename = sys.argv[1] if len(sys.argv)>2 else ""
        verbose = sys.argv[2] if len(sys.argv)>2 and sys.argv[2] in ("0","1") else "0"

    if os.path.exists(filename) and os.path.isfile(filename):
        content = open_file(filename)
    else: 
        # print(f"This is not a proper input.")
        # return 1

        ## This is for tests purpuses
        content = open_file("ram_code/example.ramed")
        inp = ramer.RegisterArray("i",[])

    if len(sys.argv)>2 or question:
        inp = ramer.RegisterArray("i",[int(el) for el in list(sys.argv[3:])])
    inp_s = ramer.RegisterInt("is", inp.size)
    
    for i in range(len(content)):
        content[i] = content[i].replace("\n","").replace("\t","").replace(" ","").lower()

    ## first line is (rs,os) - rs = working register size - os = output size
    ## Do we need this though?
    # r_s,out_s = content.pop(0).split(","); r_s = int(r_s); out_s = int(out_s)
    # r_s = ramer.RegisterInt("rs",int(r_s)); out_s = ramer.RegisterInt("os",int(out_s))
    r = ramer.RegisterArray("r", [])
    o = ramer.RegisterArray("o", [])

    # second line are register names
    reg_names = content.pop(0); reg_names = reg_names.split(",")
    # registers = [inp, inp_s, r, r_s,o,out_s]
    registers = [inp, inp_s, r,o]
    for el in reg_names: 
        if el in ("i","is","r","rs","o","os"): # forbidden names
            print(f"This register name is forbidden: {el}")
        else:
            registers.append(ramer.RegisterInt(el, 0))

    ram = ramer.Ram(registers)

    for i in range(len(content)): 
        ram.append_instruction(get_instruction(ram, content[i]))

    return (verbose=="1", ram)

    ## This is for tests purpuses

    # there is a verbose option:
    # ram.run(True)
    ram.run()

    # This displays the configuration of the RAM
    print(ram)

if __name__ == "__main__":
    # `mode` is the verbose option, displays every steps, but it's annoying
    mode, ram = open_ram()
    print("(RAM at start)", ram)
    ram.run(mode) # `run` also `optimize` (see the function in ramer.py to see why/how)
