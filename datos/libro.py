class Libro:
    def __init__(self, titulo, autor, genero, anio_publicacion, isbn, copias=1):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.isbn = isbn
        self.copias = copias  # Inicializamos con una copia del libro

    def aumentar_copias(self):
        self.copias += 1  # Aumentamos el número de copias

    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.genero})"

    # comentario