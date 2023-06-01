import tkinter as tk

# Crear una instancia de la ventana principal
ventana = tk.Tk()

# Crear un widget de etiqueta para mostrar la información
etiqueta = tk.Label(ventana, text="Información a mostrar", font=("Arial", 12))

# Organizar el widget de etiqueta en la ventana
etiqueta.pack()

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()
