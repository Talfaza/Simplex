while True:
    try:
        nbrVar = int(input("Donner le nombre de variables : "))
        if nbrVar <= 0:
            raise ValueError("Le nombre de variables doit être positif.")
        break
    except ValueError as ve:
        print(ve)

variables = {}
for i in range(nbrVar):
    variable_name = f"X{i+1}"
    while True:
        try:
            variable_value = int(input(f"Donner la valeur de X{i + 1} : "))
            if variable_value <= 0:
                raise ValueError("La valeur de la variable doit être positive.")
            variables[variable_name] = variable_value
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

# Fonction Optimal
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
print("\nz\t" + "\t".join([f"X{i+1}" for i in range(nbrVar)]) + f"\t{'\t'.join(['e'+str(i+1) for i in range(nbrContraint)])}\t=")

# Premiere Ligne 
print(f"1\t{''.join(['-' + str(variables[f'X{i+1}']) + '\t' for i in range(nbrVar)])}{'\t'.join(['0' for _ in range(nbrContraint)])}\t0")

#  
for i, (constraint_coeffs, constraint_result) in enumerate(constraints):
    slack_vars = ['0' if j != i else '1' for j in range(nbrContraint)]
    constraint_str = " + ".join([f"{coeff}X{i+1}" if coeff != 0 else "0" for i, coeff in enumerate(constraint_coeffs)])
    print(f"0\t{''.join([str(coeff) + '\t' if coeff != 0 else '0\t' for coeff in constraint_coeffs])}{'\t'.join(slack_vars)}\t{constraint_result}")



# TODO: math    

print("VHB : " + ", ".join([f"{var}" for var in variables.keys()]) + " = 0")












