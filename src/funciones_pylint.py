import pylint.lint
import os
# https://pylint.pycqa.org/en/v2.13.9/user_guide/run.html


def test(project_dir):
    # Lista para almacenar los nombres de los archivos Python
    python_files = []

    # Recorremos el directorio y almacenamos los nombres de los archivos Python
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    for file_name in python_files:
        # Ejecutando pylint para cada archivo (configuración default por ahora)

        # pylint_opts = ['--disable=line-too-long', file_name]
        # pylint.lint.Run(pylint_opts)

        results = pylint.lint.Run(['--disable=all --enable=duplicate-code', file_name])
        for message in results.linter.stats['duplicated_lines']:
            print(f'Fragmento duplicado encontrado: {message}')


test('C:\\Users\\leona\\Desktop\\TESIS\\ProyectosPython\\dateparser-master')
