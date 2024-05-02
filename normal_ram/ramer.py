

class RegisterInt:
    def __init__(self, name, value=0):
        self.name = name
        self.value = value

    def __str__(self):
        return f"[name: {self.name}; value: {self.value}]"
    
    def __add__(self, reg2):
        return self.value + reg2.value

class RegisterArray:
    def __init__(self, name, data=[]):
        self.name = name
        self.data = data
        self.size = len(data)

    def __str__(self):
        return f"[name: {self.name}; data: {self.data}; size: {self.size}]"


class MathOP:
    """Math operations add, sub, mult"""
    def __init__(self, var1, var2, var3, adr1, adr2, adr3, op_type="add", value=0):
        self.var1, self.var2, self.var3 = var1, var2, var3
        self.adr1, self.adr2, self.adr3 = adr1, adr2, adr3

        self.op_type = op_type
        self.category = "math"

    def do(self):
        pass

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
        if type(self.var1)==RegisterArray:
            self.var1.data[self.adr1] = self.var1.data[self.adr1] >> 1 # devide by 2
        else:
            self.var1 = self.var1 >> 1 # devide by 2


class JumpLike:
    """JumpLike in (je, gl, jg)"""
    def __init__(self, op_type="je", value=1):
        assert value != 0, "A jump should jump a line, not 0"

        self.value = value
        self.op_type = op_type
        self.category = "jump"

    def __str__(self):
        return f"{self.op_type}({self.value})"

    def do(self):
        pass


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
        return self.value


class Ram:
    def __init__(self, l_reg, l_instr=[]):
        self.registers = l_reg.copy()
        self.instructions = l_instr.copy()

    def add_instruction(self, instruction):
        pass


if __name__ == "__main__":
    a = RegisterInt("a", 2)
    b = RegisterInt("b", 1)
    c = RegisterInt("c", a+b)
    print(c)
