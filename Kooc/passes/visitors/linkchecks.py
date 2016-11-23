from collections import ChainMap
from weakref import ref

from Kooc import knodes
from cnorm import nodes

from . import KVisitorError, VisitorRunner

from .builder import ClassBuilder

class LinkChecks(VisitorRunner):
    """Import, Link, Checks Kooc nodes"""

    def __init__(self, koocer = None):
        VisitorRunner.__init__(self)
        self.koocer = koocer

    def register(self):
        self.register_visitor(self.grab_all_c_top_decl)
        self.register_visitor(self.resolve_imports)
        self.register_visitor(self.bind_implem)
        self.register_visitor(self.check_modules)


    def grab_all_c_top_decl(self):
        c_top_decl = ChainMap({})

        for decl in self.ast.body:
            if not isinstance(decl, nodes.Decl):
                continue

            if decl._name != '':
                c_top_decl[decl._name] = ref(decl)

        setattr(self.ast, "c_top_decl", c_top_decl)


    def resolve_imports(self):
        """Find all @import and fetch types from imported files"""

        if not self.koocer:
            # @import resolution disabled
            return

        for tl in self.ast.body:
            if not isinstance(tl, knodes.KcImport):
                continue

            # load, preprocess, parse:
            kc = self.koocer(tl.file_fullpath)
            kc.parse()

            sub_ast = kc.ast

            # pass basic visitors
            sub_linkchecks = LinkChecks(self.koocer)
            sub_linkchecks.register()
            sub_linkchecks.run(sub_ast)

            sub_class_builder = ClassBuilder()
            sub_class_builder.register()
            sub_class_builder.run(sub_ast)

            # merge sub_ast informations

            # merge kooc types
            new_ktypes = ChainMap(self.ast.ktypes, sub_ast.ktypes)
            self.ast.ktypes = new_ktypes

            # merge C types
            new_types = ChainMap(self.ast.types, sub_ast.types)
            self.ast.types = new_types

            # merge C top declarations
            new_c_top_decl = ChainMap(self.ast.c_top_decl, sub_ast.c_top_decl)
            self.ast.c_top_decl = new_c_top_decl


    def bind_implem(self):
        """Bind each implementation to corresponding module/class"""

        for implem in self.ast.body:
            if not isinstance(implem, knodes.KcImplementation):
                continue

            # find corresponding type (module/class)
            if implem.name in self.ast.ktypes:

                # bind implem to module/class
                implem.bind_mc = self.ast.ktypes[implem.name]
                if isinstance(implem.bind_mc(), knodes.KcClass):
                    implem.__class__ = knodes.KcClassImplementation
                elif isinstance(implem.bind_mc(), knodes.KcModule):
                    implem.__class__ = knodes.KcModuleImplementation

            else:
                raise KVisitorError('Cannot find KType "{}", available KTypes: {}'.format(tl.name, self.ast.ktypes.keys()))


    def check_modules(self):
        """Check module validity"""

        for tl in self.ast.body:
            if not isinstance(tl, knodes.KcModule):
                continue

            for decl in tl:
                # TODO: module declarations should not have same variable with & without constness

                # should not have a static || inline function Decl
                if isinstance(decl, nodes.FuncType):
                    ct = decl._ctype
                    if ct._storage == nodes.Storages.INLINE or ct._storage == nodes.Storages.STATIC:
                        raise KVisitorError('Functions in Module/class cannot be inline or static')

