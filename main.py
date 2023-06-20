from src import reporte
import tkinter as tk
from tkinter import filedialog


def seleccionar_carpeta():
    # Abrir el diálogo de selección de carpeta
    ruta_carpeta = filedialog.askdirectory()
    reporte.ReporteTD_UI(ruta_carpeta)


ventana = tk.Tk()
ventana.geometry("400x300")
ventana.title("Seleccione carpeta del proyecto")
ventana.configure(background='#D4E4E4')

marco = tk.Frame(ventana, background='white', borderwidth=2, relief="solid")
marco.pack(expand=True)

# Crear un botón para seleccionar la carpeta
label = tk.Label(marco, text="Seleccione carpeta del proyecto", font=("Arial", 15), background='white', pady=10, padx=10)
label.pack()
boton_seleccionar = tk.Button(marco, text="Seleccionar Carpeta", command=seleccionar_carpeta, font=("Arial", 15),
                              background='white', pady=20)
boton_seleccionar.pack(pady=20)
marco.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Ejecutar el bucle de eventos de la ventana
ventana.mainloop()


