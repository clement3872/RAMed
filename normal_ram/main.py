import sys, os

def open_file(filename):
    with open(filename, "r") as f:
        l = f.readlines()
    return l

def open_ram():
    # open file of ram code
    filename = sys.argv[1] if len(sys.argv)>=2 else ""
    if os.path.exists(filename) and os.path.isfile(filename):
        content = open_file(filename)
        ram = initialise(content)
    else: 
        #print(f"This is not a proper file name: {filename}")
        # return 1

        ## This is for tests purpuses
        content = open_file("ram_code/example.ramed")
        input = []

    if len(sys.argv)>2:
        input = list(sys.argv[2:])
    
    for i in range(len(content)):
        content[i] = content[i].replace("\n","").replace("\t","").replace(" ","").lower()

    # first line is (rs,os) - rs = working register size - os = output size
    reg_s,out_s = content.pop(0).split(","); reg_s = int(reg_s); out_s = int(out_s)

    # second line are register names
    reg_names = content.pop(0); reg_names = reg_names.split(",")
    for el in reg_names: 
        if el in ("i","is","r","rs","o","os"): # forbidden names
            print(f"This register name is forbidden: {el}")

    print(reg_s, out_s)
    print(reg_names)
    print(content) # content is now a list of instructions


if __name__ == "__main__":
    open_ram()
