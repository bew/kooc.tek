from Kooc import knodes
from cnorm import nodes

from . import KVisitorError, VisitorRunner

class LinkChecks(VisitorRunner):
    """Import, Link, Checks Kooc nodes"""

    def __init__(self, koocer):
        VisitorRunner.__init__(self)
        self.koocer = koocer

    def register(self):
        self.register_visitor(self.resolve_imports)
        self.register_visitor(self.bind_implem)
        self.register_visitor(self.check_modules)

    def resolve_imports(self):
        """Find all @import and fetch types from imported files"""

        for tl in self.ast.body:
            if not isinstance(tl, knodes.KcImport):
                continue

            # load, preprocess, parse:
            kc = self.koocer(tl.file_fullpath)
            kc.parse()

            sub_ast = kc.ast

            # extract C types & Kooc types for merging
            from collections import ChainMap

            # merge kooc types
            new_ktypes = ChainMap(self.ast.ktypes, sub_ast.ktypes)
            self.ast.ktypes = new_ktypes

            # merge C types
            new_types = ChainMap(self.ast.types, sub_ast.types)
            self.ast.types = new_types


    def bind_implem(self):
        """Bind each implementation to corresponding module/class"""

        for tl in self.ast.body:
            if not isinstance(tl, knodes.KcImplementation):
                continue

            # find corresponding type (module/class)
            if tl.name in self.ast.ktypes:
                # bind implem to kooc type
                tl.bind_mc = self.ast.ktypes[tl.name]
            else:
                raise KVisitorError('Cannot find KType "{}", available KTypes: {}'.format(tl.name, self.ast.ktypes.keys()))


    def check_modules(self):
        """Check module validity"""

        for tl in self.ast.body:
            if not isinstance(tl, knodes.KcModule):
                continue

            # should not have same variable with & without constness
            # should not have a static || inline function Decl

