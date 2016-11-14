from pyrser import meta, fmt
from cnorm.passes import to_c
from cnorm import nodes

from Kooc import knodes

from Kooc.mangling import mangling

@meta.add_method(knodes.KcModule)
def to_c(self):
    lsdata = []
    lsdata.append('// begin of module\n')

    # - generate function prototypes
    for func in self.declallfuncs():
        fname = func._name

        # mangle
        #mangled_name = mangling.mangle(func._name, func._ctype, DECLARATION_FROM_MODULE, 'module_name')
        # FIXME: mangling should not have side effect => should not modify the object !!
        mangling.mangle(func, originName = self.name)

        lsdata.append(func.to_c())
        func._name = fname

    # - generate extern variable declarations
    for var in self.declallvars():
        vname = var._name

        # mangle
        mangling.mangle(var, originName = self.name)

        var._ctype._storage = nodes.Storages.EXTERN

        lsdata.append(var.to_c())
        var._name = vname

    lsdata.append('// end of module\n\n')

    return fmt.sep("\n", lsdata)

@meta.add_method(knodes.KcImplementation)
def to_c(self):
    lsdata = []
    lsdata.append('// begin of implem\n')

    # - generate function prototypes
    for func in self.declallfuncs():
        fname = func._name

        # mangle
        #mangled_name = mangling.mangle(func._name, func._ctype, DECLARATION_FROM_MODULE, 'module_name')
        # FIXME: mangling should not have side effect => should not modify the object !!
        mangling.mangle(func, originName = self.name)

        lsdata.append(func.to_c())
        func._name = fname

    # - generate variable declarations & definition if needed
    for var in self.declallvars():
        vname = var._name

        # find in corresponding module/class if this variable needs to be initialized
        # thoughts: there shoudn't be any uninitialized variable in implem..

        # mangle
        mangling.mangle(var, originName = self.name)

        lsdata.append(var.to_c())
        var._name = vname

    # - generate variable definition from module/class
    #   FIXME: thoughts: the bind_mc's static vars should be merged with the implem vars ?
    #mc = self.bind_mc() # bind_mc is a weakref to the corresponding module/class
    #for var in mc.all_static_vars():
    #    pass

    lsdata.append('// end of implem\n\n')

    return fmt.sep("\n", lsdata)

@meta.add_method(knodes.KcLookup)
def to_c(self):
    # find type of context
    #   FIXME: how to access ktypes to check type of context ?
    #   => context must be resolved before.. via an AST passe

    #ctx = self.context() # self.context is a weakref
    ctx = None

    if isinstance(ctx, knodes.KcClass):
        pass # TODO: handle class lookup

    if isinstance(ctx, knodes.KcModule):

        # mangle member:
        # FIXME: mangling is awful, I need to create a cnorm node for nothing...
        decl = nodes.Decl(self.member, self.expr_type)
        mangling.mangle(decl, originName = ctx.name)
        return decl.to_c()

    # later: handle class instance, check class via expr_type of context
    # thoughts: the context will be a (local ?) variable, his type could
    #           be retrieved from the block ?

    return ''

