from src import metricas_radon

proyectos = {1: "dateparser-master", 2: "requests-main", 3: "tqdm-master", 4: "pytest-main", 5: "pyyaml-master",
             6: "eli5-master", 7: "pyjanitor-dev", 8: "pyperf-main", 9: "altair-master", 10: "blaze-master"}

# Ruta del directorio del proyecto
project_dir = 'C:\\Users\\leona\\Desktop\\TESIS\\ProyectosPython\\' + proyectos[6]
print(project_dir)

metricas_por_modulo = metricas_radon.MetricasPorModulo(project_dir)
metricas_proyecto = metricas_radon.MetricasProyecto(metricas_por_modulo)
informacion_basica = {"sloc": metricas_proyecto.total_sloc, "files": metricas_proyecto.total_files}

print(informacion_basica)
print(metricas_proyecto)

# Indicadores por proyecto a considerar:
# MI, Duplicacion, Interdependencia, CC (metodos / clases), SLOC, Archivos, AC/EC, DIT, Lack of Cohesion,
