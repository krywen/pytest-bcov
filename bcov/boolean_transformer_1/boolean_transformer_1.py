# boolean_transformer.py
import ast

from ast import Name, Compare


class BooleanTransformer1(ast.NodeTransformer):
    def __init__(self, filename: str):
        # Store the filename when we create the transformer
        self.filename = filename
        print("BooleanTransformer1 started")
        super().__init__()

    # def visit_Compare(self, node: ast.Compare):
    #     print(
    #         f"Found a Compare operation at {self.filename} l{node.lineno}:c{node.col_offset}-l{node.end_lineno}:c{node.end_col_offset} "
    #         f"type_comment {getattr(node, 'type_comment', None)}")
    #     for child in node.comparators:
    #         print(
    #             f"child {self.filename} l{child.lineno}:c{child.col_offset}-l{child.end_lineno}:c{child.end_col_offset} ")
    #         print(f"child id {child.id}")
    #     return node

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.AST:
        print(f"Found a boolean operation at {self.filename} l{node.lineno}:c{node.col_offset}-l{node.end_lineno}:c{node.end_col_offset} "
              f"type_comment {getattr(node, 'type_comment', None)}")
        print(f"{node.op} {node.values}")
        for child in node.values:
            print(
                f"child {self.filename} l{child.lineno}:c{child.col_offset}-l{child.end_lineno}:c{child.end_col_offset} ")
            if isinstance(child, Compare):
                # child as Compare
                print(f"Compare: ops {child.ops}, comparators {child.comparators} left{child.left}")
                pass
            if isinstance(child, Name):
                print(f"Name: name {child.id}")
                pass
        return node
