class Tree:
    # Cada árbol tendrá:
    # - father: Un objeto Tree()
    # - value: Tupla que representa las coordenadas en la matriz (row, column)
    # - cost: Costo acumulado de llegar a un nodo/arbol desde la raíz
    # - children: Lista de hijos de tipo Tree()

    def __init__(self, father, value, cost, children=[]):
        self.father = father
        self.original_father = father
        self.value = value
        self.original_value = value
        self.cost = cost
        self.original_cost = cost
        self.children = children
        self.compressed = False

    # Crear un hijo de un nodo
    def create_child(self, child_value, cost):
        child = Tree(self, child_value, cost, [])
        self.children.append(child)

    # Calcular la profundidad de un nodo
    def depth(self):
        depth = 0
        current_node = self
        while current_node.father is not None:
            depth += 1
            current_node = current_node.father
        return depth

    # Calcular la ruta de un nodo hasta la raíz del árbol
    def path(self):
        current_node = self
        path = [current_node.value]
        while current_node.father is not None:
            current_node = current_node.father
            path.insert(0, current_node.value)
        return path

    # El nodo actual toma el valor del mejor hijo y borra todos sus hijos
    def compress(self):
        if not self.compressed and self.children:
            best_child = self.children[0]
            for child in self.children:
                if child.cost < best_child.cost:
                    best_child = child
            print(f"Mejor hijo: {best_child}")
            self.value = best_child.value
            self.cost = best_child.cost
            self.children = []
            self.compressed = True

    # El nodo vuelve a tener sus valores originales
    def reexpand(self):
        self.value = self.original_value
        self.cost = self.original_cost
        self.compressed = False

    # Método para devolver una copia del árbol
    def copy(self):
        return Tree(self.father, self.value, self.cost, self.children)

    # Método para comparar si un árbol es menor a otro (por costo)
    def __lt__(self, other):
        return self.cost < other.cost

    # Método para comparar si un árbol es menor o igual a otro (por costo)
    def __le__(self, other):
        return self.cost <= other.cost

    # Método para comparar si un árbol es igual a otro por características
    def __eq__(self, other):
        return (
            self.value == other.value
            and self.cost == other.cost
            and self.path() == other.path()
        )

    # Representación en consola del árbol
    def __repr__(self) -> str:
        depth = self.depth()

        # Costo de la arista
        edge = "____" * depth
        edge = [*edge]
        edge.insert(len(edge) // 2, str(self.cost))
        edge = "".join(edge)

        children = self.children.copy()
        result = f"{'' if not self.father else '|'}{edge}{self.value}\n"
        while children:
            result += str(children.pop(0))
        return result
