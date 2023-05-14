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
    file_smells = {'count': {}, 'str': []}

    # Asignación de smells y funciones
    smell_functions = {
        'Long Class': detectar_LC,
        'Long Parameter List': detectar_LPL,
        'Long Method': detectar_LM,
        'Long Message Chain': detectar_LMC,
        'Long Scope Chaining': detectar_LSC,
        'Long Base Class List': detectar_LBCL,
        'Useless Exception Handling': detectar_UEH,
        'Long Lambda Function': detectar_LLF,
        'Complex List Comprehension': detectar_CLC,
        'Long Element Chain': detectar_LEC,
        'Long Ternary Conditional Expression': detectar_LTCE,
        'Data Class': detectar_DC,
    }

    # Por cada smell ejecutar función y actualizar contador
    for smell in smell_functions:
        smell_result = smell_functions[smell](visited)
        file_smells['str'].extend(smell_result)
        file_smells['count'].update({smell: len(smell_result)})

    return file_smells


def detectar_LC(visited: metricas_ast.MetricVisitor):
    # Long Class: LOC >= 200 o #Métodos + # Atributos > 40
    smells = []
    for cls in visited.classes:
        if cls['total_lines'] >= 200:
            smells.append(
                f"Code Smell: Long Class - "
                f"La clase '{cls['name']}' en la línea {cls['lineno']} tiene {cls['total_lines']} líneas de código")
        elif cls['methods'] + cls['attributes'] > 40:
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
                f"Code Smell: Long Parameter List - "
                f"La función '{func['name']}' en la línea {func['lineno']} tiene 5 o más parámetros: {func['params']}")
    return smells


def detectar_LM(visited: metricas_ast.MetricVisitor):
    # Long Method: LOC método >= 100
    smells = []
    for func in visited.functions:
        if func['total_lines'] >= 100:
            smells.append(
                f"Code Smell: Long Method - "
                f"El método '{func['name']}' en la línea {func['lineno']} tiene más de 100 líneas de código:"
                f" {func['total_lines']} líneas")
    return smells


def detectar_LMC(visited: metricas_ast.MetricVisitor):
    # Long Message Chain: LMC >= 4
    smells = []
    for expr in visited.lmc_expressions:
        smells.append(
            f"Code Smell: Long Message Chain - "
            f"La expresión en la línea {expr['lineno']} accede a un objeto mediante una cadena de atributos mayor a 4: "
            f"{expr['str']}")
    return smells


def detectar_LSC(visited: metricas_ast.MetricVisitor):
    # Long Scope Chaining: DOC >= 3
    smells = []
    for function in visited.functions:
        if function['DOC'] >= 3:
            smells.append(
                f"Code Smell: Long Scope Chaining - "
                f"La función en la línea {function['lineno']} tiene nivel de anidación alto con DOC de: "
                f"{function['DOC']}")
    return smells


def detectar_LBCL(visited: metricas_ast.MetricVisitor):
    # Long Base Class List: #clases base >= 3
    smells = []
    for cls in visited.classes:
        if len(cls['base_classes']) >= 3:
            smell = (f"Code Smell: Long Base Class List - "
                     f"La clase '{cls['name']}' en la línea {cls['lineno']} tiene más de 3 clases base: ")
            faltan = len(cls['base_classes']) - 1
            for base in cls['base_classes']:
                smell += str(base.id)
                if faltan > 0:
                    smell += ",  "
                faltan -= 1
            smells.append(smell)
    return smells


def detectar_UEH(visited: metricas_ast.MetricVisitor):
    # Useless Exception Handling: Excepciones totales y generales = 1 o excepciones totales = excepciones vacías
    smells = []
    for expr in visited.ueh_statements:
        smells.append(
            f"Code Smell: Useless Exception Handling - "
            f"El manejo de excepciones en la línea {expr.lineno} maneja una excepción demasiado general o tiene "
            f"cláusulas de excepción vacías.")
    return smells


def detectar_LLF(visited: metricas_ast.MetricVisitor):
    # Long Lambda Function: NOC >= 80 para cada expresión
    smells = []
    for expr in visited.long_expressions:
        smells.append(
            f"Code Smell: Long Lambda Function - "
            f"La expresión en la línea {expr['lineno']} tiene más de 80 caracteres "
            f"({expr['line_length']} caracteres encontrados)")
    return smells


def detectar_CLC(visited: metricas_ast.MetricVisitor):
    # Complex List Comprehension: NOL + NOCC >= 4 para comprensiones de lista
    smells = []
    for expr in visited.clc_expressions:
        smells.append(
            f"Code Smell: Complex List Comprehension - "
            f"La comprensión de lista en la línea {expr} tiene más de 4 bucles + condicionales")
    return smells


def detectar_LEC(visited: metricas_ast.MetricVisitor):
    # Long Element Chain: cadena de elementos de longitud > 3
    smells = []
    for expr in visited.lec_expressions:
        smells.append(
            f"Code Smell: Long Element Chain - "
            f"La expresión en la línea {expr['lineno']} es una cadena de elementos de longitud igual o mayor a 3: "
            f"{expr['str']}")
    return smells


def detectar_LTCE(visited: metricas_ast.MetricVisitor):
    # Long Ternary Conditional Expression: NOC >= 40
    smells = []
    for expr in visited.long_ternary:
        smells.append(
            f"Code Smell: Long Ternary Conditional Expression - "
            f"La expresión ternaria en la línea {expr['lineno']} tiene más de 40 caracteres: ({expr['line_length']}"
            f" caracteres encontrados)")
    return smells


def detectar_DC(visited: metricas_ast.MetricVisitor):
    # Data Class: NOM = 0
    smells = []
    for cls in visited.classes:
        if cls['methods'] == 0:
            smells.append(
                f"Code Smell: Data Class - "
                f"La clase {cls['name']} en la línea {cls['lineno']} no tiene funcionalidad")
    return smells
