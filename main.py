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
                if coeff <= 0:
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

print("Variables d'écart")

# Printing objective function in the required format
print(objectifFonction.replace(' = ', ' - ').replace(' + ', ' - ') + " = 0")

# Printing constraints
for i, (constraint_coeffs, constraint_result) in enumerate(constraints):
    constraint_str = " + ".join([f"{coeff}{variable_name}" for coeff, variable_name in zip(constraint_coeffs, variables.keys())])
    print(f"{constraint_str} + e{i+1} = {constraint_result}")
