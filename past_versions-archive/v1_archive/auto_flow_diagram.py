import ast
from graphviz import Digraph


class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.function_calls = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.function_calls.append(node.func.id)
        self.generic_visit(node)


def get_function_calls(code):
    tree = ast.parse(code)
    visitor = FunctionCallVisitor()
    visitor.visit(tree)
    return visitor.function_calls


def create_diagram(function_defs, function_calls):
    dot = Digraph(comment='Python Code Flow Diagram')

    # Create nodes for functions
    for function_def in function_defs:
        dot.node(function_def, function_def + '()')

    # Connect the functions with arrows
    for idx in range(len(function_calls) - 1):
        dot.edge(function_calls[idx], function_calls[idx + 1])

    # Save the diagram to a file
    dot.render('flow_diagram.gv', view=True)


def parse_and_generate_diagram(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    tree = ast.parse(code)
    function_defs = [node.name for node in ast.walk(
        tree) if isinstance(node, ast.FunctionDef)]
    function_calls = get_function_calls(code)

    create_diagram(function_defs, function_calls)


if __name__ == "__main__":
    parse_and_generate_diagram('active_window.py')
