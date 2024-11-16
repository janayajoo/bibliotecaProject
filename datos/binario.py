class NodoBinario:
    def __init__(self, libro):
        self.libro = libro  # El libro almacenado en el nodo
        self.izquierda = None  # Nodo izquierdo
        self.derecha = None  # Nodo derecho


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, libro):
        if self.raiz is None:
            self.raiz = NodoBinario(libro)  # Si el árbol está vacío, creamos la raíz
        else:
            self._insertar_recursivo(self.raiz, libro)

    def _insertar_recursivo(self, nodo, libro):
        # Comparamos el título para decidir si ir a la izquierda o a la derecha
        if libro.titulo < nodo.libro.titulo:
            if nodo.izquierda is None:
                nodo.izquierda = NodoBinario(libro)  # Insertamos el libro en la izquierda
            else:
                self._insertar_recursivo(nodo.izquierda, libro)  # Recursemos a la izquierda
        else:
            if nodo.derecha is None:
                nodo.derecha = NodoBinario(libro)  # Insertamos el libro en la derecha
            else:
                self._insertar_recursivo(nodo.derecha, libro)  # Recursemos a la derecha

    def mostrar_arbol(self):
        if self.raiz is None:
            return "El árbol está vacío."
        return self._mostrar_arbol_recursivo(self.raiz)

    def _mostrar_arbol_recursivo(self, nodo, nivel=0):
        if nodo is None:
            return ""
        resultado = "  " * nivel + f"{nodo.libro.titulo} ({nodo.libro.isbn})\n"
        resultado += self._mostrar_arbol_recursivo(nodo.izquierda, nivel + 1)  # Recursión izquierda
        resultado += self._mostrar_arbol_recursivo(nodo.derecha, nivel + 1)  # Recursión derecha
        return resultado
