# import_hook.py
import sys
from fileinput import filename
from importlib.abc import MetaPathFinder, Loader
from importlib.util import spec_from_file_location
import ast

from bcov.boolean_transformer_1.boolean_transformer_1 import BooleanTransformer1


class BooleanTransformLoader1(Loader):
    def __init__(self, source_file):
        self.source_file = source_file

    def exec_module(self, module):
        with open(self.source_file, 'r') as f:
            source = f.read()

        # Parse and transform the code
        tree = ast.parse(source)
        transformer = BooleanTransformer1(self.source_file)
        transformed = transformer.visit(tree)

        # Execute the code (unchanged, but we'll see the print statements)
        code = compile(transformed, self.source_file, 'exec')
        exec(code, module.__dict__)


class SimpleTransformFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        # A real implementation would be more selective
        filename = fullname.split(".")[-1]
        if filename.startswith('test_'):
            # Find the actual file - this is simplified
            if path is None:
                path = sys.path
            for entry in path:
                if entry == '':
                    entry = '.'
                file_path = f"{entry}/{filename.replace('.', '/')}.py"
                try:
                    spec = spec_from_file_location(filename, file_path)
                    if spec:
                        spec.loader = BooleanTransformLoader1(file_path)
                        return spec
                except Exception:
                    continue
        return None


# Install our finder
sys.meta_path.insert(0, SimpleTransformFinder())