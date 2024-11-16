class NodoNArio:
    def __init__(self, genero):
        self.genero = genero
        self.libros = []
        self.hijos = []

class ArbolNArio:
    def __init__(self):
        self.raiz = None

    def insertar(self, genero, libro):
        if self.raiz is None:
            self.raiz = NodoNArio(genero)
        self._insertar_recursivo(self.raiz, genero, libro)

    def _insertar_recursivo(self, actual, genero, libro):
        if actual.genero == genero:
            actual.libros.append(libro)
        else:
            for hijo in actual.hijos:
                if hijo.genero == genero:
                    self._insertar_recursivo(hijo, genero, libro)
                    return
            nuevo_nodo = NodoNArio(genero)
            nuevo_nodo.libros.append(libro)
            actual.hijos.append(nuevo_nodo)

    def mostrar_arbol(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        if nodo is not None:
            print("  " * nivel + f"Género: {nodo.genero}")
            for libro in nodo.libros:
                print("  " * (nivel + 1) + f"Libro: {libro.titulo}, Autor: {libro.autor}")
            for hijo in nodo.hijos:
                self.mostrar_arbol(hijo, nivel + 1)
