

class RegisterInt:
    def __init__(self, name, value=0):
        self.name = name
        self.value = value

    def __str__(self):
        # return f"[name: {self.name}; value: {self.value}]"
        return f"[{self.name} = {self.value}]"
    
    def __add__(self, reg2):
        return self.value + reg2.value
    
    def set(self, new_value):
        self.value = new_value

class RegisterArray:
    def __init__(self, name, data=[]):
        self.name = name
        self.data = data
        self.size = len(data)

    def __str__(self):
        # return f"[name: {self.name}; data: {self.data}; size: {self.size}]"
        return f"[{self.name} = {self.data}; size={self.size}]"
    
    def get(self, index):
        if type(index) == int:
            return self.data[index]
        elif type(index) == RegisterInt:
            return self.data[index.get()]    

    def set(self, index, new_value):
        # this should not happen
        assert type(new_value) == int, "[RegisterArray.set] type of new_value should be an int" 

        while index >= self.size:
            self.size += 1 
            self.data.append(0)

        if type(index) == int:
            self.data[index] = new_value
        elif type(index) == RegisterInt:
            self.data[index.get()] = new_value


class MathOP:
    """Math operations add, sub, mult"""
    def __init__(self, var1, var2, var3, adr1=None, adr2=None, adr3=None, op_type="add"):
        assert type(var1) in (int, RegisterInt, RegisterArray), "var1 in not a int or RegisterInt or RegisterArray"
        assert type(var2) in (int, RegisterInt, RegisterArray), "var2 in not an int or RegisterInt or RegisterArray"
        assert type(var3) in (RegisterInt, RegisterArray), "var3 in not a RegisterInt or RegisterArray"

        self.var1, self.var2, self.var3 = var1, var2, var3
        self.adr1, self.adr2, self.adr3 = adr1, adr2, adr3

        self.op_type = op_type
        self.category = "math"

    def __str__(self):
        if type(self.var1) == int: v1 = self.var1
        elif type(self.var1) == RegisterInt: v1 = self.var2
        else: v1 = self.var1.get(self.adr1)

        return f"[ {self.op_type}({self.var1}@{self.adr1}, {self.var2}@{self.adr2}, {self.var3}@{self.adr3}) ]"

    def do(self):
        """Applies the instruction"""
        if type(self.var1) == int: v1 = self.var1
        elif type(self.var1) == RegisterInt: v1 = self.var1.value
        else: v1 = self.var1.get(self.adr1)

        if type(self.var2) == int: v2 = self.var2
        elif type(self.var2) == RegisterInt: v2 = self.var2.value
        else: v2 = self.var2.get(self.adr2)

        if self.op_type == "add":
            if type(self.var3)==RegisterInt:
                self.var3.set(v1+v2)
            else: 
                self.var3.set(self.adr3, v1+v2)
        elif self.op_type == "sub":
            if type(self.var3)==RegisterInt:
                self.var3.set(v1-v2)
            else: 
                self.var3.set(self.adr3, v1-v2)
        elif self.op_type == "mult":
            if type(self.var3)==RegisterInt:
                self.var3.set(v1*v2)
            else: 
                self.var3.set(self.adr3, v1*v2)
        return 1 # jump 1 line 


class Div2:
    """Division by 2 (removes last bit)"""
    def __init__(self, var1, adr1, value=0):
        self.var1 = var1
        self.adr1 = adr1

        self.op_type = "div2"
        self.category = "math"

    def __str__(self):
        if type(self.var1)==RegisterArray:
            return f"div2({self.var1}@{self.adr1})"
        else:
            return f"div2({self.var1.name})"

    def do(self):
        """Applies the instruction"""
        if type(self.var1)==RegisterArray:
            self.var1.data[self.adr1] = self.var1.data[self.adr1] >> 1 # devide by 2
        else:
            self.var1 = self.var1 >> 1 # devide by 2
        return 1 # jump 1 line 


class JumpLike:
    """JumpLike in (je, gl, jg)"""
    def __init__(self, op_type, var1, var2, adr1=None, adr2=None, value=1):
        assert type(var1) in (int, RegisterInt, RegisterArray), "var1 in not a int or RegisterInt or RegisterArray"
        assert type(var2) in (int, RegisterInt, RegisterArray), "var2 in not an int or RegisterInt or RegisterArray"

        assert type(value) == int, "A jump value should be a int"
        assert value != 0, "A jump should jump a line, not 0"

        self.value = value
        self.op_type = op_type
        self.category = "jump"

    def __str__(self):
        return f"{self.op_type}({self.var1}@{self.adr1}, {self.var2}@{self.adr2}, {self.value})"

    def do(self):
        """Applies the instruction"""
        return self.value


class Jump:
    """Jump is basic jump"""
    def __init__(self, value=1):
        assert value != 0, "A jump should jump a line, not 0"

        self.value = value
        self.op_type = "jump"
        self.category = "jump"

    def __str__(self):
        return f"Jump({self.value})"

    def do(self):
        """Applies the instruction"""
        return self.value


class Ram:
    def __init__(self, l_reg, l_instr=[]):
        self.registers = l_reg.copy()
        self.instructions = l_instr.copy()
        self.cursor = 0

    def __str__(self):
        s = "RAM:\n-Registers:\n"
        if len(self.registers) == 0: s += "(None)\n"

        # display RAM's registers
        for el in self.registers:
            s = s + '\t' + el.__str__() + "\n"
        s += "\n-Instructions:\n"

        # display RAM's instructions
        if len(self.instructions) == 0: s += "(None)\n"
        for el in self.instructions:
            s = s + '\t' + el.__str__() + "\n"

        s += f"\nCursor position: {self.cursor}"
        return s

    def find(self, name):
        for reg in self.registers:
            if reg.name == name: return reg
        return None
    
    def print_reg_status(self):
        if len(self.registers)>0:
            print("Registers status:")
            for reg in self.registers:
                print(f"\t{reg}")

    def print_next(self):
        """Prints the next step"""
        if self.cursor < len(self.instructions):
            print(f"Next instruction:\n\t{self.instructions[self.cursor]}")
        
    def append_instruction(self, instruction):
        """Does what is says"""
        self.instructions.append(instruction)

    def next(self):
        """Does the next step"""
        self.cursor += self.instructions[self.cursor].do()

    def run(self, verbose=False):
        print("\nRAMing...")
        if verbose:
            self.print_reg_status()
            self.print_next()
            print(f"Cursor: {self.cursor}")
            input("\nPress Enter to continue")
        while self.cursor < len(self.instructions):
            self.next()
            if verbose:
                self.print_reg_status()
                self.print_next()
                print(f"Cursor: {self.cursor}")
                input("\nPress Enter to continue")
        if not verbose: print("(...)")
        out = self.find("o")
        if out != None: print(f"Output register: {out}")
        print(f"You got RAMed in {self.cursor} steps!\n")


if __name__ == "__main__":
    a = RegisterInt("a", 2)
    b = RegisterInt("b", 1)
    c = RegisterInt("c", a+b)
    print(c)
