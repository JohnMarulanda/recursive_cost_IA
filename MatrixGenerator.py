import random
import math


def generate_matrix(dimensions):
    # Función para crear los obstáculos enviados como argumentos
    def create_obstacles(probability, obstacle, dimensions, matrix):
        for _ in range(probability):
            fila_aleatoria = random.randint(0, dimensions - 1)
            columna_aleatoria = random.randint(0, dimensions - 1)
            while matrix[fila_aleatoria][columna_aleatoria] == obstacle:
                fila_aleatoria = random.randint(0, dimensions - 1)
                columna_aleatoria = random.randint(0, dimensions - 1)
            matrix[fila_aleatoria][columna_aleatoria] = obstacle
        return matrix

    # Probabilidad que se le asignó a cada uno de los obstáculos
    # (basada en las casillas del tablero)
    arbustos = math.floor((dimensions * dimensions) * 0.4)
    lich = math.floor((dimensions * dimensions) * 0.20)
    espadas = math.floor((dimensions * dimensions) * 0.10)

    # Inicializamos una matriz llena de ceros (casillas libres)
    matrix = [[0 for _ in range(dimensions)] for _ in range(dimensions)]

    # Llenamos la matriz con los obstáculos
    create_obstacles(arbustos, 1, dimensions, matrix)
    create_obstacles(lich, 4, dimensions, matrix)
    create_obstacles(espadas, 5, dimensions, matrix)

    # Elegimos una posición aleatoria en la matriz y le asignamos a Finn (posición inicial)
    # Finn está representado por el número 2
    random_row = random.randint(0, dimensions - 1)
    random_column = random.randint(0, dimensions - 1)
    matrix[random_row][random_column] = 2

    # Elegimos otra posición aleatoria y se la asignamos a Jake, asegurándonos de que
    # sea diferente a la primera. Jake está representado con el número 3
    while True:
        random_row = random.randint(0, dimensions - 1)
        random_column = random.randint(0, dimensions - 1)
        if matrix[random_row][random_column] != 2:
            matrix[random_row][random_column] = 3
            break

    return matrix
