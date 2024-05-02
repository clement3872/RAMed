import sys, os
import ramer

def open_file(filename):
    with open(filename, "r") as f:
        l = f.readlines()
    return l

def get_args(line, instr):
    return line[1:].replace(instr,"").replace(")","").split(",")

def get_instruction(line):
    """get instruction from a line"""

    # parse the instruction type
    if line[:4] in ("add(", "sub("):
        instr = line[:3]
        l_args = get_args(line, instr)
        #var1, var2, var3, adr1, adr2, adr3
    elif line[:5] == "mult(":
        instr = line[:4]
        l_args = get_args(line, instr)
    elif line[:5] == "div2(":
        instr = line[:4]
        l_args = get_args(line, instr)
    elif line[:3] in ("je(","jl(","jg("):
        instr = line[:2]
        l_args = get_args(line, instr)
    else: # it's a jump
        instr = "jump("
        l_args = get_args(line, instr)
        instr = ramed.Jump(int(l_args[0]))

    return instr


def open_ram():
    # open file of ram code
    filename = sys.argv[1] if len(sys.argv)>2 else ""
    if os.path.exists(filename) and os.path.isfile(filename):
        content = open_file(filename)
        ram = initialise(content)
    else: 
        # print(f"This is not a proper input.")
        # return 1

        ## This is for tests purpuses
        content = open_file("ram_code/example.ramed")
        inp = ramer.RegisterArray("i",[])

    if len(sys.argv)>2:
        inp = ramer.RegisterArray("i",[int(el) for el in list(sys.argv[2:])])
    inp_s = ramer.RegisterInt("is", inp.size)
    
    for i in range(len(content)):
        content[i] = content[i].replace("\n","").replace("\t","").replace(" ","").lower()

    # first line is (rs,os) - rs = working register size - os = output size
    r_s,out_s = content.pop(0).split(","); r_s = int(r_s); out_s = int(out_s)
    r_s = ramer.RegisterInt("rs",int(r_s)); out_s = ramer.RegisterInt("os",int(out_s))
    r = ramer.RegisterArray("r", [0 for _ in range(r_s.value)])
    o = ramer.RegisterArray("o", [0 for _ in range(out_s.value)])

    # second line are register names
    reg_names = content.pop(0); reg_names = reg_names.split(",")
    registers = [inp, inp_s, r, r_s,o,out_s]
    for el in reg_names: 
        if el in ("i","is","r","rs","o","os"): # forbidden names
            print(f"This register name is forbidden: {el}")

    for el in registers:
        print(el)

    l_instr = []
    for line in content: l_instr.append(get_instruction(line))


if __name__ == "__main__":
    ram = open_ram()
