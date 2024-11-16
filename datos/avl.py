class NodoAVL:
    def __init__(self, libro):
        self.libro = libro
        self.altura = 1
        self.izquierdo = None
        self.derecho = None

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, libro):
        self.raiz = self._insertar_recursivo(self.raiz, libro)

    def _insertar_recursivo(self, nodo, libro):
        if not nodo:
            return NodoAVL(libro)
        if libro.anio_publicacion < nodo.libro.anio_publicacion:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, libro)
        else:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, libro)

        # Actualizar altura y balancear
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierdo), self._obtener_altura(nodo.derecho))
        return self._balancear(nodo)

    def _obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balancear(self, nodo):
        # Balancear nodo aquí...
        return nodo
