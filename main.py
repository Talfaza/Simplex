import numpy as np

# Function to find the pivot column
def find_pivot_column(tableau):
    min_value = None
    pivot_column = None
    for index, value in enumerate(tableau[0]):
        if min_value is None or value < min_value:
            min_value = value
            pivot_column = index
    return pivot_column

# Function to find the pivot row
def find_pivot_row(tableau, pivot_column):
    ratios = []
    for index, ligne in enumerate(tableau):
        if index == 0:
            continue  # Ignore the first row (objective function)
        if ligne[pivot_column] <= 0:
            ratios.append(np.inf)  # If the coefficient is negative or zero, assign an infinite value
            continue
        ratios.append(ligne[-1] / ligne[pivot_column])  # Calculate the ratio
    pivot_row = np.argmin(ratios) + 1  # Find the minimum ratio
    return pivot_row

# Initial data
num_variables = 2  # Example number of variables
num_contraintes = 2  # Example number of constraints
tableau = np.array([
    [1, -1, -2, 0],
    [0, 3, 1, 18],
    [0, 1, 1, 4]
], dtype=float)  # Ensure tableau is of float type

iterations = 0
# Continue iterations as long as there are negative coefficients in the Z row
while np.min(tableau[0, :-1]) < 0 and iterations < 100:
    iterations += 1

    # Find pivot column and pivot row
    pivot_column = find_pivot_column(tableau)
    pivot_row = find_pivot_row(tableau, pivot_column)

    # Display iteration results
    print(f"Iteration {iterations}:")
    print(f"The pivot value is: {tableau[pivot_row, pivot_column]}")
    print(f"Its location is: Row {pivot_row}, Column {pivot_column}")

    # Step 1: Divide the pivot row by the pivot value
    pivot_value = tableau[pivot_row, pivot_column]
    tableau[pivot_row] /= pivot_value

    # Step 2: Subtract rows by the value to eliminate multiplied by the pivot row
    for i in range(len(tableau)):
        if i != pivot_row:
            value_to_eliminate = tableau[i, pivot_column]
            tableau[i] -= value_to_eliminate * tableau[pivot_row]

    # Display tableau after Gaussian elimination steps
    print(f"Tableau after iteration {iterations} :")
    print(tableau)

# Retrieve Z value
z_value = tableau[0, -1]
print(f"Z value: {z_value}")
