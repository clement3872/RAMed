from objects import *

'''
EXEMPLE:

SUB i0,i3,r0 => soustrait la valeur dans i3 a celle dans i0 et met le resultat dans r0

SUB i0,i4,i1 => Ne marche pas car les registre  `i` sont en READ-ONLY

'''

#######
# Q1  #
#######

def init_ram(file_path, input_word):
    # Initialisation du registres
    registers = {}
    str_entry = str(input_word)
    registers["i0"] = len(str_entry)
    for i in range(len(str_entry)):
        temp_ind = i + 1
        registers["i" + str(temp_ind)] = int(str_entry[i])

    # infinité de registres
    for i in range(5):
        registers["r{0}".format(i)] = 0

    # Initialisation de la liste d'instructions
    instruction_lst = []
    with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                opcode = parts[0]

                operands = parts[1].split(",")
                instruction = RAMInstruction(opcode, operands)
                instruction_lst.append(instruction)

    # Creation du programme
    return RAMMachine(registers, instruction_lst)


#######
# Q2  #
#######
# Je met le type pour l'autocompletion, on pourra enlever apres

def oneStep(ram: RAMMachine, conf: RAMConfiguration):
    if conf.get_registers() == None:
        return False
    
    # Resolu l'instruction pointe par conf
    if not ram.res_an_instr(conf):
        return False
    return True
    

#######
#Q3-4 #
#######
import time
def allSteps(file, input):
    mach = init_ram(file, input)
    conf = RAMConfiguration()
    conf.set_registers(mach.get_registers())

    print(conf)

    while True:
        time.sleep(3)
        if not oneStep(mach, conf):
            break
        print(conf)

    print("FIN")




# A corriger !!!!! 
# Gerer les erreurs
# Plein de trucs



if __name__ == "__main__":
    allSteps("machine_ram.txt", 42412)
    
    



    
    


