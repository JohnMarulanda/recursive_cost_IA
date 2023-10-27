from MatrixGenerator import generate_matrix
import pygame
import sys
import heapq
from Tree import Tree

# Inicializar Pygame
pygame.init()

"""
Convenciones del tablero:

0 = Cesped (camino libre)
1 = Arbusto (obstáculo, no se puede pasar)
2 = Finn (posición inicial)
3 = Jake (meta)
4 = Lich (desventaja, aumenta en 3 puntos el coste total)
5 = Espada (bonus, reduce en 2 puntos el coste total)
"""

# Variable para indicar las filas y las columnas de la matriz a generar
matrix_dimensions = 6

# Generación de la matriz
matrix = generate_matrix(matrix_dimensions)

# Tamaño de la ventana
matrix_rows = len(matrix)
matrix_cols = len(matrix[0])

# Ancho de la ventana
window_width = 800
# Ancho deseado para el juego
desired_game_width = 600

# Calcula el ancho de la celda basado en el ancho deseado del juego
cell_width = desired_game_width // matrix_cols

# Altura de la ventana y altura de la celda
window_height = cell_width * matrix_rows
cell_height = window_height // matrix_rows

# Ancho del área en blanco para botones
blank_width = window_width - desired_game_width

# Crear una superficie aparte
blank_surface = pygame.Surface((blank_width, window_height))
blank_surface.fill((45, 87, 44))  # Rellena el área en blanco con blanco

# Coordenadas y tamaño del nuevo botón (debajo del botón existente)
two_button_rect = pygame.Rect(
    600, 200, 160, 80
)  #  Puedes ajustar las coordenadas y el tamaño según tus necesidades


text_rect = pygame.Rect(
    20, 50, 160, 40
)  # Ajusta las coordenadas y el tamaño según tus necesidades

# Cargar las imágenes del botón
button_unpressed_image = pygame.image.load("Sprites/Play_Unpressed.png")
button_pressed_image = pygame.image.load("Sprites/Play_Pressed.png")

# Escalar las imágenes al tamaño deseado (ancho, alto)
button_unpressed_image = pygame.transform.scale(button_unpressed_image, (160, 80))
button_pressed_image = pygame.transform.scale(button_pressed_image, (160, 80))

# Coordenadas donde dibujar la imagen del botón
button_rect = button_unpressed_image.get_rect()
button_rect.topleft = (20, 180)  # Ajusta las coordenadas según tus necesidades

# Estado actual del botón
button_pressed = False

# Crear una fuente para el texto
font = pygame.font.Font("Sprites/PokemonGb-RAeo.ttf", 12)  # Tamaño de la fuente
large_font = pygame.font.Font(
    "Sprites/PokemonGb-RAeo.ttf", 24
)  # Tamaño de la fuente grande


# Crear una superficie degradada
gradient_surface = pygame.Surface((blank_width, window_height))
gradient_rect = gradient_surface.get_rect()
color1 = (159, 205, 218)  # Primer color del degradado
color2 = (255, 255, 255)  # Segundo color del degradado

# Llenar la superficie degradada con un degradado
for y in range(gradient_rect.height):
    gradient_ratio = y / gradient_rect.height
    r = int(color1[0] * (1 - gradient_ratio) + color2[0] * gradient_ratio)
    g = int(color1[1] * (1 - gradient_ratio) + color2[1] * gradient_ratio)
    b = int(color1[2] * (1 - gradient_ratio) + color2[2] * gradient_ratio)
    pygame.draw.line(gradient_surface, (r, g, b), (0, y), (gradient_rect.width, y))

# Cargar imágenes
image_dict = {
    0: pygame.image.load("Sprites/Cesped.png"),
    1: pygame.image.load("Sprites/Arbusto.png"),
    2: pygame.image.load("Sprites/Finn.png"),
    3: pygame.image.load("Sprites/Jake.png"),
    4: pygame.image.load("Sprites/Lich.png"),
    5: pygame.image.load("Sprites/sword.png"),
}


# Coordenadas iniciales y finales para Finn y Jake.
def start_end_coordinates(matrix):
    start_pos = (0, 0)
    end_pos = (0, 0)
    for row in range(matrix_rows):
        for col in range(matrix_cols):
            if matrix[row][col] == 2:
                start_pos = (row, col)
            if matrix[row][col] == 3:
                end_pos = (row, col)
    return start_pos, end_pos


def reiniciar_juego():
    global matrix, result_path
    matrix = generate_matrix(matrix_dimensions)
    result_path = recursive_uniform_cost(matrix)

    while result_path is None:
        # Si se genera una matriz donde no hay al menos un camino posible,
        # se vuelve a ejecutar el algoritmo con una nueva matriz.
        matrix = generate_matrix(matrix_dimensions)
        result_path = recursive_uniform_cost(matrix)


# Algoritmo de búsqueda por costo uniforme recursivo
def recursive_uniform_cost(matrix):
    # Calcular coordenadas iniciales y finales
    start_pos, end_pos = start_end_coordinates(matrix)

    # Creación del árbol
    root = Tree(None, start_pos, 0, [])

    queue = [root]  # Cola de prioridad
    heapq.heapify(queue)
    visited = set()  # Conjunto de nodos visitados

    # Mientras haya nodos por visitar
    while queue:
        # Se obtiene el nodo de menor costo de la cola de prioridad.
        node = heapq.heappop(queue)

        # Se extrae el costo del nodo y su ubicación en la matriz
        cost = node.cost
        row, col = node.value

        # Ignorar el nodo extraido de la cola si ya se visitó
        if node.value in visited:
            continue

        # Si el valor del nodo coincide con la posición final, se retorna
        # la lista de ancestros del nodo para construir el camino
        if node.value == end_pos:
            return node.path()

        # Se añade el nodo actual a la lista de visitados
        visited.add(node.value)

        # Función para calcular los hijos de un nodo a partir de la matriz
        def calculate_children(queue, node):
            # Ciclo para moverse a las 4 direcciones posibles desde el nodo actual
            for direction_row, direction_column in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + direction_row, col + direction_column

                # Se evalúa si se puede mover a x dirección, si en el nodo a moverse no hay un
                # arbusto (obstáculo representado por 1) o si el nodo a moverse no está visitado.
                if (
                    0 <= new_row < matrix_rows
                    and 0 <= new_col < matrix_cols
                    and matrix[new_row][new_col] != 1
                    and (new_row, new_col) not in visited
                ):
                    cost_to_move = 1  # Costo por defecto de moverse a una casilla

                    # Costos de los diferentes elementos del tablero
                    if matrix[new_row][new_col] == 4:  # Lich (desventaja)
                        cost_to_move = 3
                    elif matrix[new_row][new_col] == 5:  # Espada (bonus)
                        cost_to_move = -2

                    # Se crean los hijos del nodo
                    node.create_child((new_row, new_col), cost + cost_to_move)

                    # Se añade el nodo recién creado a la cola de prioridad para explorarse más adelante
                    heapq.heappush(queue, node.children[-1])

            return queue, node

        # Calcular hijos del nodo actual y ponerlos en la cola
        queue, node = calculate_children(queue, node)

        # Validación para saber si se cambiará de rama
        next_node = queue[0] if queue and not queue[0].compressed else False
        branch_will_change = False
        if next_node:
            if node.father and next_node.father:
                # Se evalúa si el padre del nodo actual no está en la lista de ancestros del nodo
                # anterior y viceversa, si el padre del anterior no está en el actual.
                if (
                    node.father.value not in next_node.path()
                    or next_node.father.value not in node.path()
                ):
                    branch_will_change = True

        # Comprimir nodo
        if branch_will_change and not node.compressed:
            queue = list(queue)
            for child in node.children:
                queue.remove(child)
            node.compress()
            heapq.heappush(queue, node)

        # Reexpandir nodo
        if node.compressed:
            node.reexpand()
            queue, node = calculate_children(queue, node)

    return None


# Ejecutar el algoritmo de búsqueda
result_path = recursive_uniform_cost(matrix)
while result_path is None:
    # Si se genera una matriz donde no hay al menos un camino posible,
    # se vuelve a ejecutar el algoritmo con una nueva matriz.
    matrix = generate_matrix(matrix_dimensions)
    result_path = recursive_uniform_cost(matrix)


# Crear la ventana
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("HDA: Buscando a Jake por Costo Uniforme Iterativo")


# Bucle principal para la interfaz gráfica
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if two_button_rect.collidepoint(event.pos):
                reiniciar_juego()
                # Cambia el estado del botón
                button_pressed = True
                # Espera un tiempo antes de restaurar el botón a su estado normal
                pygame.time.set_timer(
                    pygame.USEREVENT, 200
                )  # 200 ms (ajusta según tu preferencia)
        if event.type == pygame.USEREVENT:
            # Restaura el botón a su estado normal
            button_pressed = False

    # Dibuja la superficie degradada en blank_surface con un modo de mezcla
    blank_surface.fill((0, 0, 0))
    blank_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    # Dibujar la matriz de imágenes
    for row in range(matrix_rows):
        for col in range(matrix_cols):
            x = col * cell_width
            y = row * cell_height
            cell_value = matrix[row][col]
            image = image_dict.get(cell_value, None)

            if image:
                # Escalar la imagen al tamaño de la celda
                image = pygame.transform.scale(image, (cell_width, cell_height))
                screen.blit(image, (x, y))

            # Dibujar divisiones
            pygame.draw.rect(screen, (0, 128, 0), (x, y, cell_width, cell_height), 1)

    # Verificar si result_path existe y dibujar el texto en la superficie
    if result_path:
        text_y = 300
        total_cost = 0  # Inicializar el costo total a cero

        for step, position in enumerate(result_path):
            text = font.render(
                f"{step}: [{position[0]}, {position[1]}]", True, (0, 0, 0)
            )  # Texto negro
            blank_surface.blit(text, (60, text_y))
            text_y += 18  # Espacio vertical entre cada línea de texto

            # Calcular el costo de moverse a la posición actual
            row, col = position
            cost_to_move = 1  # Costo por defecto de moverse a una casilla

            # Costos de los diferentes elementos del tablero
            if matrix[row][col] == 4:  # Lich (desventaja)
                cost_to_move = 3
            elif matrix[row][col] == 5:  # Espada (bonus)
                cost_to_move = -2

            # Si no es la primera posición, sumar el costo del paso actual al costo total
            if step > 0:
                total_cost += cost_to_move

        # Imprimir el costo total al final
        text = font.render(f"Costo Total: {total_cost}", True, (0, 0, 0))
        blank_surface.blit(text, (20, text_y))

    # Dibujar bolitas rojas en el centro de cada cuadrado a lo largo del camino
    for step, position in enumerate(
        result_path[1:-1], start=1
    ):  # Excluir el inicio y el final
        row, col = position
        x = col * cell_width + cell_width // 2
        y = row * cell_height + cell_height // 2
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)

    if button_pressed:
        blank_surface.blit(button_pressed_image, button_rect)
    else:
        blank_surface.blit(button_unpressed_image, button_rect)

    # Renderizar el texto centrado en el rectángulo del texto
    text1 = large_font.render("HDA", True, (0, 0, 0))
    text3 = font.render("Recursive Cost", True, (0, 0, 0))
    blank_surface.blit(text1, text_rect.move(50, 10))
    blank_surface.blit(text3, text_rect.move(2, 40))

    screen.blit(blank_surface, (desired_game_width, 0))  # El área de la derecha.
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
