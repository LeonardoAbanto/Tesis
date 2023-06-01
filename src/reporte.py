import os
from src import metricas_radon
from src import deteccion_smells
import tkinter as tk


def ReporteTD_UI(project_dir):
    # Crear una instancia de la ventana principal
    ventana = tk.Tk()

    # Ruta del directorio del proyecto
    proyecto_label = tk.Label(ventana, text='Proyecto: ' + project_dir)
    proyecto_label.pack()

    # Ejecución Radon
    radon_por_modulo = metricas_radon.MetricasPorModulo(project_dir)
    radon_proyecto = metricas_radon.MetricasProyecto(radon_por_modulo)

    # Información básica:
    sloc_label = tk.Label(ventana, text='Lineas de código: ' + str(radon_proyecto.total_sloc) + ' / Archivos: ' + str(radon_proyecto.total_files))
    sloc_label.pack()

    cc_label = tk.Label(ventana, text='Complejidad total: ' + str(radon_proyecto.total_cc))
    cc_label.pack()

    # MI:
    mi_label = tk.Label(ventana, text='MI: ' + str(radon_proyecto.mi))
    mi_label.pack()

    # CMT
    cmt_label = tk.Label(ventana, text='CMT: ' + str(radon_proyecto.total_cmt / radon_proyecto.total_sloc))
    cmt_label.pack()

    # % CC>60
    cc_modulo_count = 0
    for modulo in radon_por_modulo:
        if modulo.mi_params[1] > 60:
            cc_modulo_count += 1
    pct_cc_modulos = cc_modulo_count/len(radon_por_modulo)
    pct_cc_modulos_label = tk.Label(ventana, text='Módulos con complejidad > 60: ' + "%.2f%%" % (100 * pct_cc_modulos))
    pct_cc_modulos_label.pack()

    # % CC>8
    function_count = 0
    cc_function_count = 0
    for modulo in radon_por_modulo:
        for func in modulo.cc:
            function_count += 1
            if func.complexity > 8:
                cc_function_count += 1
    pct_cc_metodos = cc_function_count / function_count
    pct_cc_metodos_label = tk.Label(ventana, text='Métodos con complejidad > 8: ' + "%.2f%%" % (100 * pct_cc_metodos))
    pct_cc_metodos_label.pack()

    # Módulos con bajo MI
    low_mi_encontrado = False
    low_mi_label = tk.Label(ventana, text='Módulos con baja mantenibilidad:')
    low_mi_label.pack()
    for modulo in radon_por_modulo:
        if 20 > modulo.mi > 0:
            modulo_label = tk.Label(ventana, text=modulo.file_name + ' - MI: ' + str(round(modulo.mi, 2)) + ', CC: ' +
                                           modulo.mi_params[1] + ', %COM: ' + "%.2f%%" % modulo.mi_params[3] +
                                           ', LOC: ' + modulo.mi_params[2] + ', HV: ' + round(modulo.mi_params[0], 2))
            modulo_label.pack()
            low_mi_encontrado = True
    if not low_mi_encontrado:
        no_low_mi_label = tk.Label(ventana, text='--')
        no_low_mi_label.pack()

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
        smells_totals_label = tk.Label(ventana, text='Total de smells encontrados:')
        smells_totals_label.pack()
        for key, value in total_count.items():
            if value > 0:
                smells_totals = tk.Label(ventana, text=key+' - '+str(value))
                smells_totals.pack()

    smells_array_label = tk.Label(ventana, text='\n'.join(smells_array))
    smells_array_label.pack()

    # Ejecutar el bucle principal de la aplicación
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
