import os
from main import open_ram

example = "ram_code/example.ramed"
ram_word = "ram_code/words.ramed"
to_opti = "ram_code/to_opti.ramed"

def quest1():
    mode, ram = open_ram(filename=example, verbose="0",question=True)
    print(ram)

def quest2():
    mode, ram = open_ram(filename=example, verbose="0",question=True)
    print("RAM, avant:\n", ram)
    ram.next()
    print("\nRAM, apres:\n", ram)

def quest3():
    word = "0 1 1 0 0"
    py = "python"
    verbose = "0"
    os.system(f"{py} main.py {ram_word} {verbose} {word}")
    print(f"La o=['nombre de 0', 'nombre de 1'] dans l'entree: {word}")

def quest4():
    word = "0 1 1 0 0"
    py = "python"
    verbose = "1"
    os.system(f"{py} main.py {ram_word} {verbose} {word}")
    print(f"La o=['nombre de 0', 'nombre de 1'] dans word: {word}")


def quest9():
    mode, ram = open_ram(filename=to_opti, verbose="0",question=True)
    print("RAM, avant optimisation:", ram)
    print("\nRAM, apres optimisation:", ram.optimize())
    print("\nEssayons de l'executer:")
    ram.run()

if __name__ == "__main__":
    t = """Selection la question que vous voulez executer:
    (question n, appuyez sur : n)
     - question 1 : 1
     - question 2 : 2
     - question 3 : 3
     - question 4 : 4
     - question 9 : 9
    """
    print(t)
    nb_question = int(input())

    if nb_question == 1: quest1()
    elif nb_question == 2: quest2()
    elif nb_question == 3: quest3()
    elif nb_question == 4: quest4()
    elif nb_question == 9: quest9()
    else: print("Wrong number O_O")
