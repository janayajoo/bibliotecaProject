def ordenar_por_titulo(libros):
    return sorted(libros, key=lambda libro: libro.titulo.lower())

def ordenar_por_autor(libros):
    return sorted(libros, key=lambda libro: libro.autor.lower())

def ordenar_por_genero(libros):
    return sorted(libros, key=lambda libro: libro.genero.lower())

def ordenar_por_anio(libros):
    return sorted(libros, key=lambda libro: libro.anio_publicacion)

def ordenar_por_isbn(libros):
    return sorted(libros, key=lambda libro: libro.isbn)
