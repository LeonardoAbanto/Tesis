from app import metricas_radon

project_dir = 'C:\\Users\\leona\\Desktop\\TESIS\\ProyectosPython\\eli5-master'
print(project_dir)

metricas_por_modulo = metricas_radon.MetricasPorModulo(project_dir)
metricas_proyecto = metricas_radon.MetricasProyecto(metricas_por_modulo)

informacion_basica = {"sloc": metricas_proyecto.total_sloc, "files": metricas_proyecto.total_files}
print("Información básica: " + str(informacion_basica))
print(metricas_proyecto.mi)

for modulo in metricas_por_modulo:
    print("Archivo: " + str(modulo.file_name) + " MI: " + str(modulo.mi))
    print(modulo.raw_metrics)
    print(modulo.mi_params)
    print("")

# archivo = 5
# print(metricas_por_modulo[archivo].file_name)
# print(type(metricas_por_modulo[archivo].raw_metrics.sloc))
# print(type(metricas_por_modulo[archivo].halstead))
# print(type(metricas_por_modulo[archivo].cc))
# print(type(metricas_por_modulo[archivo].mi))
# print(metricas_por_modulo[5].mi_params)