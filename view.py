import tkinter as tk
from tkinter import messagebox
import json
import sys
import os
from form import Formulario
from assign_rooms import generate_rooms_data  # Importar la función assign_rooms

DATA_FILE = 'data.json'

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=20, pady=15)  # Añadir margen alrededor de toda la aplicación
        self.create_widgets()
        self.lista_datos = []  # Lista para almacenar los datos añadidos
        self.load_data()  # Cargar los datos desde el archivo JSON

    def create_widgets(self):
        # Título
        self.label = tk.Label(self, text="Formulario para añadir datos")
        self.label.pack(anchor="w", pady=5)  # Añadir margen vertical

        # Crear un contenedor para el formulario y la lista
        self.container = tk.Frame(self)
        self.container.pack()

        # Crear un formulario
        self.formulario = Formulario(self.container, self)
        self.formulario.pack(side=tk.LEFT, padx=5)  # Añadir margen horizontal

        # Espaciador
        self.espaciador = tk.Frame(self.container, width=20)
        self.espaciador.pack(side=tk.LEFT)

        # Contenedor para la lista y los botones
        self.listbox_container = tk.Frame(self.container)
        self.listbox_container.pack(side=tk.RIGHT, padx=5)  # Añadir margen horizontal

        # Lista donde se mostrarán los datos
        self.lista_box = tk.Listbox(self.listbox_container, height=15, width=60)
        self.lista_box.pack(pady=(0, 10))  # Añadir margen vertical

        # Contenedor para los botones de limpiar y generar
        self.button_frame = tk.Frame(self.listbox_container)
        self.button_frame.pack()

        # Botón de limpiar
        self.clear_button = tk.Button(self.button_frame, text="Limpiar", command=self.clear_list)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Botón de generar
        self.generate_button = tk.Button(self.button_frame, text="Generar", command=self.generate_assignments)
        self.generate_button.pack(side=tk.LEFT, padx=5)

        self.lista_box.bind('<<ListboxSelect>>', self.on_select)

    def add_to_list(self, data):
        """Añadir un nuevo dato a la lista y actualizar la vista."""
        self.lista_datos.append(data)
        self.lista_box.insert(tk.END, data)  # Insertar el dato en el Listbox

    def on_select(self, event):
        """Cargar los datos seleccionados en el formulario para editar."""
        if not self.lista_box.curselection():
            return
        index = self.lista_box.curselection()[0]
        data = self.lista_datos[index]
        self.formulario.load_data(data, index)

    def update_list(self, index, data):
        """Actualizar un dato en la lista."""
        self.lista_datos[index] = data
        self.lista_box.delete(index)
        self.lista_box.insert(index, data)

    def clear_form(self):
        """Limpiar el formulario después de agregar un dato."""
        self.formulario.clear_fields()

    def save_data(self):
        """Guardar los datos en un archivo JSON."""
        try:
            with open(DATA_FILE, 'w', encoding="utf-8") as f:
                json.dump(self.lista_datos, f)
            print("✅ Datos guardados correctamente")
        except Exception as e:
            print(f"❌ Error al guardar data.json: {e}")

    def load_data(self):
        """Cargar los datos desde un archivo JSON."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                self.lista_datos = json.load(f)
                for data in self.lista_datos:
                    self.lista_box.insert(tk.END, data)

    def clear_list(self):
        """Limpiar todos los datos de la lista."""
        self.lista_datos.clear()
        self.lista_box.delete(0, tk.END)

    def generate_assignments(self):
        """Llamar a la función assign_rooms para generar asignaciones y mostrar en una nueva ventana."""
        asignaciones = generate_rooms_data(self.lista_datos)
        self.show_assignments(asignaciones)

    def show_assignments(self, asignaciones):
        """Mostrar las asignaciones en una nueva ventana."""
        new_window = tk.Toplevel(self.master)
        new_window.title("Habitaciones Asignadas")
        new_window.geometry("400x300")

        text = tk.Text(new_window, wrap=tk.WORD)
        text.pack(expand=True, fill=tk.BOTH)

        for id, habitacion in asignaciones.items():
            text.insert(tk.END, f"{id}: Habitación {habitacion}\n")

        text.config(state=tk.DISABLED)
