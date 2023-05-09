from src import metricas_radon

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
    encontrado = False
    print('Módulos con baja mantenibilidad:')
    for modulo in radon_por_modulo:
        if 20 > modulo.mi > 0:
            print(modulo.file_name, ' - MI: ', str(modulo.mi))
            encontrado = True
    if not encontrado:
        print('--')

    print()
    # Indicadores por proyecto a considerar:
    # MI, Duplicacion, Interdependencia, CC (metodos / clases), SLOC, Archivos, AC/EC, DIT, Lack of Cohesion,
