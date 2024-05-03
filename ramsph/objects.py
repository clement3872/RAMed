import os

# Classe representant la configuration d'une RAM
# Etat actuel du programme
class RAMConfiguration:
    def __init__(self):
        self.registers = None
        self.current_instruction_index = 0
    
    def set_registers(self, registers):
        self.registers = registers

    def set_current(self, i):
        self.current_instruction_index = i

    def __add__(self, i):
        self.current_instruction_index += i

    def get_registers(self):
        return self.registers
    
    def get_current(self):
        return self.current_instruction_index
    
    # Surcharge du print
    def __str__(self):
        os.system('cls')
        if self.registers == None:
            a = ""
            a += "--------------------------------------------------------\n"
            a += "--                             -------------------------\n"
            a += "-- RAM is not initialized yet  -------------------------\n"
            a += "--                             -------------------------\n"
            a += "--------------------------------------------------------\n"
            return a
        
        res = ""
        res += "--------------------------------------------------------\n"
        res += "--             -----------------------------------------\n"
        res += "--  REGISTERS  -----------------------------------------\n"
        res += "--             -----------------------------------------\n"
        res += "--------------------------------------------------------\n"
        res += "________________________________________________________\n"
        for key, value in self.registers.items():
            res += "=> {0}: {1} ({2})\n".format(key, bin(value), value)
            res += "________________________________________________________\n"


        return res

# Classe representant une instruction
# La methode `resolve` permet la resolution de l'objet lui-meme
class RAMInstruction:
    def __init__(self, opcode, operands):
        if (opcode == "ADD"):
            self.fct = self.add
        elif (opcode == "SUB"):
            self.fct = self.sub
        
        elif (opcode == "MULT"):
            self.fct = self.mult

        elif (opcode == "DIV"):
            self.fct = self.div
        else:
            self.fct = None
        self.operands = operands


    # Resout l'instruction
    def resolve(self, conf: RAMConfiguration):
        return self.fct(conf, *self.operands)

    # Methodes qui reproduit le comportement de chaques opcode
    def add(self, conf, r1, r2, r3):
        if (r3[0] == "i"):
            print("This register is READ-ONLY !")
            return False
    
        registers = conf.get_registers()
        if r2 not in registers.keys() or r3 not in registers.keys():
            print("This register does not exists !")
            return False
        registers[r3] = registers[r1] + registers[r2]

        conf += 1
        return True

    def sub(self, conf, r1, r2, r3):
        if (r3[0] == "i"):
            print("This register is READ-ONLY !")
            return False
        registers = conf.get_registers()
        if r2 not in registers.keys() or r3 not in registers.keys():
            print("This register does not exists !")
            return False
        registers[r3] = registers[r1] - registers[r2]
        conf += 1
        return True

    def mult(self, conf, r1, r2, r3):
        if (r3[0] == "i"):
            print("This register is READ-ONLY !")
            return False
        registers = conf.get_registers()
        if r2 not in registers.keys() or r3 not in registers.keys():
            print("This register does not exists !")
            return False
        registers[r3] = registers[r1] * registers[r2]
        conf += 1
        return True
    
    def div(self, conf, r1, r2, r3):
        if (r3[0] == "i"):
            print("This register is READ-ONLY !")
            return False
        registers = conf.get_registers()
        if r2 not in registers.keys() or r3 not in registers.keys():
            print("This register does not exists !")
            return False
        registers[r3] = registers[r1] / registers[r2]
        conf += 1
        return True
    
    def jump(self, conf, index, r1):
        if (r1[0] == "i"):
            print("This register is READ-ONLY !")
            return False
        

# RAM Machine
class RAMMachine:
    def __init__(self, registers, instr_lst):
        self.registers = registers
        self.instr_lst = instr_lst
        
    def get_registers(self):
        return self.registers
    
    def get_instruction_lst(self):
        return self.instr_lst
    
    # On resout l'instruction actuel grace a l'index actuel present dans l'objet configuration
    def res_an_instr(self, conf: RAMConfiguration):
        if conf.get_current() >= len(self.get_instruction_lst()):
            return False
        return self.instr_lst[conf.get_current()].resolve(conf)