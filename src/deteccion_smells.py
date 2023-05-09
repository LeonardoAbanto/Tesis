from src import metricas_ast
import ast


def detectar_smells(file):
    # Leer archivo
    with open(file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Parse archivo con árbol AST
    tree = ast.parse(code)
    visited = metricas_ast.MetricVisitor()
    visited.visit(tree)

    # Llamado a funciones de detección según métricas de árbol visitado
    detectar_LC(visited)
    detectar_LPL(visited)
    detectar_LM(visited)
    detectar_LMC(visited)
    detectar_LSC(visited)
    detectar_LBCL(visited)
    detectar_UEH(visited)
    detectar_LLF(visited)
    detectar_CLC(visited)
    detectar_LEC(visited)
    detectar_LTCE(visited)

    #
    # print(f"{visited.loops} loops encontrados")
    # print(f"{visited.conditionals} condicionales encontrados")
    # print(f"{visited.exceptions} cláusulas de excepción encontradas")
    # print(f"{visited.empty_exceptions} cláusulas de excepción vacias")


def detectar_LC(visited: metricas_ast.MetricVisitor):
    # Long Class: LOC >= 200 o #Métodos + # Atributos > 40
    for cls in visited.classes:
        if cls['total_lines'] >= 200:
            print(
                f"Code Smell: Clase Larga - "
                f"La clase '{cls['name']}' en la línea {cls['lineno']} tiene {cls['total_lines']} líneas de código")
        elif cls['methods']+cls['attributes'] > 40:
            print(
                f"Code Smell: Clase Larga - "
                f"La clase '{cls['name']}' en la línea {cls['lineno']} tiene {cls['methods']} métodos y "
                f"{cls['attributes']} atributos")


def detectar_LPL(visited: metricas_ast.MetricVisitor):
    # Long Parameter List: #parámetros >= 5 por función
    for func in visited.functions:
        if len(func['params']) >= 5:
            print(
                f"Code Smell: Lista de Parámetros Larga - "
                f"La función '{func['name']}' en la línea {func['lineno']} tiene 5 o más parámetros: {func['params']}")


def detectar_LM(visited: metricas_ast.MetricVisitor):
    # Long Method: LOC método >= 100
    for func in visited.functions:
        if func['total_lines'] >= 100:
            print(
                f"Code Smell: Método Largo - "
                f"El método '{func['name']}' en la línea {func['lineno']} tiene más de 100 líneas de código:"
                f" {func['total_lines']} líneas")


def detectar_LMC(visited: metricas_ast.MetricVisitor):
    # NYI
    return()


def detectar_LSC(visited: metricas_ast.MetricVisitor):
    # NYI
    return()


def detectar_LBCL(visited: metricas_ast.MetricVisitor):
    # NYI
    return()


def detectar_UEH(visited: metricas_ast.MetricVisitor):
    # NYI
    return()


def detectar_LLF(visited: metricas_ast.MetricVisitor):
    # Long Lambda Function: NOC >= 80 para cada expresión
    for expr in visited.long_expressions:
        print(
            f"Code Smell: Función Lambda Larga - "
            f"La expresión en la línea {expr['lineno']} tiene más de 80 caracteres "
            f"({expr['line_length']} caracteres encontrados)")

def detectar_CLC(visited: metricas_ast.MetricVisitor):
    # NYI
    return()


def detectar_LEC(visited: metricas_ast.MetricVisitor):
    # NYI
    return()


def detectar_LTCE(visited: metricas_ast.MetricVisitor):
    # Long Ternary Conditional Expression: NOC >= 40
    for expr in visited.long_ternary:
        print(
            f"Code Smell: Expresión Condicional Ternaria Larga - "
            f"La expresión ternaria en la línea {expr['lineno']} tiene más de 40 caracteres: ({expr['line_length']}"
            f" caracteres encontrados)")

