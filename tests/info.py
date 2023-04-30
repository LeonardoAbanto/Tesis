import os
import radon
import radon.raw
from app import metricas_radon
def InformacionBasica (project_dir):
    # Lista para almacenar los nombres de los archivos Python
    python_files = []

    # Recorremos el directorio y almacenamos los nombres de los archivos Python
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    #Información del proyecto
    tloc = 0
    for file_name in python_files:
        with open(file_name, 'r', encoding='utf-8') as file:
            source = file.read()
            a = radon.raw.analyze (source)
            tloc += (a.loc)
    return("Proyecto: " + project_dir + "\nTotal Archivos .py: " + str(len(python_files)) + " \nLOC Total: " + str(tloc))