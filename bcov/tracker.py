import ast

class Node:
    def __init__(self, children: list['Node'], file, line_start, line_end, col_start, col_end):
        self.file = file
        self.line_start = line_start
        self.line_end = line_end
        self.col_start = col_start
        self.col_end = col_end
        self.children = children if children is not None else []

    def get_key(self):
        """Return an id to uniquely identify this node"""
        return (self.file,
                self.line_start,
                self.line_end,
                self.col_start,
                self.col_end
                )

class BoolExprNode(Node):
    def __init__(self, children: list['Node'], file, line_start, line_end, col_start, col_end):
        super().__init__(children, file, line_start, line_end, col_start, col_end)

class AndNode(Node):
    def __init__(self, children: list['Node'], file, line_start, line_end, col_start, col_end):
        super().__init__(children, file, line_start, line_end, col_start, col_end)

class OrNode(Node):
    def __init__(self, children: list['Node'], file, line_start, line_end, col_start, col_end):
        super().__init__(children, file, line_start, line_end, col_start, col_end)

class UnaryNotNode(Node):
    def __init__(self, children: list['Node'], file, line_start, line_end, col_start, col_end):
        super().__init__(children, file, line_start, line_end, col_start, col_end)


class BooleanExpressionTracker:
    def __init__(self):
        self.nodes_map = dict()

    def _get_node(self, filename: str, node: ast.BoolOp):
        n = None
        if isinstance(node.op, ast.And):
            children = []
            for child in node.values:
                child_node = self._get_node(filename, child)
                children.append(child_node)
            n = AndNode(children = children,
                        file = filename,
                        line_start= node.lineno,
                        line_end=node.end_lineno,
                        col_start=node.col_offset,
                        col_end=node.end_col_offset
                        )
        else:
            raise NotImplemented(f"node type not supported yet: {node}")


        key = n.get_key()
        if key in self.nodes_map:
            # already processed
            return self.nodes_map[key]
        self.nodes_map[key] = n
        return n

    # Recursively all this node and all the children
    def exists(self, filename: str, node: ast.BoolOp):
        """
        Tell the tracker the a boolOp exists here
        """

        # 1. Ignore if already present
        # 2. track this
        # 3. track all the subnodes

        if isinstance(node.op, ast.And):
            n = AndNode()
