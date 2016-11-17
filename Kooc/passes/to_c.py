import copy, weakref

from pyrser import meta, fmt
from cnorm.passes import to_c
from cnorm import nodes

from Kooc import knodes

from Kooc.mangling.full import Mangler as FullMangler

mangler = FullMangler()

@meta.add_method(knodes.KcImport)
def to_c(self):
    lsdata = []

    translation_table = dict.fromkeys(map(ord, '/;.%'), None)
    unique_define = 'SOME_GARBAGE_' + self.file_name.translate(translation_table)
    lsdata.append('#ifndef ' + unique_define)
    lsdata.append('# define ' + unique_define)
    lsdata.append('# include "%s"' % self.file_name)
    lsdata.append('#endif')
    return fmt.sep("\n", lsdata)

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
    #           => The type will be OK, resolved from typing visitor

    raise Exception('Unknown context type: {}'.format(ctx))

#TODO: move this to : from Kooc.passes.typing import get_types
#TODO: the type (ex: None or PrimaryType or [PrimaryType, ref(PrimaryType)]) must be wrapped in a KExprType
#      (which allow intersection, merging, etc..)
def get_types(ast):
    def get_single_type(from_t):
        if isinstance(from_t, weakref.ref):
            return from_t()
        return from_t

    t = ast.expr_type

    if isinstance(t, list):
        types = []
        for sub_t in t:
            types.append(get_single_type(sub_t))
        return types

    return get_single_type(t)

@meta.add_method(knodes.KcCall)
def to_c(self):
    ctx = self.context() # self.context is a weakref

    if isinstance(ctx, knodes.KcClass):
        pass # FIXME: need ?

    if isinstance(ctx, knodes.KcModule):
        # fetch all params types
        params_types = []
        for p in self.params:
            params_types.append(nodes.Decl('', get_types(p)))
            pass

        # mangle
        func_ctype = nodes.FuncType(self.expr_type._ctype._identifier, params_types)
        mangled_name = mangler.mangle_module(self.function, func_ctype, typeName = ctx.name)

        # create fake function call
        fake_func_call = nodes.Func(nodes.Id(mangled_name), self.params)
        return fake_func_call.to_c()

    # later: handle class instance
    # - assert context is class instance
    # - get klass
    # - do stuff

    raise Exception('Unknown context type: {}'.format(ctx))
