import sys, os

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
        content = open_file("example.ramed")
        print(content)