import numpy as np
import re

nbrVar = int(input("Donner le nombre de variables : "))

variables = {}
for i in range(nbrVar):
    variable_name = f"x{i+1}"
    while True:
        try:
            variable_value = int(input(f"Donner la valeur de x{i + 1}: "))
            variables[variable_name] = variable_value
            break
        except ValueError:
            print("Veuillez entrer uniquement des nombres entiers.")

nbrContraint = int(input("Donner le nombre de Contraint : "))

constraints = []
for i in range(nbrContraint):
    constraint_str = input(f"Entrez la contrainte {i + 1}: ")
    constraints.append(constraint_str)

