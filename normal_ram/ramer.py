

class RegisterInt:
    def __init__(self, name, value=0):
        self.name = name
        self.value = value

    def __str__(self):
        return f"name: {self.name}; value: {self.value}"
    

class RegisterArray:
    def __init__(self, name, data=[]):
        self.name = name
        self.data = data
        self.size = len(data)

    def __str__(self):
        return f"name: {self.name}; data: {self.data}; size: {self.size}"


class MathOP:
    def __init__(self, op_type, value=0):
        self.op_type = op_type
        self.category = "jump"


class JumpLike:
    """JumpLike in (je, gl, jg)"""
    def __init__(self, op_type, value=0):
        self.op_type = op_type
        self.category = "jump"


class Jump:
    """Jump is basic jump"""
    def __init__(self, value=0):
        self.category = "jump"


class Ram:
    def __init__(self, l_reg, l_instr):
        self.registers = l_reg.copy()
        self.instructions = l_instr.copy()
