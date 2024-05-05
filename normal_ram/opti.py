import ramer

def get_accessibles(l_instructions):
    # we don't really need a graphe for this... or do we?
    l_index = []

    def rec_access(l_instructions, cursor=0):
        if cursor in l_index or cursor >= len(l_instructions):
            return 0
        else:
            l_index.append(cursor)
            instr = l_instructions[cursor]
            if instr == None:
                # if it's NOT a conditionnal jump
                rec_access(l_instructions,cursor+1)
            elif instr.op_type in ("je", "jl", "jg"): 
                # if it's a conditionnal jump
                rec_access(l_instructions,cursor+instr.value)
                rec_access(l_instructions,cursor+1)
            else:
                if instr.op_type=="jump":
                    # if it's a jump (not conditionnal)
                    rec_access(l_instructions, cursor+instr.value)
                else:
                    rec_access(l_instructions,cursor+1)

    rec_access(l_instructions)
    return l_index

def remove_inacessibles(ram):
    # `ram` is an object ramer.Ram
    l = get_accessibles(ram.instructions)

    for i in range(len(ram.instructions)):
        if i not in l:
            ram.cleared = False # to see if there is a None in self.instructions
            ram.solved = False # same idea for `solve_issues` function
            ram.instructions[i] = None

    return ram.solve_issues()
