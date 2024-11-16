class NodoBinario:
    def __init__(self, libro):
        self.libro = libro
        self.izquierda = None  # L
        self.derecha = None  # R


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, libro):
        if not self.raiz:
            self.raiz = NodoBinario(libro)
        else:
            self._insertar_recursivo(self.raiz, libro)

    def _insertar_recursivo(self, nodo, libro):
        if libro.titulo.lower() < nodo.libro.titulo.lower():
            if not nodo.izquierda:
                nodo.izquierda = NodoBinario(libro)
            else:
                self._insertar_recursivo(nodo.izquierda, libro)
        else:
            if not nodo.derecha:
                nodo.derecha = NodoBinario(libro)
            else:
                self._insertar_recursivo(nodo.derecha, libro)

    def mostrar_arbol(self):
        if not self.raiz:
            return "Árbol vacío"

        lineas = []
        lineas.append(f"Root (Título): {self.raiz.libro.titulo}")
        self._mostrar_arbol_recursivo(self.raiz, "", True, lineas)
        return "\n".join(lineas)

    def _mostrar_arbol_recursivo(self, nodo, prefijo, es_izquierdo, lineas):
        if not nodo:
            return

        if nodo.izquierda:
            lineas.append(f"{prefijo}L── {nodo.izquierda.libro.titulo}")
            self._mostrar_arbol_recursivo(nodo.izquierda,
                                          prefijo + "    ",
                                          True,
                                          lineas)

        if nodo.derecha:
            lineas.append(f"{prefijo}R── {nodo.derecha.libro.titulo}")
            self._mostrar_arbol_recursivo(nodo.derecha,
                                          prefijo + "    ",
                                          False,
                                          lineas)

    def eliminar(self, titulo):
        self.raiz = self._eliminar_recursivo(self.raiz, titulo.lower())

    def _eliminar_recursivo(self, nodo, titulo):
        if not nodo:
            return None

        if titulo < nodo.libro.titulo.lower():
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, titulo)
        elif titulo > nodo.libro.titulo.lower():
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, titulo)
        else:
            # Caso 1: Nodo hoja o con un solo hijo
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda

            # Caso 2: Nodo con dos hijos
            sucesor = self._encontrar_minimo(nodo.derecha)
            nodo.libro = sucesor.libro
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.libro.titulo.lower())

        return nodo

    def _encontrar_minimo(self, nodo):
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual