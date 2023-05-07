# from src import metricas_ast

project_dir = 'C:\\Users\\leona\\Desktop\\TESIS\\ProyectosPython\\eli5-master'
print(project_dir)

# metricas_ast.test(project_dir)
# metricas_ast.test_astor(project_dir)

import ast


class MetricCounter(ast.NodeVisitor):
    def __init__(self):
        self.loops = 0
        self.conditionals = 0
        self.functions = []
        self.classes = []
        self.exceptions = 0
        self.empty_exceptions = 0

    def visit_FunctionDef(self, node):
        self.functions.append({
            'name': node.name,
            'lineno': node.lineno,
            'params': [arg.arg for arg in node.args.args],
            'total_lines': node.end_lineno - node.lineno + 1
        })
        self.generic_visit(node)

    def visit_For(self, node):
        self.loops += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.loops += 1
        self.generic_visit(node)

    def visit_If(self, node):
        self.conditionals += 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.conditionals += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.exceptions += 1
        self.generic_visit(node)

    def visit_TryFinally(self, node):
        self.exceptions += 1
        self.generic_visit(node)

    def visit_TryExcept(self, node):
        self.exceptions += 1
        if not node.body:
            self.empty_exceptions += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_dict = {
            'name': node.name,
            'lineno': node.lineno,
            'methods': 0,
            'methods_list': [],
            'attributes': 0,
            'total_lines': node.end_lineno - node.lineno + 1
        }

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                class_dict['methods'] += 1
                method_dict = {
                    'name': item.name,
                    'total_lines': item.end_lineno - item.lineno + 1
                }
                class_dict['methods_list'].append(method_dict)
            elif isinstance(item, ast.Assign):
                class_dict['attributes'] += 1

        self.classes.append(class_dict)
        self.generic_visit(node)


def count_metrics(file_path):
    with open(file_path, 'r') as f:
        code = f.read()

    tree = ast.parse(code)
    counter = MetricCounter()
    counter.visit(tree)

    for func in counter.functions:
        if len(func['params']) > 2:
            print(
                f"La función '{func['name']}' en la línea {func['lineno']} tiene más de 2 parámetros: {func['params']}")

    for cls in counter.classes:
        print(
            f"La clase '{cls['name']}' en la línea {cls['lineno']} tiene {cls['methods']} métodos, {cls['attributes']} "
            f"atributos y {cls['total_lines']} líneas de código")
        print(f"La clase '{cls['name']}' tiene los siguientes métodos:")
        for mtd in cls['methods_list']:
            print(f"El método '{mtd['name']}' tiene '{mtd['total_lines']}' líneas de código")

    print(f"{counter.loops} loops encontrados")
    print(f"{counter.conditionals} condicionales encontrados")
    print(f"{len(counter.functions)} funciones encontradas")
    print(f"{len(counter.classes)} clases encontradas")
    print(f"{counter.exceptions} cláusulas de excepción encontradas")
    print(f"{counter.empty_exceptions} cláusulas de excepción vacias")


count_metrics('C:\\Users\\leona\\Desktop\\TESIS\\ProyectosPython\\eli5-master\\tests\\test_sklearn_transform.py')
