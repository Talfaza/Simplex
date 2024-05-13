import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

while True:
    try:
        nbrVar = int(input("Donner le nombre de variables : "))
        if nbrVar <= 0:
            raise ValueError("Le nombre de variables doit être positif.")
        break
    except ValueError as ve:
        print(ve)

variables = {}
max_variable_index = None
max_variable_value = 0  # Track the maximum variable value
for i in range(nbrVar):
    variable_name = f"X{i+1}"
    while True:
        try:
            variable_value = int(input(f"Donner la valeur de X{i + 1} : "))
            if variable_value <= 0:
                raise ValueError("La valeur de la variable doit être positive.")
            variables[variable_name] = variable_value
            if variable_value > max_variable_value:
                max_variable_value = variable_value
                max_variable_index = i
            break
        except ValueError as ve:
            print(ve)

while True:
    try:
        nbrContraint = int(input("Donner le nombre de Contraint : "))
        if nbrContraint <= 0:
            raise ValueError("Le nombre de contraintes doit être positif.")
        break
    except ValueError as ve:
        print(ve)

constraints = []

for i in range(nbrContraint):
    constraint_coeffs = []
    for j in range(nbrVar):
        while True:
            try:
                coeff = int(input(f"Donner le coefficient de X{j+1} pour la contrainte {i+1} : "))
                if coeff < 0:
                    raise ValueError("Le coefficient doit être positif.")
                constraint_coeffs.append(coeff)
                break
            except ValueError as ve:
                print(ve)
    while True:
        try:
            constraint_result = int(input(f"Donner le résultat de la contrainte {i+1} : "))
            if constraint_result <= 0:
                raise ValueError("Le résultat de la contrainte doit être positif.")
            constraints.append((constraint_coeffs, constraint_result))
            break
        except ValueError as ve:
            print(ve)

objectifFonction = "z = "
objectifFonction += " + ".join([f"{variables[f'X{i+1}']}X{i+1}" for i in range(nbrVar)])
print("Fonction Objectif : ")
print(objectifFonction)

print("Contraintes :")
for constraint_coeffs, constraint_result in constraints:
    constraint_str = " + ".join([f"{coeff}X{i+1}" for i, coeff in enumerate(constraint_coeffs)])
    print(f"{constraint_str} ≤ {constraint_result}")

for i in range(1, nbrVar + 1):
    print(f"X{i} >= 0")

print("---------------")

# Z -xN = 0 
print(objectifFonction.replace(' = ', ' - ').replace(' + ', ' - ') + " = 0")

# Affichage Contrainte 
for i, (constraint_coeffs, constraint_result) in enumerate(constraints):
    constraint_str = " + ".join([f"{coeff}X{i+1}" if coeff != 0 else "0" for i, coeff in enumerate(constraint_coeffs)])
    slack_vars = ['0' if j != i else '1' for j in range(nbrContraint)]
    print(f"{constraint_str} + {' '.join(['e'+str(j+1) if j == i else '0' for j in range(nbrContraint)])} = {constraint_result}")

# Affichage Entete table (header) 
header = "\nz\t" + "\t".join([f"X{i+1}" for i in range(nbrVar)])
header += "\t" + '\t'.join([f"e{i+1}" for i in range(nbrContraint)]) + "\t="
print(header)

# Premiere Ligne 
print("1\t" + ''.join([f"-{str(variables[f'X{i+1}'])}\t" if i == max_variable_index else f"{str(variables[f'X{i+1}'])}\t" for i in range(nbrVar)]) + '\t'.join(['0' for _ in range(nbrContraint)]) + "\t0")

#  
for i, (constraint_coeffs, constraint_result) in enumerate(constraints):
    slack_vars = ['0' if j != i else '1' for j in range(nbrContraint)]
    constraint_str = " + ".join([f"{coeff}X{i+1}" if coeff != 0 else "0" for i, coeff in enumerate(constraint_coeffs)])
    print("0\t" + ''.join([f"{str(coeff)}\t" if coeff != 0 else '0\t' for coeff in constraint_coeffs]) + '\t'.join(slack_vars) + f"\t{constraint_result}")

# TODO: math    
print("VHB : " + ", ".join([f"{var}" for var in variables.keys()]) + " = 0")
print("\nVB : \n")
for i, (_, constraint_result) in enumerate(constraints):
    print(f"e{i+1} = {constraint_result}")
# Identify the pivot column and pivot row
pivot_column_index = max_variable_index
pivot_row_index = None
pivot_value = float('-inf')

for i, (constraint_coeffs, constraint_result) in enumerate(constraints):
    coeff = constraint_coeffs[pivot_column_index]
    if coeff != 0:
        ratio = constraint_result / coeff
        if ratio > 0 and (pivot_row_index is None or ratio < pivot_value):
            pivot_row_index = i
            pivot_value = ratio

# Check if pivot column is found
if pivot_row_index is None:
    print("The problem is unbounded or infeasible.")
    exit()  # Exit the program or handle the situation accordingly

# Highlight the pivot column and pivot row
pivot_column_highlight = Fore.RED
pivot_row_highlight = Back.RED
print(Fore.RED + "Colonne Pivot : ")
header = "\nz\t" + "\t".join([Fore.RED + f"X{i+1}" + Fore.RESET if max_variable_index == i else f"X{i+1}" for i in range(nbrVar)])
header += "\t" + '\t'.join([f"e{i+1}" for i in range(nbrContraint)]) + "\t="

print(header)

# Premiere Ligne 
print("1\t" + ''.join([Fore.RED + f"-{str(variables[f'X{i+1}'])}\t" + Fore.RESET if i == max_variable_index else f"{str(variables[f'X{i+1}'])}\t" for i in range(nbrVar)]) + '\t'.join(['0' for _ in range(nbrContraint)]) + "\t0")

#  
for i, (constraint_coeffs, constraint_result) in enumerate(constraints):
    slack_vars = ['0' if j != i else '1' for j in range(nbrContraint)]
    constraint_str = " + ".join([f"{coeff}X{i+1}" if coeff != 0 else "0" for i, coeff in enumerate(constraint_coeffs)])
    print("0\t" + ''.join([Fore.RED + f"{str(coeff)}\t" + Fore.RESET if max_variable_index == j else f"{str(coeff)}\t" for j, coeff in enumerate(constraint_coeffs)]) + '\t'.join(slack_vars) + f"\t{constraint_result}")
# Print the tableau with pivot column and pivot row highlighted
print(Fore.RED +"Ligne Pivot")

header = "\nz\t" + "\t".join([f"X{i+1}" for i in range(nbrVar)])
header += "\t" + '\t'.join([f"e{i+1}" for i in range(nbrContraint)]) + "\t="
print(header)

# Premiere Ligne 
pivot_row = constraints[pivot_row_index]
pivot_row_coeffs, pivot_row_result = pivot_row
print("1\t" + ''.join([f"-{str(coeff)}\t" if i == pivot_column_index else f"{str(coeff)}\t" for i, coeff in enumerate(pivot_row_coeffs)]) + '\t'.join(['0' for _ in range(nbrContraint)]) + f"\t{pivot_row_result}")

#  
for i, (constraint_coeffs, constraint_result) in enumerate(constraints):
    slack_vars = ['0' if j != i else '1' for j in range(nbrContraint)]
    constraint_str = " + ".join([f"{coeff}X{i+1}" if coeff != 0 else "0" for i, coeff in enumerate(constraint_coeffs)])
    if i == pivot_row_index:
        print(Fore.RED + "0\t" + ''.join([f"{str(coeff)}\t" if coeff != 0 else '0\t' for coeff in constraint_coeffs]) + '\t'.join(slack_vars) + f"\t{constraint_result}")
    else:
        print("0\t" + ''.join([f"{str(coeff)}\t" if coeff != 0 else '0\t' for coeff in constraint_coeffs]) + '\t'.join(slack_vars) + f"\t{constraint_result}")
