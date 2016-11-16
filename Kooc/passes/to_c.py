import copy

from pyrser import meta, fmt
from cnorm.passes import to_c
from cnorm import nodes

from Kooc import knodes

from Kooc.mangling.full import Mangler as FullMangler

mangler = FullMangler()

# TODO: refactor to_c of implem & module
@meta.add_method(knodes.KcModule)
def to_c(self):
    lsdata = []
    lsdata.append('// begin of module\n')

    # - generate function prototypes
    for func in self.declallfuncs():
        # mangle
        func._name = mangler.mangle_module(func._name, func._ctype, typeName = self.name)

        lsdata.append(func.to_c())

    # - generate extern variable declarations
    for v in self.declallvars():
        var = copy.deepcopy(v)

        # mangle
        var._name = mangler.mangle_module(var._name, var._ctype, typeName = self.name)

        var._ctype._storage = nodes.Storages.EXTERN
        delattr(var, '_assign_expr')

        lsdata.append(var.to_c())

    lsdata.append('// end of module\n\n')

    return fmt.sep("\n", lsdata)

@meta.add_method(knodes.KcImplementation)
def to_c(self):
    lsdata = []
    lsdata.append('// begin of implem\n')

    # - generate function prototypes
    for func in self.declallfuncs():
        # mangle
        func._name = mangler.mangle_module(func._name, func._ctype, typeName = self.name)

        lsdata.append(func.to_c())

    # - generate variable declarations & definition if needed
    for var in self.declallvars():
        # mangle
        var._name = mangler.mangle_module(var._name, var._ctype, typeName = self.name)

        lsdata.append(var.to_c())

    # - generate variable definition from module/class
    #   FIXME: thoughts: the bind_mc's static vars should be merged with the implem vars ?
    mc = self.bind_mc() # bind_mc is a weakref to the corresponding module/class
    for var in mc.declallvars():
        if not hasattr(var, '_assign_expr'):
            continue

        # mangle
        var._name = mangler.mangle_module(var._name, var._ctype, typeName = self.name)

        lsdata.append(var.to_c())



    lsdata.append('// end of implem\n\n')

    return fmt.sep("\n", lsdata)

@meta.add_method(knodes.KcLookup)
def to_c(self):
    # find type of context
    #   FIXME: how to access ktypes to check type of context ?
    #   => context must be resolved before.. via an AST passe

    ctx = self.context() # self.context is a weakref

    if isinstance(ctx, knodes.KcClass):
        # thoughts: how is class lookup different from module lookup ?
        pass # TODO: handle class lookup

    if isinstance(ctx, knodes.KcModule):

        # mangle member:
        mangled_name = mangler.mangle_module(self.member, self.expr_type._ctype, typeName = ctx.name)

        return nodes.Id(mangled_name).to_c() # or just return mangled_name ?


    # later: handle class instance, check class via expr_type of context
    # thoughts: the context will be a (local ?) variable, his type could
    #           be retrieved from the block ?

    raise Exception('Unknown context type: {}'.format(ctx))

