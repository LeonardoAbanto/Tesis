from src import reporte
import tkinter as tk
from tkinter import filedialog

proyectos = {1: "dateparser-master", 2: "requests-main", 3: "tqdm-master", 4: "pytest-main", 5: "pyyaml-master",
             6: "eli5-master", 7: "pyjanitor-dev", 8: "pyperf-main", 9: "altair-master", 10: "blaze-master"}

# reporte.ReporteTD_UI('C:\\Users\\leona\\Desktop\\TESIS\\ProyectosPython\\' + proyectos[6])

def seleccionar_carpeta():
    # Abrir el diálogo de selección de carpeta
    ruta_carpeta = filedialog.askdirectory()
    reporte.ReporteTD_UI(ruta_carpeta)

ventana = tk.Tk()
ventana.geometry("400x300")
ventana.title("Seleccione carpeta del proyecto")
ventana.configure(background='#D4E4E4')

marco = tk.Frame(ventana)
marco.pack(expand=True)

# Crear un botón para seleccionar la carpeta
boton_seleccionar = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_seleccionar.pack(pady=50)
marco.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Ejecutar el bucle de eventos de la ventana
ventana.mainloop()


