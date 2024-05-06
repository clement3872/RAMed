import sys, os
from adv_ramer import *


def get_var_name(line, start_index):
    """
    A parsing function
    """
    vname = ""
    for i in range(start_index, len(line)):
        if line[i]=="=": break
        elif line[i]!=" ": vname += line[i]
        i+=1
    return vname

def get_var_data(line):
    i = 5 # 5 <= len(vname)+len(vtype)
    while line[i] != "=":
        i += 1
    while line[i] != " ":
        i += 1
    return line[i:len(line)] # vtype

def find_else_create(ram, vname):
    """
    Creates a new variable if the vname in not None
    """
    if vname is not None:
        v = ram.search_name(vname)
        if v is None:
            if vname[0]=="[" and vname[-1]=="]": 
                v = Variable(name=vname, vtype="list", data=eval(vname))
            elif vname[0]=='"' and vname[-1]=='"': 
                v = Variable(name=vname, vtype="str", data=eval(vname))
            elif "." in vname:
                v = Variable(name=vname, vtype="number", data=float(vname))
            elif vname != "":
                v = Variable(name=vname, vtype="number", data=int(vname))
            ram.add_variable(v)
        return v
    else:
        return None

def get_instruction_args(line, itype, ram):
    # itype means instruction type
    line = line.replace(itype, "").replace("(","").replace(")","").replace(" ","")
    l = line.split(",")
    
    var1,var2,var3, adr1,adr2,adr3 = (None,None,None,None,None,None)

    if itype in ("add", "sub", "mult", "je", "jl", "jg"):
        if "@" in l[0]: 
            var1,adr1 = l[0].split("@")
        else: var1 = l[0]
        if "@" in l[1]: 
            var2,adr2 = l[1].split("@")
        else: var2 = l[1]
        if "@" in l[2]: 
            var3,adr3 = l[2].split("@")
        else: var3 = l[2]
        
    elif itype=="pop":
        var1 = l[0] # Pop takes only 1 argument 
    elif itype=="mov":
        if "@" in l[0]: 
            var1,adr1 = l[0].split("@")
        else: var1 = l[0]
        if "@" in l[1]: 
            var2,adr2 = l[1].split("@")
    elif itype=="push":
        if "@" in l[0]: 
            var1,adr1 = l[0].split("@")
        else: var1 = l[0]
        var2 = l[1]
    elif itype in ("jump", "cout"):
        if "@" in l[0]: 
            var1,adr1 = l[0].split("@")
        else: var1 = l[0]

    l = [var1,var2,var3, adr1,adr2,adr3]
    for i in range(len(l)):
        l[i] = find_else_create(ram, l[i])
    return l

def initialise(content): 
    """
    This function looks like a compiler/interpreter
    """
    # removing anoying characters
    for i in range(len(content)): 
        content[i] = content[i].replace("\n","").strip().lower()
    
    ram = RAM()
    cursor = 0
    # creating variables
    for el in content: # content[0] is the input
        if el[0:5] == "list ": # (yes, we need a space)
            vtype = "list"
            vname = get_var_name(el, 5)
        elif el[0:4] == "str ":
            vtype = "str"
            vname = get_var_name(el, 4)
        elif el[0:4] == "int ":
            vtype = "number"
            vname = get_var_name(el, 4)
        elif el[0:6] == "float ":
            vtype = "number"
            vname = get_var_name(el, 6)
        elif el.strip()=="" or el.strip()[0]=="#":
            vtype = None
        else: break
        
        if vtype is not None:
            vdata = eval(get_var_data(el))
            ram.add_variable(Variable(name=vname, vtype=vtype, data=vdata))
        cursor += 1

    # instructions
    for el in content[cursor:]:
        instruction = None
        # category: mov
        if el.startswith("mov"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"mov",ram)
            instruction = MovInstruction(var1, var2, adr1, adr2)
        
        # category: math
        elif el.startswith("add"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"add",ram)
            instruction = MathOperation("add", var1, var2, var3, adr1, adr2, adr3)
        elif el.startswith("sub"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"sub",ram)
            instruction = MathOperation("sub", var1, var2, var3, adr1, adr2, adr3)
        elif el.startswith("mult"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"mult",ram)
            instruction = MathOperation("mult", var1, var2, var3, adr1, adr2, adr3)

        # category: list
        elif el.startswith("push"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"push",ram)
            instruction = PushList(var1, var2, adr1)
        elif el.startswith("pop"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"pop",ram)
            instruction = PopList(var1)

        # category: jump
        elif el.startswith("jump"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"jump",ram)
            instruction = JumpInstruction(var1, adr1)
        elif el.startswith("je"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"je",ram)
            instruction = JumpCompare("je", var1,var2,var3, adr1,adr2,adr3)
        elif el.startswith("jl"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"jl",ram)
            instruction = JumpCompare("jl", var1,var2,var3, adr1,adr2,adr3)
        elif el.startswith("jg"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"jg",ram)
            instruction = JumpCompare("jg", var1,var2,var3, adr1,adr2,adr3)

        elif el.startswith("cout"):
            var1,var2,var3, adr1,adr2,adr3 = get_instruction_args(el,"cout",ram)
            instruction = OutputDisplay(var1, adr1)
        
        if instruction is None:
            instruction = SkipLine()
        ram.add_instruction(instruction)

    return ram

def open_file(filename):
    with open(filename, "r") as f:
        l = f.readlines()
    return l

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv)==2 else ""
    if os.path.exists(filename) and os.path.isfile(filename):
        content = open_file(filename)
        ram = initialise(content)
    else: 
        #print("This is not a proper file name.")

        ## This is for tests purpuses
        content = open_file("aram_code/example.aramed")
        ram = initialise(content)
        ram.describe()
        ram.run()
        
