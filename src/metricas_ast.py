import ast
import os
import astor


def test(project_dir):
    # Lista para almacenar los nombres de los archivos Python
    python_files = []

    # Recorremos el directorio y almacenamos los nombres de los archivos Python
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    for file_name in python_files:
        # Lee el contenido del archivo de Python
        with open(file_name, 'r') as f:
            source_code = f.read()

        # Analiza el código fuente en un árbol de sintaxis abstracta (AST)
        ast_tree = ast.parse(source_code)

        # Recorre el árbol de sintaxis abstracta (AST) en busca de definiciones de funciones
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                print(f"Nombre de la función: {node.name}")
                print(f"Número de líneas de la función: {node.body[-1].lineno - node.body[0].lineno + 1}")
                print(node.args.lineno)
                print(node.returns)
            elif isinstance(node, ast.ClassDef):
                print(f"Nombre de la clase: {node.name}")
                print(f"Número de líneas de la clase: {node.body[-1].lineno - node.body[0].lineno + 1}")
