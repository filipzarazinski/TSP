import numpy as np
import random

def generate_distance_matrix(num_cities):
    # Generowanie macierzy odległości
    distance_matrix = np.zeros((num_cities, num_cities), dtype=int)

    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = random.randint(1, 100)
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance

    return distance_matrix

def save_matrix_to_file(matrix, filename):
    # Zapisywanie macierzy do pliku tekstowego
    with open(filename, 'w') as f:
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

# Przykład użycia
num_cities = 10000  # Zmień na żądaną liczbę miast
matrix = generate_distance_matrix(num_cities)
print('done')
# Nazwa pliku do zapisu
filename = 'distance_matrix.txt'
save_matrix_to_file(matrix, filename)
