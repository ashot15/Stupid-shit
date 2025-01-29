import ast
import astor  # pip install astor
import sys
from io import StringIO

class SelfToSeTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Заменяем 'se' на 'self' в параметрах функции
        for arg in node.args.args:
            if arg.arg == 'se':
                arg.arg = 'self'
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'se':
            node.value.id = 'self'
        self.generic_visit(node)
        return node

def transform_code(code):
    tree = ast.parse(code)
    transformer = SelfToSeTransformer()
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)
    return astor.to_source(transformed_tree)

class CodeTransformer:
    def __init__(self):
        self.original_stdout = sys.stdout
        self.buffer = StringIO()

    def transform_and_execute(self, code):
        transformed_code = transform_code(code)
        sys.stdout = self.buffer
        exec(compile(transformed_code, filename="<ast>", mode="exec"), globals())
        sys.stdout = self.original_stdout
        return self.buffer.getvalue()


    