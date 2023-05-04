from src import metricas_radon
from src import deteccion_ast

proyectos = {1: "dateparser-master", 2: "requests-main", 3: "tqdm-master", 4: "pytest-main", 5: "pyyaml-master",
             6: "eli5-master", 7: "pyjanitor-dev", 8: "pyperf-main", 9: "altair-master", 10: "blaze-master"}


def ReporteTD(i):
    # Ruta del directorio del proyecto
    project_dir = 'C:\\Users\\leona\\Desktop\\TESIS\\ProyectosPython\\' + proyectos[i]
    print('Proyecto: ', str(proyectos[i]))

    # Ejecución Radon
    radon_por_modulo = metricas_radon.MetricasPorModulo(project_dir)
    radon_proyecto = metricas_radon.MetricasProyecto(radon_por_modulo)

    # Información básica:
    print('Lineas de código: ', radon_proyecto.total_sloc, ' / Archivos: ', radon_proyecto.total_files)

    print(radon_proyecto)

    # Indicadores por proyecto a considerar:
    # MI, Duplicacion, Interdependencia, CC (metodos / clases), SLOC, Archivos, AC/EC, DIT, Lack of Cohesion,


ReporteTD(3)
