class NodoNArio:
    def __init__(self, genero=None):
        self.genero = genero
        self.libros = []
        self.hijos = []
        self.padre = None


class ArbolNArio:
    def __init__(self):
        self.raiz = None
        self.todos_los_libros = []
        self.generos_principales = {
            "Literatura": [
                ("Terror", ["Paranormal", "Psicológico", "Gore"]),
                ("Ficción", ["Ciencia Ficción", "Aventura", "Distopía"]),
                ("Biografía", ["Histórica", "Deportiva", "Artística"]),
                ("Comedia", ["Romántica", "Satírica", "Humor Negro"])
            ],
            "Terror": [
                ("Paranormal", []),
                ("Psicológico", []),
                ("Gore", [])
            ],
            "Ficción": [
                ("Ciencia Ficción", []),
                ("Aventura", []),
                ("Distopía", [])
            ],
            "Biografía": [
                ("Histórica", []),
                ("Deportiva", []),
                ("Artística", [])
            ],
            "Comedia": [
                ("Romántica", []),
                ("Satírica", []),
                ("Humor Negro", [])
            ]
        }
        self.inicializar_arbol()

    def inicializar_arbol(self):
        """Inicializa el árbol con Literatura como raíz por defecto"""
        self.crear_estructura_desde_genero("Literatura")

    def crear_estructura_desde_genero(self, genero_raiz):
        """Crea la estructura del árbol manteniendo los libros existentes"""
        self.raiz = NodoNArio(genero_raiz)

        if genero_raiz in self.generos_principales:
            for genero, subgeneros in self.generos_principales[genero_raiz]:
                nodo_genero = NodoNArio(genero)
                nodo_genero.padre = self.raiz
                self.raiz.hijos.append(nodo_genero)

                # Agregar subgéneros
                for subgenero in subgeneros:
                    nodo_subgenero = NodoNArio(subgenero)
                    nodo_subgenero.padre = nodo_genero
                    nodo_genero.hijos.append(nodo_subgenero)

        # Reasignar todos los libros existentes
        for libro in self.todos_los_libros:
            self._insertar_en_estructura(libro)

    def _contar_libros_genero(self, genero):
        """Cuenta los libros que pertenecen a un género específico"""
        count = 0
        genero_lower = genero.lower()
        for libro in self.todos_los_libros:
            if libro.genero.lower() == genero_lower:
                count += 1
        return count

    def insertar(self, libro):
        """Inserta un nuevo libro en el árbol"""
        if libro not in self.todos_los_libros:
            self.todos_los_libros.append(libro)
            self._insertar_en_estructura(libro)
        return True

    def _insertar_en_estructura(self, libro):
        """Inserta un libro en la estructura actual del árbol"""
        genero_libro = libro.genero.strip().lower()

        # Buscar el género exacto
        for nodo in self.raiz.hijos:
            if nodo.genero.lower() == genero_libro:
                if libro not in nodo.libros:
                    nodo.libros.append(libro)
                return True

            # Buscar en subgéneros
            for subnodo in nodo.hijos:
                if subnodo.genero.lower() == genero_libro:
                    if libro not in subnodo.libros:
                        subnodo.libros.append(libro)
                    return True

        # Si no encuentra el género, lo asigna al primer género disponible
        if self.raiz.hijos:
            self.raiz.hijos[0].libros.append(libro)
        return True

    def eliminar_libro(self, libro):
        """Elimina un libro del árbol"""
        if libro in self.todos_los_libros:
            self.todos_los_libros.remove(libro)

        if not self.raiz:
            return False

        # Eliminar de los nodos
        for nodo in self.raiz.hijos:
            if libro in nodo.libros:
                nodo.libros.remove(libro)
                return True
            for subnodo in nodo.hijos:
                if libro in subnodo.libros:
                    subnodo.libros.remove(libro)
                    return True
        return False

    def mostrar_estructura(self):
        """Muestra la estructura del árbol con conteo de libros"""
        if not self.raiz:
            return "Árbol vacío"

        lineas = []
        lineas.append(f"Root (Género): {self.raiz.genero}")
        self._mostrar_estructura_recursivo(self.raiz, "", lineas)
        return "\n".join(lineas)

    def _mostrar_estructura_recursivo(self, nodo, prefijo, lineas):
        for i, hijo in enumerate(nodo.hijos):
            es_ultimo = i == len(nodo.hijos) - 1
            direccion = "L" if i == 0 else "R"

            # Contar libros del género y sus subgéneros
            total_libros = self._contar_libros_genero(hijo.genero)
            for subhijo in hijo.hijos:
                total_libros += self._contar_libros_genero(subhijo.genero)

            # Mostrar género con contador
            lineas.append(f"{prefijo}{direccion}── {hijo.genero} ({total_libros})")

            if hijo.hijos:
                nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
                self._mostrar_estructura_recursivo(hijo, nuevo_prefijo, lineas)

    def obtener_generos(self):
        """Retorna una lista de géneros disponibles para selección"""
        return list(self.generos_principales.keys())

    def obtener_subgeneros(self, genero):
        """Retorna los subgéneros de un género específico"""
        if genero in self.generos_principales:
            return [subgenero for subgenero, _ in self.generos_principales[genero]]
        return []

    def obtener_libros_por_genero(self, genero):
        """Obtiene todos los libros de un género específico"""
        libros = []
        genero_lower = genero.lower()
        for libro in self.todos_los_libros:
            if libro.genero.lower() == genero_lower:
                libros.append(libro)
        return libros

    def esta_vacio(self):
        """Verifica si el árbol está vacío"""
        return len(self.todos_los_libros) == 0

    # Alias para mantener compatibilidad
    def crear_arbol_desde_genero(self, genero):
        return self.crear_estructura_desde_genero(genero)