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


def detectar_LC(visited: metricas_ast.MetricVisitor):
    # Long Class: LOC >= 200 o #Métodos + # Atributos > 40
    smells = []
    for cls in visited.classes:
        if cls['total_lines'] >= 200:
            smells.append(
                f"Code Smell: Clase Larga - "
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
    # Long Message Chain: LMC >= 4
    smells = []
    for expr in visited.lmc_expressions:
        smells.append(
            f"Code Smell: Cadena de Mensajes Larga - "
            f"La expresión en la línea {expr['lineno']} accede a un objeto mediante una cadena de atributos mayor a 4: "
            f"{expr['str']}")
    return smells


def detectar_LSC(visited: metricas_ast.MetricVisitor):
    # Long Scope Chaining: DOC >= 3
    smells = []
    for function in visited.functions:
        if function['DOC'] >= 3:
            smells.append(
                f"Code Smell: Cadena de Alcance Larga - "
                f"La función en la línea {function['lineno']} tiene nivel de anidación alto con DOC de: "
                f"{function['DOC']}")
    return smells


def detectar_LBCL(visited: metricas_ast.MetricVisitor):
    # Long Base Class List: #clases base >= 3
    smells = []
    for cls in visited.classes:
        if len(cls['base_classes']) >= 3:
            smell = (f"Code Smell: Lista de Clases Base Larga - "
                     f"La clase '{cls['name']}' en la línea {cls['lineno']} tiene más de 3 clases base: ")
            faltan = len(cls['base_classes'])-1
            for base in cls['base_classes']:
                smell += str(base.id)
                if faltan > 0:
                    smell += ",  "
                faltan -= 1
            smells.append(smell)
    return smells


def detectar_UEH(visited: metricas_ast.MetricVisitor):
    # Manejo de Excepciones Inútil: Excepciones totales y generales = 1 o excepciones totales = excepciones vacías
    smells = []
    for expr in visited.ueh_statements:
        smells.append(
            f"Code Smell: Manejo de Excepciones Inútil - "
            f"El manejo de excepciones en la línea {expr.lineno} maneja una excepción demasiado general o tiene "
            f"cláusulas de excepción vacías.")
    return smells


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
    # Complex List Comprehension: NOL + NOCC >= 4 para comprensiones de lista
    smells = []
    for expr in visited.clc_expressions:
        smells.append(
            f"Code Smell: Comprensión de Lista Compleja - "
            f"La comprensión de lista en la línea {expr} tiene más de 4 bucles + condicionales")
    return smells


def detectar_LEC(visited: metricas_ast.MetricVisitor):
    # Long Element Chain: cadena de elementos de longitud > 3
    smells = []
    for expr in visited.lec_expressions:
        smells.append(
            f"Code Smell: Cadena de Elementos Larga - "
            f"La expresión en la línea {expr['lineno']} es una cadena de elementos de longitud igual o mayor a 3: "
            f"{expr['str']}")
    return smells


def detectar_LTCE(visited: metricas_ast.MetricVisitor):
    # Long Ternary Conditional Expression: NOC >= 40
    smells = []
    for expr in visited.long_ternary:
        smells.append(
            f"Code Smell: Expresión Condicional Ternaria Larga - "
            f"La expresión ternaria en la línea {expr['lineno']} tiene más de 40 caracteres: ({expr['line_length']}"
            f" caracteres encontrados)")
    return smells
