import tkinter as tk
from tkinter import messagebox
from constants import MIN_CREDITOS, MAX_CREDITOS, MIN_HABITACION, MAX_HABITACION

class Formulario(tk.Frame):
    def __init__(self, master=None, app=None):
        super().__init__(master)
        self.master = master
        self.app = app
        self.pack()
        self.create_widgets()
        self.edit_index = None

    def create_widgets(self):
        self.label_nombre = tk.Label(self, text="*Nombre:", anchor='w')
        self.label_nombre.pack(fill='x', pady=(5, 0))
        self.entry_nombre = tk.Entry(self, width=40)
        self.entry_nombre.pack(pady=(0, 5))

        self.label_anyo = tk.Label(self, text="*Año:", anchor='w')
        self.label_anyo.pack(fill='x', pady=(5, 0))
        self.entry_anyo = tk.Entry(self, width=40)
        self.entry_anyo.pack(pady=(0, 5))

        self.label_creditos = tk.Label(self, text="*Creditos Obtenidos:", anchor='w')
        self.label_creditos.pack(fill='x', pady=(5, 0))
        self.entry_creditos = tk.Entry(self, width=40)
        self.entry_creditos.pack(pady=(0, 5))

        self.label_habitacion_actual = tk.Label(self, text="*Habitación Actual:", anchor='w')
        self.label_habitacion_actual.pack(fill='x', pady=(5, 0))
        self.entry_habitacion_actual = tk.Entry(self, width=40)
        self.entry_habitacion_actual.pack(pady=(0, 5))

        self.label_habitaciones_solicitadas = tk.Label(self, text="Habitaciones Solicitadas (separadas por comas):", anchor='w')
        self.label_habitaciones_solicitadas.pack(fill='x', pady=(5, 0))
        self.entry_habitaciones_solicitadas = tk.Entry(self, width=40)
        self.entry_habitaciones_solicitadas.pack(pady=(0, 5))

        # Contenedor para los botones
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        # Botón de eliminar (inicialmente oculto)
        self.delete_button = tk.Button(self.button_frame, text="Eliminar", command=self.delete_data)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        self.delete_button.pack_forget()

        # Botón de envío
        self.submit_button = tk.Button(self.button_frame, text="Añadir", command=self.submit_data)
        self.submit_button.pack(side=tk.RIGHT, padx=5)

    def submit_data(self):
        """Se obtienen y validan los datos del formulario y se añaden a la lista, creando o actualizando una nueva entrada."""
        nombre = self.entry_nombre.get()
        anyo = self.entry_anyo.get()
        creditos = self.entry_creditos.get()
        habitacion_actual = self.entry_habitacion_actual.get()
        habitaciones_solicitadas = self.entry_habitaciones_solicitadas.get()     
        # Validaciones   
        if not nombre or not anyo or not creditos or not habitacion_actual:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos obligatorios (*).")
            return
        try:
            anyo = int(anyo)
            if anyo < 1:
                messagebox.showwarning("Advertencia", f"El año de un colegial indica el número de años que lleva en el colegio y por tanto debe ser mayor a 0.")
                return
            creditos = float(creditos)
            if creditos < MIN_CREDITOS or creditos > MAX_CREDITOS:
                messagebox.showwarning("Advertencia", f"Los créditos deben ser un número decimal entre {MIN_CREDITOS} y {MAX_CREDITOS}.")
                return
            habitacion_actual = int(habitacion_actual)
            if habitacion_actual < MIN_HABITACION or habitacion_actual > MAX_HABITACION:
                messagebox.showwarning("Advertencia", f"La habitación actual debe ser un número entero entre {MIN_HABITACION} y {MAX_HABITACION}.")
                return
            if habitaciones_solicitadas:
                habitaciones_solicitadas = [int(h) for h in habitaciones_solicitadas.split(',')]
                if any(h < MIN_HABITACION or h > MAX_HABITACION for h in habitaciones_solicitadas):
                    messagebox.showwarning("Advertencia", f"Todas las habitaciones solicitadas deben ser números enteros entre {MIN_HABITACION} y {MAX_HABITACION}.")
                    return
                if len(habitaciones_solicitadas) != len(set(habitaciones_solicitadas)):
                    messagebox.showwarning("Advertencia", "Se ha introducido más de una vez la misma habitación.")
                    return
                if habitacion_actual in habitaciones_solicitadas:
                    messagebox.showwarning("Advertencia", "La habitación actual no puede estar en la lista de habitaciones solicitadas.")
                    return
            else: habitaciones_solicitadas = [] # Si no se han introducido habitaciones solicitadas se interpreta que no se pde cambio y se asigna una lista vacía
            # Verificar si la habitación actual ya está ocupada
            for colegial in self.app.lista_datos:
                _, _, _, habitacion_ocupada, _ = colegial.split(' - ')
                if int(habitacion_ocupada) == habitacion_actual:
                    messagebox.showwarning("Advertencia", "La habitación actual ya está ocupada.")
                    return
        except ValueError:
            messagebox.showwarning("Advertencia", "Por favor, introduzca valores válidos.")
            return
        # Creación de entrada de la lista
        data = f"{nombre} - {anyo} - {creditos} - {habitacion_actual} - {habitaciones_solicitadas}"
        if self.edit_index is None:
            self.app.add_to_list(data)  # Enviar los datos al método de la clase principal
        else:
            self.app.update_list(self.edit_index, data)
            self.edit_index = None
            self.submit_button.config(text="Añadir")
            self.delete_button.pack_forget()
        self.clear_fields()  # Limpiar el formulario

    def load_data(self, data, index):
        """Se cargan los datos de la entrada seleccionada de la lista para poder ser editados en el formulario."""
        self.edit_index = index
        nombre, anyo, creditos, habitacion_actual, habitaciones_solicitadas = data.split(' - ')
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, nombre)
        self.entry_anyo.delete(0, tk.END)
        self.entry_anyo.insert(0, anyo)
        self.entry_creditos.delete(0, tk.END)
        self.entry_creditos.insert(0, creditos)
        self.entry_habitacion_actual.delete(0, tk.END)
        self.entry_habitacion_actual.insert(0, habitacion_actual)
        habitaciones_solicitadas = habitaciones_solicitadas.strip('[]').replace(' ', '')
        self.entry_habitaciones_solicitadas.delete(0, tk.END)
        self.entry_habitaciones_solicitadas.insert(0, habitaciones_solicitadas)
        self.submit_button.config(text="Actualizar")
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def delete_data(self):
        """Se elimina la entrada de la lista seleccionada."""
        if self.edit_index is not None:
            self.app.lista_datos.pop(self.edit_index)
            self.app.lista_box.delete(self.edit_index)
            self.clear_fields()

    def clear_fields(self):
        """Limpia los campos del formulario."""
        self.entry_nombre.delete(0, tk.END)
        self.entry_anyo.delete(0, tk.END)
        self.entry_creditos.delete(0, tk.END)
        self.entry_habitacion_actual.delete(0, tk.END)
        self.entry_habitaciones_solicitadas.delete(0, tk.END)
        self.edit_index = None
        self.submit_button.config(text="Añadir")
        self.delete_button.pack_forget()
