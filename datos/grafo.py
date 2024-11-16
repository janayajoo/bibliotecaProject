class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, libro):
        if libro not in self.vertices:
            self.vertices[libro] = []

    def agregar_relacion(self, libro1, libro2):
        if libro1 in self.vertices and libro2 in self.vertices:
            self.vertices[libro1].append(libro2)
            self.vertices[libro2].append(libro1)
