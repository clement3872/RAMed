

class RAM:
    def __init__(self):
        self.variables = []
        self.instructions = []
        self.index = 0
    
    def search_name(self, name):
        for el in self.variables:
            if el.name == name: return el
        return None
    
    def add_variable(self, var):
        self.variables.append(var)

    def add_instruction(self, action):
        self.instructions.append(action)
    
    def describe(self):
        print("Variable names:")
        for el in self.variables:
            print(el.type, el.name, el.data)
        print("\nInstruction names:")
        for inst in self.instructions:
            print(inst.category)
        print()

class Variable:
    def __init__(self, name, vtype="number", data=0):
        self.name = name
        self.type = vtype
        self.data = data
    
    def get(self, adr=None):
        if self.type == "number" or adr == None: return self.data
        elif self.type == "list" or self.type == "str": return self.data[adr]
    
    def set_data(self, new_value, adr=None):
        """
        It sets a value and returns the new value of the Variable
        """
        if self.type == "number" or adr == None: 
            self.data = new_value
            return self.data
        elif self.type == "list": 
            self.data[adr] = new_value
            return self.data


class PushList:
    def __init__(self, var1, var2, adr1=None):
        # push var1[@adr1] into var2
        assert var1.type != "list", f"{var2.name} should NOT be a list"
        assert var2.type == "list", f"{var2.name} should be a list"
        self.var1 = var1
        self.var2 = var2
        
        self.adr1 = adr1
    
        self.category = "push"
    
    def do(self):
        adr1 = None if self.adr1==None else self.adr1.get()
        self.var2.data.append(self.var1.get(adr1))

class PopList:
    def __init__(self, var1):
        assert var1.type != "list", f"{var2.name} should NOT be a list"
        assert var2.type == "list", f"{var2.name} should be a list"
        self.var1 = var1
    
        self.category = "push"
    
    def do(self):
        self.var1.data.pop()
        

class MovInstruction:
    def __init__(self, var1, var2, adr1=None, adr2=None):
        self.var1 = var1
        self.var2 = var2
        
        self.adr1 = adr1
        self.adr2 = adr2
    
        self.category = "mov"

    def do(self):
        adr1 = None if self.adr1==None else self.adr1.get()
        adr2 = None if self.adr2==None else self.adr2.get()
        
        self.var2.set_data(self.var1.get(adr1), self.adr2)
        return self.var2.data


class MathOperation:
    def __init__(self, operation, var1, var2, var3, adr1=None, adr2=None, adr3=None):
        """
        operation in (add, sub, mult)
        var are a Variables
        adr are addresses (int)
        """
        for (var,adr) in zip([var1,var2,var3], [adr1,adr2,adr3]):
            assert var.type == "number" or var.type == "list", f"{var.name} is not an number or a list"
            assert (adr==None and var.type=="number") or (adr=="number" and var.type=="list"),\
                f"{adr.name} is {adr} but {var.name} is {var.type}"

        self.var1 = var1
        self.var2 = var2
        self.var3 = var3
        
        self.adr1 = adr1
        self.adr2 = adr2
        self.adr3 = adr3

        self.operation = operation
        self.category = "math"
    
    def do(self):
        adr1 = None if self.adr1==None else self.adr1.get()
        adr2 = None if self.adr2==None else self.adr2.get()
        adr3 = None if self.adr3==None else self.adr3.get()

        if self.operation == 'add':
            self.var3.set_data(self.var1.get(adr1) + self.var2.get(adr2), self.adr3)
        elif self.operation == 'sub':
            self.var3.set_data(self.var1.get(adr1) - self.var2.get(adr2), self.adr3)
        elif self.operation == 'mult':
            self.var3.set_data(self.var1.get(adr1) * self.var2.get(adr2), self.adr3)
        return self.var3.data


class JumpInstruction:
    def __init__(self, var1, adr1=None):
        self.var1 = var1
        self.adr1 = adr1

        self.category = "jump"

    def do(self):
        adr1 = None if self.adr1==None else self.adr1.get()
        return self.var1.get(adr1)

class JumpCompare:
    # JE, JL, JG
    def __init__(self, operation, var1, var2, var3, adr1=None, adr2=None, adr3=None):
        """
        operation in (je, jl, jg)
        var are a Variables
        adr are addresses (int)
        """
        for (var,adr) in zip([var1,var2,var3], [adr1,adr2,adr3]):
            #assert var.type == "number" or var.type == "list", f"{var.name} is not an number or a list"
            assert (adr==None and var.type in ("number", "str")) or (adr=="number" and var.type=="list"),\
                f"{adr.name} is {adr} but {var.name} is {var.type}"

        self.var1 = var1
        self.var2 = var2
        self.var3 = var3
        
        self.adr1 = adr1
        self.adr2 = adr2
        self.adr3 = adr3

        self.operation = operation
        self.category = "jump"
        
    def do(self):
        adr1 = None if self.adr1==None else self.adr1.get()
        adr2 = None if self.adr2==None else self.adr2.get()
        adr3 = None if self.adr3==None else self.adr3.get()

        if self.operation=="je":
            if self.var1.get(adr1) == self.var2.get(adr2):
                return self.var3.get(adr3)
        elif self.operation=="jl":
            if self.var1.get(adr1) < self.var2.get(adr2):
                return self.var3.get(adr3)
        elif self.operation=="jg":
            if self.var1.get(adr1) > self.var2.get(adr2):
                return self.var3.get(adr3)
        return 1 
    
class OutputDisplay:
    def __init__(self, var1, adr1=None):
        self.var1 = var1
        self.adr1 = adr1

        self.category = "display"

    def do(self):
        adr1 = None if self.adr1==None else self.adr1.get()
        print(self.var1.get(adr1))