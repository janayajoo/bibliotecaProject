def buscar_por_titulo(libros, titulo):
    return [libro for libro in libros if libro.titulo.lower() == titulo.lower()]

def buscar_por_autor(libros, autor):
    return [libro for libro in libros if libro.autor.lower() == autor.lower()]

def buscar_por_genero(libros, genero):
    return [libro for libro in libros if libro.genero.lower() == genero.lower()]

def buscar_por_anio(libros, anio):
    return [libro for libro in libros if libro.anio_publicacion == anio]

def buscar_por_isbn(libros, isbn):
    return [libro for libro in libros if libro.isbn == isbn]
