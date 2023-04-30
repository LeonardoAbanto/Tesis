import os
# Radon
# https://radon.readthedocs.io/en/latest/api.html#radon.metrics.mi_visit
# https://radon.readthedocs.io/en/latest/intro.html
import radon
import radon.raw, radon.complexity, radon.metrics
from collections import namedtuple


def MetricasPorModulo(project_dir):

    # Lista para almacenar los nombres de los archivos Python
    python_files = []

    # Recorremos el directorio y almacenamos los nombres de los archivos Python
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    # resultados de Radon por modulo
    metricas_modulos = []

    # La clase Metrica contiene: 1. Modulo raw
    class module_metrics:
        def __init__(self, file_name, raw_metrics, halstead, cc, mi, mi_params):
            self.file_name = file_name        
            self.raw_metrics = raw_metrics
            self.halstead = halstead
            self.cc = cc
            self.mi = mi
            self.mi_params = mi_params

    # Recorremos la lista de archivos y calculamos las métricas
    for file_name in python_files:
        # print(f"Archivo: {file_name}", "\n")
        with open(file_name, 'r', encoding='utf-8') as file:
            source = file.read()
            # : LOC, LLOC, SLOC, CMT, MULTI, SINGLE_CMT, BLANK
            raw_metrics = radon.raw.analyze (source)

            # Halstead
            halstead = radon.metrics.h_visit(source)

            # CC
            cc = radon.complexity.cc_visit(source)

            # MI
            mi = radon.metrics.mi_visit(source,False)
            # mi_params: hv, cc, lloc, pcmt
            mi_params = radon.metrics.mi_parameters(source,False)
            
            metrica = module_metrics(os.path.relpath(file_name, project_dir), raw_metrics, halstead, cc, mi, mi_params)
            metricas_modulos.append(metrica)
        
    return metricas_modulos

def MetricasProyecto(metricas_modulos):

    total_files = len(metricas_modulos)
    hv_t = 0
    cc = 0
    lloc = 0
    sloc = 0
    cmt = 0
    pcmt = 0

    for modulo in metricas_modulos:
        sloc += modulo.raw_metrics.sloc
        cmt += modulo.raw_metrics.comments
        hv_t += modulo.mi_params[0]
        cc += modulo.mi_params[1]
        lloc += modulo.mi_params[2]
        pcmt += modulo.mi_params[3]
   
    ave_lloc = lloc/total_files
    ave_cc = cc/total_files
    ave_hv = hv_t/total_files
    ave_pcmt = pcmt/total_files

    mi = radon.metrics.mi_compute(ave_hv,ave_cc,ave_lloc,ave_pcmt)
    Resultado = namedtuple('Resultado', ['mi', 'total_files', 'total_cc', 'total_sloc', 'total_cmt'])
    # return {"ave_cc":ave_cc, "ave_hv":ave_hv, "ave_lloc":ave_lloc, "ave_cmt":ave_pcmt, "mi":mi, "total_files":total_files, "total_cc": cc, "total_sloc":sloc, "total_cmt":cmt, "lloc":lloc}
    return Resultado(mi, total_files, cc, sloc, cmt)

