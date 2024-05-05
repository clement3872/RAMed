# RAMed


## (normal) RAM

#### Instructions implémentées / Implemented Instructions
- ADD (addition)
- SUB (subtraction)
- MULT (multiplication)
- DIV2 (divide by 2) (removes last bit)
- JUMP (jump to a instruction in the code)
- JE (Jump if Equal)
- JL (Jump if Less)
- JG (Jump if Greater)

## Advanced RAM

#### Instructions implémentées / Implemented Instructions, same as normal RAM plus:
- MOV (put a value into a register)
- PUSH (append an element to the end of a list)
- POP (removes the last element of a list)

------

### FR

Notes:
Le code n'est pas sensible aux majuscules/minuscules (add = ADD; R1 = r1; ...).
Il ne faut pas mettre d'instructions imbriquées (exemple à ne pas faire: MOV(ADD(...)))
Merci de regarder les exemples qui se trouvent dans le dossier `normal/ram_code` pour comprendre comment creer un fichier RAM.

Il faut aussi noter que Advanced RAM est du bonus, et n'est clairement pas fini.

### Utilisation

#### Vous pouvez utilser les commandes suivantes
- `make quest` : pour executer le fichier *questions.py*.
- `make ex` : simuler un fichier exemple.
- `make ex_verbose` : simuler un fichier example avec le mode *verbose*.
- `python main.py ram_file.ramed 0` : simuler une machine RAM **sans** le mode *verbose* et sans entree.
- `python main.py ram_file.ramed 1` : simuler une machine RAM **avec** le mode *verbose* et sans entree.
- `python main.py ram_file.ramed 0 int1 int2 int3 ...` : simuler une machine RAM (sans le mode *verbose*) et avec un entree.
- `python main.py ram_file.ramed 1 int1 int2 int3 ...` : meme chose avec le mode verbose.

### ENG

Notes:
The code is not case sensitive (add = ADD; R1 = r1; ...).
Nested instructions should not be used (example not to do: MOV(ADD(...)))
Please look in the `normal/ram_code` folder to try to understand how to creates your own RAM file.

We must note as well that Advanced RAM is bonus, it's not finished.

### Usage

#### You can use the following commandes
- `make quest` : to run the python *questions.py* file.
- `make ex` : to run an example file.
- `make ex_verbose` : to run an example file with *verbose* mode on.
- `python main.py ram_file.ramed 0` : simulate a RAM machine **without** verbose mode.
- `python main.py ram_file.ramed 1` : simulate a RAM machine **with** verbose mode.
- `python main.py ram_file.ramed 0 int1 int2 int3 ...` : simulate a RAM machine (without verbose) with an entry.
- `python main.py ram_file.ramed 1 int1 int2 int3 ...` : simulate a RAM machine (with verbose) with an entry.
