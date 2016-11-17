from Kooc import knodes
from cnorm import nodes

from . import KVisitorError, VisitorRunner

class LinkChecks(VisitorRunner):
    """Import, Link, Checks Kooc nodes"""

    def register(self):
        self.register_visitor(self.bind_implem)
        self.register_visitor(self.check_modules)

    def bind_implem(self):
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
        for tl in self.ast.body:
            if not isinstance(tl, knodes.KcModule):
                continue

            # should not have same variable with & without constness
            # should not have a static || inline function Decl

