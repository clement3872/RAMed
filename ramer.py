

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

    def add_action(self, action):
        self.instructions.append(action)

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
        elif self.type == "list" or self.type == "str": 
            self.data[adr] = new_value
            return self.data
    
    def push(self, new_value):
        if self.type=="list":
            self.data.append(new_value)
            return self.data
    
    def pop(self):
        if self.type=="list":
            self.data.pop()
            return self.data


class MovOperation:
    def __init__(self, var1, var2, adr1=None, adr2=None):
        self.var1 = var1
        self.var2 = var2
        
        self.adr1 = adr1
        self.adr2 = adr2
    
        self.category = "mov"

    def do(self):
        adr1 = None if self.adr1==None else self.adr1.get()
        adr2 = None if self.adr2==None else self.adr2.get()
        
        self.var2.set_data(self.var1.get(self.adr1.get()), self.adr2)
        return self.var2.data


class MathOperation:
    def __init__(self, operation, var1, var2, var3, adr1=None, adr2=None, adr3=None):
        """
        operation in (add, sub, mult)
        var are a Variables
        adr are addresses (int)
        """

        assert var1.type == "number" or var1.type == "list", f"{var1.name} is not an number or a list"
        assert var2.type == "number" or var2.type == "list", f"{var2.name} is not an number or a list"
        assert var3.type == "number" or var3.type == "list", f"{var3.name} is not an number or a list"
        assert adr1.type == "number" and adr2.type == "number" and adr3.type == "number", \
            "all addresses should be of type number"

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
            self.var3.set_data(self.var1.get(self.adr1.get()) + self.var2.get(self.adr2.get()), 
                    self.adr3.get())
        elif self.operation == 'sub':
            self.var3.set_data(self.var1.get(self.adr1.get()) - self.var2.get(self.adr2.get()), 
                    self.adr3.get())
        elif self.operation == 'mult':
            self.var3.set_data(self.var1.get(self.adr1.get()) * self.var2.get(self.adr2.get()), 
                    self.adr3.get())
        return self.var3.data


class JumpCompare:
    # JE, JL, JG
    def __init__(self, operation, var1, var2, var3, adr1=None, adr2=None, adr3=None):
        """
        operation in (je, jl, jg)
        var are a Variables
        adr are addresses (int)
        """
        assert var3.type == "number", f"{var3.name} is not an number"
        assert adr1.type == "number" and adr2.type == "number" and adr3.type == "number", \
            "all addresses should be of type number"

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