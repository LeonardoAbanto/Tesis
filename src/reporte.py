import os
from src import metricas_radon
from src import deteccion_smells
import tkinter as tk


def ReporteTD_UI(project_dir):
    # Variables
    background_color = '#D4E4E4'
    ratings_colores = {'A': '#00FF00', 'B': '#FFFF00', 'C': '#FF0000'}

    # Ejecución funciones
    radon_por_modulo = metricas_radon.MetricasPorModulo(project_dir)
    radon_proyecto = metricas_radon.MetricasProyecto(radon_por_modulo)

    # Creación y configuración de ventana principal
    ventana = tk.Tk()
    ventana.minsize(400,400)
    ventana.title("Reporte de Deuda Técnica")
    ventana.configure(background=background_color)
    ventana.grid_rowconfigure(1, weight=1)
    ventana.grid_rowconfigure(2, weight=1)
    ventana.grid_rowconfigure(3, weight=1)
    ventana.grid_rowconfigure(4, weight=1)
    # ventana.grid_columnconfigure(0, weight=1)

    # Frame 1
    frame_1 = tk.Frame(ventana, background=background_color)
    frame_1.grid(row=1, column=0, sticky="nw")

    # Frame Info Proyecto
    frame_info_proyecto = tk.Frame(frame_1, background='white', borderwidth=2, relief="solid")
    frame_info_proyecto.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
    # Nombre del proyecto
    frame_titulo = tk.Frame(frame_info_proyecto)
    frame_titulo.grid(row=1, column=0, sticky="w")
    nombre_carpeta = os.path.basename(project_dir)
    label_titulo = tk.Label(frame_titulo, text='Nombre del proyecto:', font=("Arial", 15), background='white')
    label_titulo.pack(side=tk.LEFT)
    nombre_proyecto = tk.Label(frame_titulo, text=nombre_carpeta, font=("Arial", 15, "bold"), background='white')
    nombre_proyecto.pack(side=tk.LEFT)
    # Tamaño de proyecto
    frame_sloc = tk.Frame(frame_info_proyecto)
    frame_sloc.grid(row=2, column=0, sticky="w")
    label_sloc = tk.Label(frame_sloc, text='Líneas de codigo:', font=("Arial", 12), background='white')
    label_sloc.pack(side=tk.LEFT)
    sloc = tk.Label(frame_sloc, text=str(radon_proyecto.total_sloc), font=("Arial", 12, "bold"), background='white')
    sloc.pack(side=tk.LEFT)
    frame_files = tk.Frame(frame_info_proyecto)
    frame_files.grid(row=3, column=0, sticky="w")
    label_files = tk.Label(frame_files, text='Total de archivos Python:', font=("Arial", 12), background='white')
    label_files.pack(side=tk.LEFT)
    files = tk.Label(frame_files, text=str(radon_proyecto.total_files), font=("Arial", 12, "bold"), background='white')
    files.pack(side=tk.LEFT)

    # Frame Indicadores
    frame_indicadores = tk.Frame(frame_1, background='white', borderwidth=2, relief="solid")
    frame_indicadores.grid(row=1, column=2, padx=10, pady=10, sticky="nw")
    titulo_indicadores = tk.Label(frame_indicadores, text='Indicadores del proyecto:', font=("Arial", 14, "bold"),
                                  background='white')
    titulo_indicadores.grid(row=0, column=0, sticky="w", pady=2, padx=2)
    # Complejidad (temporal):
    complexity = tk.Label(frame_indicadores, text=('Complejidad total: ' + str(radon_proyecto.total_cc)),
                          font=("Arial", 12), background='white')
    complexity.grid(row=1, column=0, sticky="w", pady=2, padx=2)
    # MI:
    frame_mi = tk.Frame(frame_indicadores)
    frame_mi.grid(row=2, column=0, sticky="w", pady=2, padx=2)
    label_mi = tk.Label(frame_mi, text='Indice de Mantenibilidad:', font=("Arial", 12), background='white')
    label_mi.pack(side=tk.LEFT)
    mi_proyecto = radon_proyecto.mi
    rating_mi = rating_MI(mi_proyecto)
    mi = tk.Label(frame_mi, text=str(round(mi_proyecto, 2)), font=("Arial", 12), background=ratings_colores[rating_mi])
    mi.pack(side=tk.LEFT)
    # CMT:
    frame_cmt = tk.Frame(frame_indicadores)
    frame_cmt.grid(row=3, column=0, sticky="w", pady=2, padx=2)
    label_cmt = tk.Label(frame_cmt, text='Comentarios:', font=("Arial", 12), background='white')
    label_cmt.pack(side=tk.LEFT)
    cmt_pct = radon_proyecto.total_cmt / radon_proyecto.total_sloc
    rating_cmt = rating_CMT(cmt_pct)
    cmt = tk.Label(frame_cmt, text="%.2f%%" % (100 * cmt_pct), font=("Arial", 12),
                   background=ratings_colores[rating_cmt])
    cmt.pack(side=tk.LEFT)
    # % Módulos CC>60
    frame_cc_mod = tk.Frame(frame_indicadores)
    frame_cc_mod.grid(row=4, column=0, sticky="w", pady=2, padx=2)
    label_cc_mod = tk.Label(frame_cc_mod, text='Módulos con alta complejidad:', font=("Arial", 12), background='white')
    label_cc_mod.pack(side=tk.LEFT)
    cc_modulo_count = 0
    for modulo in radon_por_modulo:
        if modulo.mi_params[1] > 60:
            cc_modulo_count += 1
    pct_cc_modulos = cc_modulo_count / len(radon_por_modulo)
    rating_cc_mod = rating_cc(pct_cc_modulos)
    cc_mod = tk.Label(frame_cc_mod, text="%.2f%%" % (100 * pct_cc_modulos), font=("Arial", 12),
                      background=ratings_colores[rating_cc_mod])
    cc_mod.pack(side=tk.LEFT)
    # % Módulos CC>60
    frame_cc_met = tk.Frame(frame_indicadores)
    frame_cc_met.grid(row=5, column=0, sticky="w", pady=2, padx=2)
    label_cc_met = tk.Label(frame_cc_met, text='Métodos con alta complejidad:', font=("Arial", 12), background='white')
    label_cc_met.pack(side=tk.LEFT)
    function_count = 0
    cc_function_count = 0
    for modulo in radon_por_modulo:
        for func in modulo.cc:
            function_count += 1
            if func.complexity > 8:
                cc_function_count += 1
    pct_cc_metodos = cc_function_count / function_count
    rating_cc_met = rating_cc(pct_cc_metodos)
    cc_met = tk.Label(frame_cc_met, text="%.2f%%" % (100 * pct_cc_metodos), font=("Arial", 12),
                      background=ratings_colores[rating_cc_met])
    cc_met.pack(side=tk.LEFT)

    # Frame Módulos MI
    frame_low_mi = tk.Frame(ventana, background='white', borderwidth=2, relief="solid")
    frame_low_mi.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
    # Módulos con bajo MI
    low_mi_encontrado = False
    titulo = tk.Label(frame_low_mi, text='Módulos con baja mantenibilidad identificados:',
                      font=("Arial", 14, "bold"), background='white')
    titulo.grid(sticky="w")
    for modulo in radon_por_modulo:
        if 20 > modulo.mi > 0:
            low_mi = tk.Label(frame_low_mi,
                              text=(nombre_carpeta+'\\'+os.path.relpath(modulo.file_name, project_dir) +
                                    ' - MI: ' + str(round(modulo.mi, 2)) + ', Líneas de Código: '
                                    + str(modulo.mi_params[2])),
                              font=("Arial", 13), background='white')
            low_mi.grid(sticky="w")
            low_mi_encontrado = True
    if not low_mi_encontrado:
        not_found = tk.Label(frame_low_mi, text='-', font=("Arial", 12), background='white')
        not_found.grid(sticky="w")

    # Frames smells
    frame_smells_resumido = tk.Frame(ventana, background='white', borderwidth=2, relief="solid")
    frame_smells_resumido.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

    frame_smells_detalle = tk.Frame(ventana, background=background_color)
    frame_smells_detalle.grid(row=4, column=0, padx=10, pady=10, sticky="nw")

    # Crear un widget de desplazamiento vertical
    scrollbar_y = tk.Scrollbar(frame_smells_detalle, orient=tk.VERTICAL)
    scrollbar_y.grid(row=0, column=1, sticky=tk.NS)

    # Crear un widget de desplazamiento horizontal
    scrollbar_x = tk.Scrollbar(frame_smells_detalle, orient=tk.HORIZONTAL)
    scrollbar_x.grid(row=1, column=0, sticky=tk.EW)

    # Crear un widget de texto para información de smells
    text_widget = tk.Text(frame_smells_detalle, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set,
                          font=("Arial", 13), background='white', width=70, height=10, wrap="none")
    text_widget.grid(row=0, column=0, sticky="nsew")

    frame_smells_detalle.grid_rowconfigure(0, weight=1)
    frame_smells_detalle.grid_columnconfigure(0, weight=1)

    scrollbar_y.config(command=text_widget.yview)
    scrollbar_x.config(command=text_widget.xview)

    # Configurar el sistema de rejilla del marco
    frame_smells_detalle.grid_rowconfigure(0, weight=1)
    frame_smells_detalle.grid_rowconfigure(1, weight=1)
    frame_smells_detalle.grid_columnconfigure(0, weight=1)
    frame_smells_detalle.grid_columnconfigure(1, weight=1)

    # Code Smells
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
            smells_array.append("Archivo: " + str(file))
            for smell in smells:
                smells_array.append(smell)
            smells_array.append('')
        for key, value in count.items():
            total_count[key] = total_count.get(key, 0) + value

    # Contadores Smells
    if total_count:
        resumen_smells_titulo = tk.Label(frame_smells_resumido, text='Code Smells detectados:',
                                         font=("Arial", 14, "bold"), background='white')
        resumen_smells_titulo.grid(column=0, sticky="w")
        for key, value in total_count.items():
            if value > 0:
                smells_contador = tk.Label(frame_smells_resumido, text=(key + ' - ' + str(value)), font=("Arial", 12),
                                           background='white')
                smells_contador.grid(column=0, sticky="w")

    text_widget.insert(tk.END, '\n'.join(smells_array))
    text_widget.config(state="disabled")
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
    print(rating_MI_texto(mi))
    print()

    # CMT
    cmt = radon_proyecto.total_cmt / radon_proyecto.total_sloc
    print(rating_cmt_texto(cmt))

    # % CC>60
    cc_modulo_count = 0
    for modulo in radon_por_modulo:
        if modulo.mi_params[1] > 60:
            cc_modulo_count += 1
    pct_cc_modulos = cc_modulo_count / len(radon_por_modulo)
    print('Módulos con complejidad > 60: ', "%.2f%%" % (100 * pct_cc_modulos), ' - Nivel ',
          rating_cc_texto(pct_cc_modulos))

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
          rating_cc_texto(pct_cc_metodos))

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
                print(key + ' - ' + str(value))

    print('\n'.join(smells_array))


def rating_MI(mi):
    if mi < 10:
        return 'C'
    elif mi < 20:
        return 'B'
    else:
        return 'A'


def rating_MI_texto(mi):
    if mi < 10:
        nivel = 'baja'
    elif mi < 20:
        nivel = 'media'
    else:
        nivel = 'alta'
    return ''.join(('Índice de mantenibilidad: ', str(round(mi, 2)), ' - Mantenibilidad ', nivel))


def rating_CMT(cmt):
    if cmt >= 0.3:
        return 'A'
    elif cmt >= 0.2:
        return 'B'
    else:
        return 'C'


def rating_cmt_texto(cmt):
    if cmt >= 0.3:
        nivel = 'Verde'
    elif cmt >= 0.2:
        nivel = 'Amarillo'
    else:
        nivel = 'Rojo'
    return ''.join(('Densidad de comentarios: ', "%.2f%%" % (100 * cmt), ' - Nivel ', nivel))


def rating_cc_texto(cc):
    if cc <= 0.1:
        nivel = 'Verde'
    elif cc <= 0.15:
        nivel = 'Amarillo'
    else:
        nivel = 'Rojo'
    return nivel


def rating_cc(cc):
    if cc <= 0.1:
        return 'A'
    elif cc <= 0.15:
        return 'B'
    else:
        return 'C'
