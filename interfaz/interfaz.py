import tkinter as tk
from tkinter import ttk, messagebox
from datos.libro import Libro
import json
from datos.binario import ArbolBinarioBusqueda

class InterfazBiblioteca:

    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Sistema de Gestión de Biblioteca")

        # Estructuras de datos
        self.libros = []
        self.diccionario_libros = {}
        self.arbol_binario = ArbolBinarioBusqueda()  # Árbol binario para organizar los libros por título

        # Cargar datos desde JSON
        self.cargar_desde_json()

        # Crear el control de pestañas
        self.notebook = ttk.Notebook(self.raiz)
        self.notebook.grid(row=0, column=0, padx=10, pady=10)

        # Crear pestañas para organizar los componentes
        self.tab_agregar = ttk.Frame(self.notebook)
        self.tab_buscar = ttk.Frame(self.notebook)
        self.tab_ordenar = ttk.Frame(self.notebook)
        self.tab_resultados = ttk.Frame(self.notebook)
        self.tab_eliminar = ttk.Frame(self.notebook)
        self.tab_arbol = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_agregar, text="Agregar Libro")
        self.notebook.add(self.tab_buscar, text="Buscar Libro")
        self.notebook.add(self.tab_ordenar, text="Ordenar Libros")
        self.notebook.add(self.tab_resultados, text="Resultados")
        self.notebook.add(self.tab_eliminar, text="Eliminar Libro")
        self.notebook.add(self.tab_arbol, text="Árbol Binario")

        # Crear componentes de cada pestaña
        self.crear_componentes_agregar()
        self.crear_componentes_buscar()
        self.crear_componentes_ordenar()
        self.crear_componentes_resultados()
        self.crear_componentes_eliminar()
        self.crear_componentes_arbol()

        # Ejecutar la interfaz
        self.raiz.mainloop()

    def cargar_desde_json(self):
        try:
            with open("libros.json", "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                for dato in datos:
                    libro = Libro(**dato)
                    self.libros.append(libro)
                    self.diccionario_libros[libro.isbn] = libro
                    # Insertar en el árbol binario cuando cargamos los libros
                    self.arbol_binario.insertar(libro)
        except FileNotFoundError:
            pass

    def guardar_en_json(self):
        datos = [libro.__dict__ for libro in self.libros]
        with open("libros.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        messagebox.showinfo("Éxito", "Los datos se han guardado correctamente.")

    def crear_componentes_agregar(self):
        # Componentes para la pestaña "Agregar Libro"
        tk.Label(self.tab_agregar, text="Título:").grid(row=0, column=0, sticky=tk.W)
        self.entry_titulo = tk.Entry(self.tab_agregar, width=30)
        self.entry_titulo.grid(row=0, column=1)

        tk.Label(self.tab_agregar, text="Autor:").grid(row=1, column=0, sticky=tk.W)
        self.entry_autor = tk.Entry(self.tab_agregar, width=30)
        self.entry_autor.grid(row=1, column=1)

        tk.Label(self.tab_agregar, text="Género:").grid(row=2, column=0, sticky=tk.W)
        self.entry_genero = tk.Entry(self.tab_agregar, width=30)
        self.entry_genero.grid(row=2, column=1)

        tk.Label(self.tab_agregar, text="Año de Publicación:").grid(row=3, column=0, sticky=tk.W)
        self.entry_anio = tk.Entry(self.tab_agregar, width=30)
        self.entry_anio.grid(row=3, column=1)

        tk.Label(self.tab_agregar, text="ISBN:").grid(row=4, column=0, sticky=tk.W)
        self.entry_isbn = tk.Entry(self.tab_agregar, width=30)
        self.entry_isbn.grid(row=4, column=1)

        tk.Button(self.tab_agregar, text="Agregar Libro", command=self.agregar_libro).grid(row=5, column=0, columnspan=2, pady=10)

    def crear_componentes_buscar(self):
        # Componentes para la pestaña "Buscar Libro"
        tk.Label(self.tab_buscar, text="Criterio de Búsqueda:").grid(row=0, column=0)
        self.combo_buscar = ttk.Combobox(self.tab_buscar, values=["Título", "Autor", "Género", "Año", "ISBN"], state="readonly")
        self.combo_buscar.grid(row=0, column=1)

        tk.Label(self.tab_buscar, text="Valor:").grid(row=1, column=0)
        self.entry_buscar = tk.Entry(self.tab_buscar, width=30)
        self.entry_buscar.grid(row=1, column=1)

        tk.Button(self.tab_buscar, text="Buscar", command=self.buscar_libro).grid(row=2, column=0, columnspan=2, pady=10)

    def crear_componentes_ordenar(self):
        # Componentes para la pestaña "Ordenar Libros"
        tk.Label(self.tab_ordenar, text="Ordenar por:").grid(row=0, column=0)
        self.combo_ordenar = ttk.Combobox(self.tab_ordenar, values=["Título", "Autor", "Año"], state="readonly")
        self.combo_ordenar.grid(row=0, column=1)

        tk.Button(self.tab_ordenar, text="Ordenar", command=self.ordenar_libros).grid(row=0, column=2, padx=10)

    def crear_componentes_resultados(self):
        # Componentes para la pestaña "Resultados"
        self.text_resultados = tk.Text(self.tab_resultados, width=60, height=15)
        self.text_resultados.pack()

    def crear_componentes_eliminar(self):
        # Componentes para la pestaña "Eliminar Libro"
        tk.Label(self.tab_eliminar, text="ISBN:").grid(row=0, column=0)
        self.entry_eliminar_isbn = tk.Entry(self.tab_eliminar, width=30)
        self.entry_eliminar_isbn.grid(row=0, column=1)

        tk.Button(self.tab_eliminar, text="Eliminar Libro", command=self.eliminar_libro_ui).grid(row=1, column=0, columnspan=2, pady=10)

    def crear_componentes_arbol(self):
        # Componentes para la pestaña "Árbol Binario"
        self.text_arbol = tk.Text(self.tab_arbol, width=60, height=10)
        self.text_arbol.pack()

    # Funciones de la interfaz
    def agregar_libro(self):
        try:
            titulo = self.entry_titulo.get()
            autor = self.entry_autor.get()
            genero = self.entry_genero.get()
            anio = int(self.entry_anio.get())
            isbn = self.entry_isbn.get()

            if isbn in self.diccionario_libros:
                messagebox.showerror("Error", "Ya existe un libro con este ISBN.")
                return

            libro = Libro(titulo, autor, genero, anio, isbn)
            self.libros.append(libro)
            self.diccionario_libros[isbn] = libro

            # Insertar el libro en el árbol binario
            self.arbol_binario.insertar(libro)

            # Guardar cambios en JSON
            self.guardar_en_json()

            # Limpiar campos
            self.entry_titulo.delete(0, tk.END)
            self.entry_autor.delete(0, tk.END)
            self.entry_genero.delete(0, tk.END)
            self.entry_anio.delete(0, tk.END)
            self.entry_isbn.delete(0, tk.END)

            messagebox.showinfo("Éxito", "Libro agregado correctamente.")

            # Actualizar la interfaz con los libros ordenados
            self.actualizar_interfaz()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def buscar_libro(self):
        criterio = self.combo_buscar.get()
        valor = self.entry_buscar.get()
        resultados = []

        if criterio == "Título":
            resultados = [libro for libro in self.libros if valor.lower() in libro.titulo.lower()]
        elif criterio == "Autor":
            resultados = [libro for libro in self.libros if valor.lower() in libro.autor.lower()]
        elif criterio == "Género":
            resultados = [libro for libro in self.libros if valor.lower() in libro.genero.lower()]
        elif criterio == "Año":
            try:
                anio = int(valor)
                resultados = [libro for libro in self.libros if libro.anio_publicacion == anio]
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese un año válido.")
                return
        elif criterio == "ISBN":
            resultados = [libro for libro in self.libros if libro.isbn == valor]

        self.mostrar_resultados(resultados)

    def ordenar_libros(self):
        criterio = self.combo_ordenar.get()
        if criterio == "Título":
            self.libros.sort(key=lambda libro: libro.titulo)
        elif criterio == "Autor":
            self.libros.sort(key=lambda libro: libro.autor)
        elif criterio == "Año":
            self.libros.sort(key=lambda libro: libro.anio_publicacion)

        self.mostrar_resultados(self.libros)

    def mostrar_resultados(self, resultados):
        self.text_resultados.delete(1.0, tk.END)
        if resultados:
            for libro in resultados:
                self.text_resultados.insert(tk.END, f"{libro}\n")
        else:
            self.text_resultados.insert(tk.END, "No se encontraron resultados.\n")

    def eliminar_libro_ui(self):
        isbn = self.entry_eliminar_isbn.get()
        if isbn in self.diccionario_libros:
            libro = self.diccionario_libros.pop(isbn)
            self.libros.remove(libro)
            # Eliminar el libro del árbol binario
            self.arbol_binario.eliminar(libro)

            self.guardar_en_json()
            messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
            self.actualizar_interfaz()
        else:
            messagebox.showerror("Error", "No se encontró un libro con ese ISBN.")

    def actualizar_interfaz(self):
        self.text_arbol.delete(1.0, tk.END)
        self.text_arbol.insert(tk.END, self.arbol_binario.mostrar_inorden())
