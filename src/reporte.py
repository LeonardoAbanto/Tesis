import os
from src import metricas_radon
from src import deteccion_smells
import tkinter as tk


def ReporteTD_UI(project_dir):

    # Variables
    background_color = '#D4E4E4'

    # Ejecución funciones
    radon_por_modulo = metricas_radon.MetricasPorModulo(project_dir)
    radon_proyecto = metricas_radon.MetricasProyecto(radon_por_modulo)

    # Creación y configuración de ventana principal
    ventana = tk.Tk()
    ventana.title("Reporte de Deuda Técnica")
    ventana.configure(background=background_color)
    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

    # Frame Info Proyecto
    frame_info_proyecto = tk.Frame(ventana, background='white', borderwidth=2, relief="solid")
    frame_info_proyecto.grid(row=0, column=0, padx=10, pady=10)

    # Nombre del proyecto
    frame_titulo = tk.Frame(frame_info_proyecto)
    frame_titulo.pack()
    nombre_carpeta = os.path.basename(project_dir)
    label1 = tk.Label(frame_titulo, text='Nombre del proyecto:', font=("Arial", 13), background='white')
    label1.pack(side=tk.LEFT)
    nombre_proyecto = tk.Label(frame_titulo, text=nombre_carpeta, font=("Arial", 13, "bold"), background='white')
    nombre_proyecto.pack(side=tk.LEFT)

    # Tamaño de proyecto
    sloc = tk.Label(frame_info_proyecto, text=('Líneas de codigo: '+str(radon_proyecto.total_sloc)),
                    font=("Arial", 13), background='white')
    sloc.pack()
    files = tk.Label(frame_info_proyecto, text=('Total de archivos python: '+str(radon_proyecto.total_files)),
                     font=("Arial", 13), background='white')
    files.pack()

    # Frame Indicadores
    frame_indicadores = tk.Frame(ventana, background='white', borderwidth=2, relief="solid")
    frame_indicadores.grid(row=1, column=0, padx=10, pady=10)

    # Complejidad (temporal):
    complexity = tk.Label(frame_indicadores, text=('Complejidad total: '+str(radon_proyecto.total_cc)),
                          font=("Arial", 13), background='white')
    complexity.pack()


    grupo_2 = tk.Frame(ventana, background=background_color)
    grupo_2.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)



    # Crear un widget de desplazamiento vertical
    scrollbar = tk.Scrollbar(ventana)
    scrollbar.grid(row=2, column=1, sticky=tk.N+tk.S)

    # Crear un widget de texto para información de smells
    text_widget = tk.Text(grupo_2, yscrollcommand=scrollbar.set)
    text_widget.pack()

    # Asociar la barra de desplazamiento al widget de texto
    scrollbar.config(command=text_widget.yview)











    # MI:
    text_widget.insert(tk.END, 'MI: ' + str(radon_proyecto.mi) + '\n')

    # CMT
    text_widget.insert(tk.END, 'CMT: ' + str(radon_proyecto.total_cmt / radon_proyecto.total_sloc) + '\n')

    # % CC>60
    cc_modulo_count = 0
    for modulo in radon_por_modulo:
        if modulo.mi_params[1] > 60:
            cc_modulo_count += 1
    pct_cc_modulos = cc_modulo_count/len(radon_por_modulo)
    text_widget.insert(tk.END, 'Módulos con complejidad > 60: ' + "%.2f%%" % (100 * pct_cc_modulos) + '\n')

    # % CC>8
    function_count = 0
    cc_function_count = 0
    for modulo in radon_por_modulo:
        for func in modulo.cc:
            function_count += 1
            if func.complexity > 8:
                cc_function_count += 1
    pct_cc_metodos = cc_function_count / function_count
    text_widget.insert(tk.END, 'Métodos con complejidad > 8: ' + "%.2f%%" % (100 * pct_cc_metodos) + '\n')

    # Módulos con bajo MI
    low_mi_encontrado = False
    text_widget.insert(tk.END, 'Módulos con baja mantenibilidad:\n')
    for modulo in radon_por_modulo:
        if 20 > modulo.mi > 0:
            text_widget.insert(tk.END, modulo.file_name + ' - MI: ' + str(round(modulo.mi, 2)) + ', CC: ' +
                               modulo.mi_params[1] + ', %COM: ' + "%.2f%%" % modulo.mi_params[3] +
                               ', LOC: ' + modulo.mi_params[2] + ', HV: ' + str(round(modulo.mi_params[0], 2)) + '\n')
            low_mi_encontrado = True
    if not low_mi_encontrado:
        text_widget.insert(tk.END, '--\n')

    # Code Smells (AST)
    archivos = []
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                archivos.append(os.path.join(root, file))

    smells_array = []
    total_count = {}
    for file in archivos:
        file_smells = deteccion_smells.detectar_smells(file)
        count = file_smells['count']
        smells = file_smells['str']
        if smells:
            smells_array.append('')
            smells_array.append("Detecciones en archivo: " + str(file))
            for smell in smells:
                smells_array.append(smell)
        for key, value in count.items():
            total_count[key] = total_count.get(key, 0) + value

    if total_count:
        text_widget.insert(tk.END, 'Total de smells encontrados:\n')
        for key, value in total_count.items():
            if value > 0:
                text_widget.insert(tk.END, key + ' - ' + str(value) + '\n')

    text_widget.insert(tk.END, '\n'.join(smells_array))

    ventana.mainloop()


def ReporteTD(project_dir):
    # Ruta del directorio del proyecto
    print('Proyecto: ', project_dir)

    # Ejecución Radon
    radon_por_modulo = metricas_radon.MetricasPorModulo(project_dir)
    radon_proyecto = metricas_radon.MetricasProyecto(radon_por_modulo)

    # Información básica:
    print('Lineas de código: ', radon_proyecto.total_sloc, ' / Archivos: ', radon_proyecto.total_files)

    print('Complejidad total: ', radon_proyecto.total_cc)

    # MI:
    print()
    mi = radon_proyecto.mi
    print(rating_MI(mi))
    print()

    # CMT
    cmt = radon_proyecto.total_cmt / radon_proyecto.total_sloc
    print(rating_cmt(cmt))

    # % CC>60
    cc_modulo_count = 0
    for modulo in radon_por_modulo:
        if modulo.mi_params[1] > 60:
            cc_modulo_count += 1
    pct_cc_modulos = cc_modulo_count/len(radon_por_modulo)
    print('Módulos con complejidad > 60: ', "%.2f%%" % (100 * pct_cc_modulos), ' - Nivel ',
          rating_cc(pct_cc_modulos))

    # % CC>8
    function_count = 0
    cc_function_count = 0
    for modulo in radon_por_modulo:
        for func in modulo.cc:
            function_count += 1
            if func.complexity > 8:
                cc_function_count += 1
    pct_cc_metodos = cc_function_count / function_count
    print('Métodos con complejidad > 8: ', "%.2f%%" % (100 * pct_cc_metodos), ' - Nivel ',
          rating_cc(pct_cc_metodos))

    # Módulos con bajo MI
    print()
    low_mi_encontrado = False
    print('Módulos con baja mantenibilidad:')
    for modulo in radon_por_modulo:
        if 20 > modulo.mi > 0:
            print(
                modulo.file_name, ' - MI: ', str(round(modulo.mi, 2)), ', CC: ', modulo.mi_params[1], ', %COM: ',
                "%.2f%%" % modulo.mi_params[3], ', LOC: ', modulo.mi_params[2], ', HV: ', round(modulo.mi_params[0], 2)
            )
            low_mi_encontrado = True
    if not low_mi_encontrado:
        print('--')

    # Indicadores por proyecto a considerar:
    # MI, Duplicacion, Interdependencia, CC (metodos / clases), SLOC, Archivos, AC/EC, DIT, Lack of Cohesion,

    # Code Smells (AST)
    archivos = []
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                archivos.append(os.path.join(root, file))

    # Obtener smells desde función, almacenar cuentas totales y ocurrencias
    smells_array = []
    total_count = {}
    for file in archivos:
        file_smells = deteccion_smells.detectar_smells(file)
        count = file_smells['count']
        smells = file_smells['str']
        if smells:
            smells_array.append('')
            smells_array.append("Detecciones en archivo: " + str(file))
            for smell in smells:
                smells_array.append(smell)
        for key, value in count.items():
            total_count[key] = total_count.get(key, 0) + value

    # Imprimir totales por smell
    print()
    if total_count:
        print('Total de smells encontrados:')
        for key, value in total_count.items():
            if value > 0:
                print(key+' - '+str(value))

    print('\n'.join(smells_array))


def rating_MI(mi):
    if mi < 10:
        nivel = 'baja'
    elif mi < 20:
        nivel = 'media'
    else:
        nivel = 'alta'
    return ''.join(('Índice de mantenibilidad: ', str(round(mi, 2)), ' - Mantenibilidad ', nivel))


def rating_cmt(cmt):
    if cmt >= 0.3:
        nivel = 'Verde'
    elif cmt >= 0.2:
        nivel = 'Amarillo'
    else:
        nivel = 'Rojo'
    return ''.join(('Densidad de comentarios: ', "%.2f%%" % (100 * cmt), ' - Nivel ', nivel))


def rating_cc(cc):
    if cc <= 0.1:
        nivel = 'Verde'
    elif cc <= 0.15:
        nivel = 'Amarillo'
    else:
        nivel = 'Rojo'
    return nivel
