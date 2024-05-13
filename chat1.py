import sys
import numpy as np
from colorama import Fore, Style

try:
    import pandas as pd
    pandas_av = True
except ImportError:
    pandas_av = False
    pass

noms_produits = []
valeurs_colonnes = []
equation_z = []
lignes_finales = []
solutions = []
x = 'X'
equation_z2 = []
variables_supprimables = []

def main():
    global decimales, nb_contraintes, nb_produits, noms_contraintes
    print(f"""
    {Fore.GREEN}CALCULATEUR DE PROGRAMME LINÉAIRE{Style.RESET_ALL}
    
Quel type de problème voulez-vous résoudre ?	
    1 : Maximisation 
    
    """)
    try:
        type_pb = int(input(f"{Fore.YELLOW}Entrez le numéro du type de problème : {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}Veuillez entrer un numéro parmi les choix ci-dessus.{Style.RESET_ALL}")
        type_pb = int(input(f"{Fore.YELLOW}Entrez le numéro du type de problème : {Style.RESET_ALL}"))
    if type_pb != 1:
        sys.exit(f"{Fore.RED}Vous avez entré un choix de problème incorrect ->{Style.RESET_ALL}" + str(type_pb))

    print('\n##########################################')
    nb_contraintes = int(input(f"{Fore.YELLOW}Combien de produits avez-vous : {Style.RESET_ALL}"))
    nb_produits = int(input(f"{Fore.YELLOW}Combien de contraintes avez-vous : {Style.RESET_ALL}"))
    noms_contraintes = [x + str(i) for i in range(1, nb_contraintes + 1)]
    for i in range(1, nb_produits + 1):
        val_produit = input(f"{Fore.YELLOW}Entrez le nom de la contrainte {i} : {Style.RESET_ALL}")
        noms_produits.append(val_produit)
    print(f"{Fore.BLUE}__________________________________________________{Style.RESET_ALL}")
    if type_pb == 1:
        for i in noms_contraintes:
            try:
                val = float(input(f"{Fore.YELLOW}Entrez la valeur de {i} dans l'équation Z : {Style.RESET_ALL}"))
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre.{Style.RESET_ALL}")
                val = float(input(f"{Fore.YELLOW}Entrez la valeur de {i} dans l'équation Z : {Style.RESET_ALL}"))
            equation_z.append(0 - val)
        equation_z.append(0)

        while len(equation_z) <= (nb_contraintes + nb_produits):
            equation_z.append(0)
        print(f"{Fore.BLUE}__________________________________________________{Style.RESET_ALL}")
        for prod in noms_produits:
            for const in noms_contraintes:
                try:
                    val = float(input(f"{Fore.YELLOW}Entrez la valeur de {const} dans {prod} : {Style.RESET_ALL}"))
                except ValueError:
                    print(f"{Fore.RED}Veuillez vous assurer d'entrer un nombre.{Style.RESET_ALL}")
                    val = float(input(f"{Fore.YELLOW}Entrez la valeur de {const} dans {prod} : {Style.RESET_ALL}"))
                valeurs_colonnes.append(val)
            equate_prod = float(input(f"{Fore.YELLOW}Égaliser {prod} à : {Style.RESET_ALL}"))
            valeurs_colonnes.append(equate_prod)

        colonnes_finales = lignes_standardisees(valeurs_colonnes)
        i = len(noms_contraintes) + 1
        while len(noms_contraintes) < len(colonnes_finales[0]) - 1:
            noms_contraintes.append('X' + str(i))
            solutions.append('X' + str(i))
            i += 1
        solutions.append(' Z')
        noms_contraintes.append('Solution')
        colonnes_finales.append(equation_z)
        lignes_finales = np.array(colonnes_finales).T.tolist()
        print(f"{Fore.BLUE}_____________________________________________{Style.RESET_ALL}")
        decimales = int(input(f"{Fore.YELLOW}Nombre de décimales : {Style.RESET_ALL}"))
        print(f'\n{Fore.BLUE}##########################################{Style.RESET_ALL}')
        maximisation(colonnes_finales, lignes_finales)

    else:
        sys.exit(f"{Fore.RED}Vous avez entré un choix de problème incorrect {Style.RESET_ALL}" + str(type_pb))


def maximisation(colonnes_finales, lignes_finales):
    row_app = []
    derniere_colonne = colonnes_finales[-1]
    min_derniere_ligne = min(derniere_colonne)
    min_manager = 1
  
    print(f"{Fore.GREEN}TABLEAU INITIAL :{Style.RESET_ALL}")
    afficher_tableau(colonnes_finales, noms_contraintes, solutions)
    count = 2
    pivot_element = 2
    while min_derniere_ligne < 0 < pivot_element != 1 and min_manager == 1 and count < 6:
        print(f"{Fore.YELLOW}*********************************************************{Style.RESET_ALL}")
        derniere_colonne = colonnes_finales[-1]
        derniere_ligne = lignes_finales[-1]
        min_derniere_ligne = min(derniere_colonne)
        index_min = derniere_colonne.index(min_derniere_ligne)
        pivot_row = lignes_finales[index_min]
        index_pivot_row = lignes_finales.index(pivot_row)
        row_div_val = []
        i = 0
        for _ in derniere_ligne[:-1]:
            try:
                val = float(derniere_ligne[i] / pivot_row[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                row_div_val.append(val)
            except ZeroDivisionError:
                val = 10000000000
                row_div_val.append(val)
            i += 1
        min_div_val = min(row_div_val)
        index_min_div_val = row_div_val.index(min_div_val)
        pivot_element = pivot_row[index_min_div_val]
        pivot_col = colonnes_finales[index_min_div_val]
        index_pivot_col = colonnes_finales.index(pivot_col)
        row_app[:] = []
        for col in colonnes_finales:
            if col is not pivot_col and col is not colonnes_finales[-1]:
                form = col[index_min] / pivot_element
                final_val = np.array(pivot_col) * form
                new_col = (np.round((np.array(col) - final_val), decimales)).tolist()
                colonnes_finales[colonnes_finales.index(col)] = new_col

            elif col is pivot_col:
                new_col = (np.round((np.array(col) / pivot_element), decimales)).tolist()
                colonnes_finales[colonnes_finales.index(col)] = new_col
            else:
                form = abs(col[index_min]) / pivot_element
                final_val = np.array(pivot_col) * form
                new_col = (np.round((np.array(col) + final_val), decimales)).tolist()
                colonnes_finales[colonnes_finales.index(col)] = new_col
        lignes_finales[:] = []
        re_final_rows = np.array(colonnes_finales).T.tolist()
        lignes_finales = lignes_finales + re_final_rows

        if min(row_div_val) != 10000000000:
            min_manager = 1
        else:
            min_manager = 0
        print(f'{Fore.RED}élément pivot : {pivot_element}{Style.RESET_ALL}')
        print(f'{Fore.MAGENTA}colonne pivot : {pivot_row}{Style.RESET_ALL}')
        print(f'{Fore.MAGENTA}ligne pivot : {pivot_col}{Style.RESET_ALL}')

        print("\n")
        solutions[index_pivot_col] = f"{Fore.MAGENTA}{noms_contraintes[index_pivot_row]}{Style.RESET_ALL}"


        print(f"{Fore.GREEN}TABLEAU {count} :{Style.RESET_ALL}")
        afficher_tableau(colonnes_finales, noms_contraintes, solutions)
        print(f"{Fore.YELLOW}*********************************************************{Style.RESET_ALL}")
        count += 1
        derniere_colonne = colonnes_finales[-1]
        derniere_ligne = lignes_finales[-1]
        min_derniere_ligne = min(derniere_colonne)
        index_min = derniere_colonne.index(min_derniere_ligne)
        pivot_row = lignes_finales[index_min]
        row_div_val = []
        i = 0
        for _ in derniere_ligne[:-1]:
            try:
                val = float(derniere_ligne[i] / pivot_row[i])
                if val <= 0:
                    val = 10000000000
                else:
                    val = val
                row_div_val.append(val)
            except ZeroDivisionError:
                val = 10000000000
                row_div_val.append(val)
            i += 1
        min_div_val = min(row_div_val)
        index_min_div_val = row_div_val.index(min_div_val)
        pivot_element = pivot_row[index_min_div_val]
        if pivot_element < 0:
            print(aucune_solution)

def lignes_standardisees(valeurs_colonnes):
    colonnes_finales = [valeurs_colonnes[x:x + nb_contraintes + 1] for x in range(0, len(valeurs_colonnes), nb_contraintes + 1)]
    for cols in colonnes_finales:
        while len(cols) < (nb_contraintes + nb_produits):
            cols.insert(-1, 0)

    i = nb_contraintes
    for sub_col in colonnes_finales:
        sub_col.insert(i, 1)
        i += 1

    return colonnes_finales


def afficher_tableau(colonnes, noms, solutions):
    try:
        final_pd = pd.DataFrame(np.array(colonnes), columns=noms, index=solutions)
        print(final_pd)
    except:
        print('  ', noms)
        i = 0
        for cols in colonnes:
            print(solutions[i], cols)
            i += 1

if __name__ == "__main__":
    main()
