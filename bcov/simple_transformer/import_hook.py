import sys
from importlib.abc import MetaPathFinder, Loader
from importlib.util import spec_from_file_location
import ast

from bcov.simple_transformer.transformer_simple import SimpleBooleanTransformer


# from bcov.transformer_simple import SimpleBooleanTransformer



class TransformLoader(Loader):
    def __init__(self, source_file):
        self.source_file = source_file

    def exec_module(self, module):
        with open(self.source_file, 'r') as f:
            source = f.read()

        # Parse and transform the code
        tree = ast.parse(source)
        transformer = SimpleBooleanTransformer(self.source_file)
        transformed = transformer.visit(tree)

        # Execute the code (unchanged, but we'll see the print statements)
        code = compile(transformed, self.source_file, 'exec')
        exec(code, module.__dict__)


class SimpleTransformFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        # A real implementation would be more selective
        if fullname.startswith('test_'):
            # Find the actual file - this is simplified
            if path is None:
                path = sys.path
            for entry in path:
                if entry == '':
                    entry = '.'
                file_path = f"{entry}/{fullname.replace('.', '/')}.py"
                try:
                    spec = spec_from_file_location(fullname, file_path)
                    if spec:
                        spec.loader = TransformLoader(file_path)
                        return spec
                except Exception:
                    continue
        return None


# Install our finder
sys.meta_path.insert(0, SimpleTransformFinder())
