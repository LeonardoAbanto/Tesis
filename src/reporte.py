import os
from src import metricas_radon
from src import deteccion_smells


def ReporteTD(i):
    # Ruta del directorio del proyecto
    project_dir = 'C:\\Users\\leona\\Desktop\\TESIS\\ProyectosPython\\' + i
    print('Proyecto: ', i)

    # Ejecución Radon
    radon_por_modulo = metricas_radon.MetricasPorModulo(project_dir)
    radon_proyecto = metricas_radon.MetricasProyecto(radon_por_modulo)

    # Información básica:
    print('Lineas de código: ', radon_proyecto.total_sloc, ' / Archivos: ', radon_proyecto.total_files)
    print('% de comentarios: ', "%.2f%%" % (100 * radon_proyecto.total_cmt/radon_proyecto.total_sloc))

    # MI:
    print()
    mi = radon_proyecto.mi
    if mi < 10:
        print('Índice de mantenibilidad: ', str(round(radon_proyecto.mi, 2)), ' - Mantenibilidad baja')
    elif mi < 20:
        print('Índice de mantenibilidad: ', str(round(radon_proyecto.mi, 2)), ' - Mantenibilidad media')
    else:
        print('Índice de mantenibilidad: ', str(round(radon_proyecto.mi, 2)), ' - Mantenibilidad alta')

    # Módulos con bajo MI
    print()
    low_mi_encontrado = False
    print('Módulos con baja mantenibilidad:')
    for modulo in radon_por_modulo:
        if 20 > modulo.mi > 0:
            print(modulo.file_name, ' - MI: ', str(modulo.mi))
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

    smells_array = []
    total_count = {}
    for file in archivos:
        file_smells = deteccion_smells.detectar_smells(file)
        count = file_smells['count']
        smells = file_smells['str']
        if smells:
            smells_array.append('')
            smells_array.append("Análisis de archivo: " + str(file))
            for smell in smells:
                smells_array.append(smell)
        for key, value in count.items():
            total_count[key] = total_count.get(key, 0) + value

    print()
    if total_count:
        print('Total de smells encontrados:')
        for key, value in total_count.items():
            print(key+' - '+str(value))

    print('\n'.join(smells_array))

