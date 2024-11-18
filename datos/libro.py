class Libro:
    def __init__(self, titulo, autor, genero, anio_publicacion, isbn):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.isbn = isbn

    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.genero})"

    # comentario