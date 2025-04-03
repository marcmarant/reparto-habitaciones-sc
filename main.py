import tkinter as tk
from view import Application

def main():
    # Crear la ventana principal de la aplicación
    root = tk.Tk()
    
    # Establecer el título de la ventana principal
    root.title("Asignador de habitaciones SC")

    # Establecer el icono de la ventana principal
    root.iconbitmap("icon.ico")
    
    # Establecer el tamaño inicial de la ventana
    root.geometry("700x350")
    root.resizable(False, False)
    
    # Instanciar la clase Application que contiene la interfaz
    app = Application(master=root)

    # Guardar los datos al cerrar la ventana
    root.protocol("WM_DELETE_WINDOW", lambda: (app.save_data(), root.destroy()))
    
    # Iniciar el bucle principal de la aplicación
    app.mainloop()

if __name__ == "__main__":
    # Ejecutar el programa llamando a la función main
    main()