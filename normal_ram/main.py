import sys, os
import ramer

def open_file(filename):
    with open(filename, "r") as f:
        l = f.readlines()
    return l

def get_instruction(line):
    """get instruction from a line"""
    # TO DO
    pass

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

    # second line are register names
    reg_names = content.pop(0); reg_names = reg_names.split(",")
    registers = [inp, inp_s, r_s]
    for el in reg_names: 
        if el in ("i","is","r","rs","o","os"): # forbidden names
            print(f"This register name is forbidden: {el}")

    print(inp, "-", inp_s)
    print(r_s, "-", out_s)
    print(reg_names)
    print(content) # content is now a list of instructions

    l_instr = []
    for line in content: l_instr.append(get_instruction(line))


if __name__ == "__main__":
    ram = open_ram()
