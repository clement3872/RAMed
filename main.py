import sys, os
from ramer import *

def initialise(content): 
    """
    This function looks like a compiler/interpreter
    """
    # removing anoying characters
    for i in range(len(content)): 
        content[i] = content[i].replace("\n","").replace(" ","").lower()
    
    ram = RAM()

    ram_input = content[0]
    if ram_input[0]=="[" and ram_input[-1]=="]": 
        ram.add_variable(Variable(name="input", vtype="list", data=eval(ram_input)))
    elif ram_input[0]=='"' and ram_input[-1]=='"': 
        ram.add_variable(Variable(name="input", vtype="str", data=eval(ram_input)))
    elif "." in ram_input:
        ram.add_variable(Variable(name="input", vtype="number", data=float(ram_input)))
    elif ram_input != "":
        ram.add_variable(Variable(name="input", vtype="number", data=int(ram_input)))

    # TODO

def open_file(filename):
    with open(filename, "r") as f:
        l = f.readlines()
    return l

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv)==2 else ""
    if os.path.exists(filename) and os.path.isfile(filename):
        open_file(filename)
    else: 
        #print("This is not a proper file name.")

        ## This is for tests purpuses
        content = open_file("example.ramed")
        initialise(content)