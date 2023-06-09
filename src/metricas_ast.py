import ast


class MetricVisitor(ast.NodeVisitor):
    def __init__(self):
        self.loops = 0
        self.conditionals = 0
        self.functions = []
        self.classes = []
        self.exceptions = 0
        self.empty_exceptions = 0
        self.long_ternary = []
        self.long_expressions = []
        self.lmc_expressions = []
        self.clc_expressions = []
        self.lec_expressions = []
        self.ueh_statements = []

    def visit_FunctionDef(self, node):
        class_dict = ({
            'name': node.name,
            'lineno': node.lineno,
            'params': [arg.arg for arg in node.args.args],
            'total_lines': node.end_lineno - node.lineno + 1,
            'DOC': 0
        })
        class_dict['DOC'] = self.calculate_depth_closure(node)
        self.functions.append(class_dict)
        self.generic_visit(node)

    def calculate_depth_closure(self, node):
        depth = 1
        # Recorrer las cláusulas "closure" de la función
        for closure in node.body:
            if isinstance(closure, ast.FunctionDef):
                # Llamada recursiva para calcular el depth of closure de la función anidada
                nested_depth = self.calculate_depth_closure(closure) + 1
                depth = max(depth, nested_depth)
        return depth

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
        line_length = node.end_col_offset - node.col_offset
        if line_length >= 40:
            self.long_ternary.append({'lineno': node.lineno, 'line_length': line_length})
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
            'total_lines': node.end_lineno - node.lineno + 1,
            'base_classes': node.bases
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

    def visit_Expr(self, node):
        line_length = node.end_col_offset - node.col_offset
        if line_length >= 80:
            self.long_expressions.append({'lineno': node.lineno, 'line_length': line_length})
        self.generic_visit(node)

    def visit_Attribute(self, node):
        access_chain_length = 0
        current_node = node
        expression = []

        while isinstance(current_node, ast.Attribute):
            expression.append(current_node.attr)
            current_node = current_node.value
            access_chain_length += 1

        if access_chain_length >= 4:
            if isinstance(current_node, ast.Name):
                expression.append(current_node.id)
            elif isinstance(current_node, ast.Call):
                expression.append(ast.dump(current_node.func))
            expression.reverse()
            expression_str = '.'.join(str(comp) for comp in expression)
            self.lmc_expressions.append({'lineno': current_node.lineno, 'str': expression_str})
        self.generic_visit(node)

    def visit_ListComp(self, node):
        num_loops = sum(1 for generator in node.generators if isinstance(generator, ast.comprehension))
        num_conditionals = sum(1 for generator in node.generators if isinstance(generator, ast.comprehension) and
                               generator.ifs)
        total = num_loops + num_conditionals
        if total >= 4:
            self.clc_expressions.append(node.lineno)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        nested_count = 0
        while isinstance(node, ast.Subscript):
            nested_count += 1
            node = node.value
        if nested_count >= 3:
            self.lec_expressions.append({'lineno': node.lineno, 'str': ast.unparse(node)})
        self.generic_visit(node)

    def visit_Try(self, node):
        self.exceptions += 1
        except_count = len(node.handlers)
        general_except_count = sum(isinstance(handler.type, ast.Name) and handler.type.id == 'Exception'
                                   for handler in node.handlers)
        empty_except_count = sum(handler.body == [] for handler in node.handlers)
        if (except_count == 1 and general_except_count == 1) or (except_count == empty_except_count and
                                                                 except_count > 1):
            self.ueh_statements.append(node)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.generic_visit(node)
