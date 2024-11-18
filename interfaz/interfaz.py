import tkinter as tk
from tkinter import ttk, messagebox
from datos.libro import Libro
import json
from datos.binario import ArbolBinarioBusqueda
from datos.nario import ArbolNArio

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class InterfazBiblioteca:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Sistema de Gestión de Biblioteca")
        self.raiz.geometry("1000x800")

        # Estructuras de datos
        self.libros = []
        self.diccionario_libros = {}
        self.arbol_binario = ArbolBinarioBusqueda()
        self.arbol_nario = ArbolNArio()

        # Cargar datos desde JSON
        self.cargar_desde_json()

        # Crear el control de pestañas
        self.notebook = ttk.Notebook(self.raiz)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Crear pestañas
        self.tab_agregar = ttk.Frame(self.notebook)
        self.tab_buscar = ttk.Frame(self.notebook)
        self.tab_ordenar = ttk.Frame(self.notebook)
        self.tab_resultados = ttk.Frame(self.notebook)
        self.tab_eliminar = ttk.Frame(self.notebook)
        self.tab_arboles = ttk.Frame(self.notebook)
        self.tab_generos = ttk.Frame(self.notebook)

        # Añadir pestañas al notebook
        self.notebook.add(self.tab_agregar, text="Agregar Libro")
        self.notebook.add(self.tab_buscar, text="Buscar Libro")
        self.notebook.add(self.tab_ordenar, text="Ordenar Libros")
        self.notebook.add(self.tab_resultados, text="Resultados")
        self.notebook.add(self.tab_eliminar, text="Eliminar Libro")
        self.notebook.add(self.tab_arboles, text="Árbol Binario")
        self.notebook.add(self.tab_generos, text="Árbol de Géneros")

        # Crear componentes
        self.crear_componentes_agregar()
        self.crear_componentes_buscar()
        self.crear_componentes_ordenar()
        self.crear_componentes_resultados()
        self.crear_componentes_eliminar()
        self.crear_componentes_arboles()
        self.crear_componentes_generos()

        self.tab_grafos = ttk.Frame(self.notebook)
        self.tab_grafos.pack(fill='both', expand=True)
        self.notebook.add(self.tab_grafos, text="Visualización de Grafos")
        self.crear_componentes_grafos()

        # Ejecutar la interfaz
        self.raiz.mainloop()


    def cargar_desde_json(self):
        try:
            with open("libros.json", "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                for dato in datos:
                    libro = Libro(
                        titulo=dato['titulo'],
                        autor=dato['autor'],
                        genero=dato['genero'],
                        anio_publicacion=dato['anio_publicacion'],
                        isbn=dato['isbn']
                    )
                    self.libros.append(libro)
                    self.diccionario_libros[libro.isbn] = libro
                    self.arbol_binario.insertar(libro)
                    self.arbol_nario.insertar(libro)
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar desde JSON: {str(e)}")

    def guardar_en_json(self):
        try:
            datos = []
            for libro in self.libros:
                datos.append({
                    'titulo': libro.titulo,
                    'autor': libro.autor,
                    'genero': libro.genero,
                    'anio_publicacion': libro.anio_publicacion,
                    'isbn': libro.isbn
                })

            with open("libros.json", "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar en JSON: {str(e)}")

    def crear_componentes_agregar(self):
        frame = ttk.Frame(self.tab_agregar, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Título:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_titulo = ttk.Entry(frame, width=40)
        self.entry_titulo.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Autor:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_autor = ttk.Entry(frame, width=40)
        self.entry_autor.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Género:").grid(row=2, column=0, sticky='w', pady=5)
        self.entry_genero = ttk.Entry(frame, width=40)
        self.entry_genero.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(frame, text="Año:").grid(row=3, column=0, sticky='w', pady=5)
        self.entry_anio = ttk.Entry(frame, width=40)
        self.entry_anio.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(frame, text="ISBN:").grid(row=4, column=0, sticky='w', pady=5)
        self.entry_isbn = ttk.Entry(frame, width=40)
        self.entry_isbn.grid(row=4, column=1, pady=5, padx=5)

        ttk.Button(frame, text="Agregar Libro", command=self.agregar_libro).grid(row=5, column=0, columnspan=2, pady=20)

    def crear_componentes_buscar(self):
        frame = ttk.Frame(self.tab_buscar, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Buscar por:").grid(row=0, column=0, sticky='w', pady=5)
        self.combo_buscar = ttk.Combobox(frame, values=["Título", "Autor", "Género", "Año", "ISBN"], state="readonly")
        self.combo_buscar.grid(row=0, column=1, pady=5, padx=5)
        self.combo_buscar.set("Título")

        ttk.Label(frame, text="Valor:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_buscar = ttk.Entry(frame, width=40)
        self.entry_buscar.grid(row=1, column=1, pady=5, padx=5)

        ttk.Button(frame, text="Buscar", command=self.buscar_libro).grid(row=2, column=0, columnspan=2, pady=20)

    def crear_componentes_ordenar(self):
        frame = ttk.Frame(self.tab_ordenar, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Ordenar por:").grid(row=0, column=0, sticky='w', pady=5)
        self.combo_ordenar = ttk.Combobox(frame, values=["Título", "Autor", "Año"], state="readonly")
        self.combo_ordenar.grid(row=0, column=1, pady=5, padx=5)
        self.combo_ordenar.set("Título")

        ttk.Button(frame, text="Ordenar", command=self.ordenar_libros).grid(row=1, column=0, columnspan=2, pady=20)

    def crear_componentes_resultados(self):
        frame = ttk.Frame(self.tab_resultados, padding="10")
        frame.pack(fill='both', expand=True)

        scroll = ttk.Scrollbar(frame)
        scroll.pack(side='right', fill='y')

        self.text_resultados = tk.Text(frame, width=60, height=20, yscrollcommand=scroll.set)
        self.text_resultados.pack(fill='both', expand=True)
        scroll.config(command=self.text_resultados.yview)

    def crear_componentes_eliminar(self):
        frame = ttk.Frame(self.tab_eliminar, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="ISBN del libro a eliminar:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_eliminar_isbn = ttk.Entry(frame, width=40)
        self.entry_eliminar_isbn.grid(row=0, column=1, pady=5, padx=5)

        ttk.Button(frame, text="Eliminar Libro", command=self.eliminar_libro).grid(row=1, column=0, columnspan=2,
                                                                                   pady=20)

    def crear_componentes_arboles(self):
        frame = ttk.Frame(self.tab_arboles, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="ÁRBOL BINARIO DE LIBROS",
                  font=('Helvetica', 12, 'bold')).pack(pady=5)

        frame_arbol = ttk.Frame(frame)
        frame_arbol.pack(fill='both', expand=True)

        scroll = ttk.Scrollbar(frame_arbol)
        scroll.pack(side='right', fill='y')

        self.text_arbol = tk.Text(frame_arbol, width=60, height=20,
                                  font=('Courier', 10),
                                  yscrollcommand=scroll.set)
        self.text_arbol.pack(fill='both', expand=True)
        scroll.config(command=self.text_arbol.yview)

        ttk.Button(frame, text="Actualizar Árbol",
                   command=self.actualizar_arbol).pack(pady=10)

        self.actualizar_arbol()

    def crear_componentes_generos(self):
        frame = ttk.Frame(self.tab_generos, padding="10")
        frame.pack(fill='both', expand=True)

        frame_seleccion = ttk.LabelFrame(frame, text="Selección de Género Raíz", padding="5")
        frame_seleccion.pack(fill='x', pady=5)

        ttk.Label(frame_seleccion, text="Seleccione el género raíz:").pack(side='left', padx=5)
        self.combo_genero_raiz = ttk.Combobox(
            frame_seleccion,
            values=["Literatura", "Terror", "Ficción", "Biografía", "Comedia"],
            state="readonly",
            width=20
        )
        self.combo_genero_raiz.pack(side='left', padx=5)
        self.combo_genero_raiz.set("Literatura")

        ttk.Button(frame_seleccion,
                   text="Crear Árbol",
                   command=self.crear_arbol_desde_seleccion).pack(side='left', padx=5)

        frame_arbol = ttk.LabelFrame(frame, text="Estructura de Géneros", padding="5")
        frame_arbol.pack(fill='both', expand=True, pady=5)

        scroll = ttk.Scrollbar(frame_arbol)
        scroll.pack(side='right', fill='y')

        self.text_generos = tk.Text(frame_arbol,
                                    width=50,
                                    height=20,
                                    font=('Consolas', 11),
                                    yscrollcommand=scroll.set)
        self.text_generos.pack(fill='both', expand=True)
        scroll.config(command=self.text_generos.yview)

        self.actualizar_vista_arbol()

    def agregar_libro(self):
        try:
            titulo = self.entry_titulo.get()
            autor = self.entry_autor.get()
            genero = self.entry_genero.get()
            anio = int(self.entry_anio.get())
            isbn = self.entry_isbn.get()

            if not all([titulo, autor, genero, isbn]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            if isbn in self.diccionario_libros:
                messagebox.showerror("Error", "Ya existe un libro con este ISBN")
                return

            libro = Libro(titulo, autor, genero, anio, isbn)
            self.libros.append(libro)
            self.diccionario_libros[isbn] = libro
            self.arbol_binario.insertar(libro)
            self.arbol_nario.insertar(libro)

            self.guardar_en_json()

            for entry in [self.entry_titulo, self.entry_autor, self.entry_genero,
                          self.entry_anio, self.entry_isbn]:
                entry.delete(0, tk.END)

            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            self.actualizar_visualizaciones()

        except ValueError:
            messagebox.showerror("Error", "El año debe ser un número válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar libro: {str(e)}")

    def buscar_libro(self):
        criterio = self.combo_buscar.get()
        valor = self.entry_buscar.get()

        if not valor:
            messagebox.showerror("Error", "Ingrese un valor para buscar")
            return

        try:
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
                    messagebox.showerror("Error", "El año debe ser un número")
                    return
            elif criterio == "ISBN":
                resultados = [libro for libro in self.libros if libro.isbn == valor]

            self.mostrar_resultados(resultados)

        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")

    def ordenar_libros(self):
        criterio = self.combo_ordenar.get()
        try:
            if criterio == "Título":
                libros_ordenados = sorted(self.libros, key=lambda x: x.titulo.lower())
            elif criterio == "Autor":
                libros_ordenados = sorted(self.libros, key=lambda x: x.autor.lower())
            elif criterio == "Año":
                libros_ordenados = sorted(self.libros, key=lambda x: x.anio_publicacion)

            self.mostrar_resultados(libros_ordenados)

        except Exception as e:
            messagebox.showerror("Error", f"Error al ordenar: {str(e)}")

    def eliminar_libro(self):
        isbn = self.entry_eliminar_isbn.get()

        if not isbn:
            messagebox.showerror("Error", "Ingrese un ISBN")
            return

        if isbn in self.diccionario_libros:
            libro = self.diccionario_libros[isbn]

            # Eliminar de todas las estructuras
            self.libros.remove(libro)
            del self.diccionario_libros[isbn]
            self.arbol_binario.eliminar(libro.titulo)
            self.arbol_nario.eliminar_libro(libro)

            self.guardar_en_json()
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")

            self.entry_eliminar_isbn.delete(0, tk.END)
            self.actualizar_visualizaciones()
        else:
            messagebox.showerror("Error", "No se encontró un libro con ese ISBN")

    def mostrar_resultados(self, libros):
        self.text_resultados.delete(1.0, tk.END)
        if not libros:
            self.text_resultados.insert(tk.END, "No se encontraron resultados\n")
            return

        for libro in libros:
            self.text_resultados.insert(tk.END,
                                        f"Título: {libro.titulo}\n"
                                        f"Autor: {libro.autor}\n"
                                        f"Género: {libro.genero}\n"
                                        f"Año: {libro.anio_publicacion}\n"
                                        f"ISBN: {libro.isbn}\n"
                                        f"{'-' * 50}\n")

    def actualizar_arbol(self):
        self.text_arbol.delete(1.0, tk.END)
        estructura = self.arbol_binario.mostrar_arbol()
        self.text_arbol.insert(tk.END, estructura)

    def actualizar_vista_arbol(self):
        self.text_generos.delete(1.0, tk.END)
        estructura = self.arbol_nario.mostrar_estructura()
        self.text_generos.insert(tk.END, estructura)

    def crear_arbol_desde_seleccion(self):
        genero_raiz = self.combo_genero_raiz.get()
        if not genero_raiz:
            messagebox.showerror("Error", "Por favor seleccione un género")
            return

        self.arbol_nario.crear_arbol_desde_genero(genero_raiz)
        self.actualizar_vista_arbol()

    def actualizar_visualizaciones(self):
        self.actualizar_arbol()
        self.actualizar_vista_arbol()


    def crear_componentes_grafos(self):
        """Crear la pestaña de visualización de grafos."""
        frame = ttk.Frame(self.tab_grafos, padding="7")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Visualización de Grafos de Libros", font=("Helvetica", 7, "bold")).pack(pady=3)

        # Frame para mostrar el grafo
        frame_grafo = ttk.Frame(frame)
        frame_grafo.pack(fill='both', expand=True)

        self.canvas_grafo = tk.Canvas(frame_grafo, bg="white")
        self.canvas_grafo.pack(fill='both', expand=True, padx=5, pady=5)

        # Generar el grafo inmediatamente al cargar la pestaña
        self.mostrar_grafo()

    def mostrar_grafo(self):
        """Visualiza un grafo con nodos mejor separados."""
        if not self.libros:
            messagebox.showerror("Error", "No hay libros en el sistema.")
            return

        # Crear el grafo
        G = nx.Graph()

        # Añadir nodos y conexiones (libros y atributos)
        for libro in self.libros:
            # Nodo para el libro
            G.add_node(libro.titulo, tipo="libro")

            # Nodos para atributos y conexiones
            G.add_node(libro.genero, tipo="genero")
            G.add_edge(libro.titulo, libro.genero)

            G.add_node(libro.autor, tipo="autor")
            G.add_edge(libro.titulo, libro.autor)

            G.add_node(libro.anio_publicacion, tipo="anio")
            G.add_edge(libro.titulo, libro.anio_publicacion)

        # Posicionar nodos con un mayor espaciado
        pos = nx.spring_layout(G, seed=42, k=1)  # 'k' controla la distancia entre nodos

        # Colores por tipo de nodo
        colores = []
        for nodo, datos in G.nodes(data=True):
            if datos["tipo"] == "libro":
                colores.append("skyblue")  # Libros en azul claro
            elif datos["tipo"] == "genero":
                colores.append("lightgreen")  # Género en verde claro
            elif datos["tipo"] == "autor":
                colores.append("lightcoral")  # Autor en rojo claro
            elif datos["tipo"] == "anio":
                colores.append("lightyellow")  # Año en amarillo claro

        # Crear figura para Matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colores, node_size=500)
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", width=1)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, font_weight="bold")

        # Configuración de visualización
        ax.set_title("Relaciones entre Libros y sus Atributos")
        ax.axis("off")  # Quitar ejes

        # Crear la leyenda
        import matplotlib.patches as mpatches
        libro_patch = mpatches.Patch(color="skyblue", label="Libro (Título)")
        genero_patch = mpatches.Patch(color="lightgreen", label="Género")
        autor_patch = mpatches.Patch(color="lightcoral", label="Autor")
        anio_patch = mpatches.Patch(color="lightyellow", label="Año de Publicación")

        ax.legend(handles=[libro_patch, genero_patch, autor_patch, anio_patch], loc="upper right")

        # Integrar Matplotlib con Tkinter para mostrar el grafo
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_grafo)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.fig = fig  # Guardar referencia a la figura
        plt.close(fig)