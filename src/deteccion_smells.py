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
    all_smells = []
    all_smells.extend(detectar_LC(visited))
    all_smells.extend(detectar_LPL(visited))
    all_smells.extend(detectar_LM(visited))
    all_smells.extend(detectar_LMC(visited))
    all_smells.extend(detectar_LSC(visited))
    all_smells.extend(detectar_LBCL(visited))
    all_smells.extend(detectar_UEH(visited))
    all_smells.extend(detectar_LLF(visited))
    all_smells.extend(detectar_CLC(visited))
    all_smells.extend(detectar_LEC(visited))
    all_smells.extend(detectar_LTCE(visited))

    return all_smells
    #
    # print(f"{visited.loops} loops encontrados")
    # print(f"{visited.conditionals} condicionales encontrados")
    # print(f"{visited.exceptions} cláusulas de excepción encontradas")
    # print(f"{visited.empty_exceptions} cláusulas de excepción vacias")


def detectar_LC(visited: metricas_ast.MetricVisitor):
    # Long Class: LOC >= 200 o #Métodos + # Atributos > 40
    smells = []
    for cls in visited.classes:
        if cls['total_lines'] >= 200:
            smells.append(
                f"Code Smell: Clase Larga - "
                f"La clase '{cls['name']}' en la línea {cls['lineno']} tiene {cls['total_lines']} líneas de código")
        elif cls['methods']+cls['attributes'] > 40:
            smells.append(
                f"Code Smell: Clase Larga - "
                f"La clase '{cls['name']}' en la línea {cls['lineno']} tiene {cls['methods']} métodos y "
                f"{cls['attributes']} atributos")
    return smells


def detectar_LPL(visited: metricas_ast.MetricVisitor):
    # Long Parameter List: #parámetros >= 5 por función
    smells = []
    for func in visited.functions:
        if len(func['params']) >= 5:
            smells.append(
                f"Code Smell: Lista de Parámetros Larga - "
                f"La función '{func['name']}' en la línea {func['lineno']} tiene 5 o más parámetros: {func['params']}")
    return smells


def detectar_LM(visited: metricas_ast.MetricVisitor):
    # Long Method: LOC método >= 100
    smells = []
    for func in visited.functions:
        if func['total_lines'] >= 100:
            smells.append(
                f"Code Smell: Método Largo - "
                f"El método '{func['name']}' en la línea {func['lineno']} tiene más de 100 líneas de código:"
                f" {func['total_lines']} líneas")
    return smells


def detectar_LMC(visited: metricas_ast.MetricVisitor):
    # NYI
    return []


def detectar_LSC(visited: metricas_ast.MetricVisitor):
    # NYI
    return []


def detectar_LBCL(visited: metricas_ast.MetricVisitor):
    # NYI
    return []


def detectar_UEH(visited: metricas_ast.MetricVisitor):
    # NYI
    return []


def detectar_LLF(visited: metricas_ast.MetricVisitor):
    # Long Lambda Function: NOC >= 80 para cada expresión
    smells = []
    for expr in visited.long_expressions:
        smells.append(
            f"Code Smell: Función Lambda Larga - "
            f"La expresión en la línea {expr['lineno']} tiene más de 80 caracteres "
            f"({expr['line_length']} caracteres encontrados)")
    return smells


def detectar_CLC(visited: metricas_ast.MetricVisitor):
    # NYI
    return []


def detectar_LEC(visited: metricas_ast.MetricVisitor):
    # NYI
    return []


def detectar_LTCE(visited: metricas_ast.MetricVisitor):
    # Long Ternary Conditional Expression: NOC >= 40
    smells = []
    for expr in visited.long_ternary:
        smells.append(
            f"Code Smell: Expresión Condicional Ternaria Larga - "
            f"La expresión ternaria en la línea {expr['lineno']} tiene más de 40 caracteres: ({expr['line_length']}"
            f" caracteres encontrados)")
    return smells
