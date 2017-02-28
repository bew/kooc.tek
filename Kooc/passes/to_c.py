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
    unique_define = 'SOME_GARBAGE_' + self.file_fullpath.translate(translation_table)

    header_name = self.file_name[:-3] + '.h'

    lsdata.append('#ifndef ' + unique_define)
    lsdata.append('# define ' + unique_define)
    lsdata.append('# include "%s"' % header_name)
    lsdata.append('#endif\n\n')
    return fmt.sep("\n", lsdata)

@meta.add_method(knodes.KcModule)
def to_c(self):
    lsdata = []
    lsdata.append('// begin of module ' + self.name + ' header\n')

    # - generate function prototypes
    for func in self.declallfuncs():
        # mangle
        func._name = mangler.mangle_module(func._name, func._ctype, typeName = self.name)
        if hasattr(func, 'body'):
            delattr(func, 'body')

        lsdata.append(func.to_c())

    # - generate extern variable declarations
    for v in self.declallvars():
        var = copy.deepcopy(v)

        # mangle
        #name = mangler.mangle_module(var._name, var._ctype, typeName = self.name)
        #print('name variable after mangling:', name)

        # transform to extern declaration
        var._ctype._storage = nodes.Storages.EXTERN
        delattr(var, '_assign_expr')

        lsdata.append(var.to_c())

    lsdata.append('// end of module ' + self.name + ' header\n')
    return fmt.sep("\n", lsdata)

@meta.add_method(knodes.KcModuleImplementation)
def to_c(self):
    lsdata = []
    lsdata.append('// begin of module ' + self.name + ' implem\n')

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
    mc = self.bind_mc() # bind_mc is a weakref to the corresponding module/class
    for var in mc.declallvars():
        if not hasattr(var, '_assign_expr'):
            continue

        # mangle
        var._name = mangler.mangle_module(var._name, var._ctype, typeName = self.name)
        lsdata.append(var.to_c())

    lsdata.append('// end of module ' + self.name + ' implem\n')

    return fmt.sep("\n", lsdata)

@meta.add_method(knodes.KcLookup)
def to_c(self):
    ctx = self.context() # self.context is a weakref

    if isinstance(ctx, knodes.KcModule):
        # mangle
        mangled_name = mangler.mangle_module(self.member, self.expr_type, typeName = ctx.name)
        return nodes.Id(mangled_name).to_c()


    # later: handle class instance, check class via expr_type of context
    # thoughts: the context will be a (local ?) variable, his type could
    #           be retrieved from the block ?
    #           => The type will be OK, resolved from typing visitor

    raise Exception('Unknown context type: {}'.format(ctx))

def get_types(ast):
    def get_single_type(from_t):
        if isinstance(from_t, weakref.ref):
            return from_t()
        return from_t

    assert(ast.expr_type is not None)
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

    if isinstance(ctx, knodes.KcModule):
        # fetch all params types
        params_types = []
        for p in self.params:
            params_types.append(nodes.Decl('', get_types(p)))
            pass

        # mangle
        func_ctype = nodes.FuncType(self.expr_type._identifier, params_types)
        mangled_name = mangler.mangle_module(self.function, func_ctype, typeName = ctx.name)

        # create fake function call
        fake_func_call = nodes.Func(nodes.Id(mangled_name), self.params)
        return fake_func_call.to_c()

    # later: handle class instance
    # - assert context is class instance : any pointer(KType)
    # - get klass of KType
    # - find method
    # - method is virtual ? use vtable
    # - method is not virtual ? use direct function call

    raise Exception('Unknown context type: {}'.format(ctx))

# KcClass
#--------------------------------

@meta.add_method(knodes.KcClass)
def to_c(self):
    # generate header for the class
    class_lsdata = []
    class_lsdata.append('// begin of class ' + self.name + ' header')

    # Fast forward declaration of metadata
    metadata_forward_decl = copy.deepcopy(self.structs['metadata'])
    if hasattr(metadata_forward_decl._ctype, 'fields'):
        delattr(metadata_forward_decl._ctype, 'fields')

    class_lsdata.append(metadata_forward_decl.to_c())
    class_lsdata.append(self.structs['instance'].to_c())
    class_lsdata.append(self.structs['interface'].to_c())
    class_lsdata.append(self.typedef.to_c())

    class_lsdata.append('// end of class ' + self.name + ' header\n')
    return fmt.sep('\n', class_lsdata)


@meta.add_method(knodes.KcClassImplementation)
def to_c(self):
    # generate implemention for the class
    implem_lsdata = []
    implem_lsdata.append('// begin of class ' + self.name + ' implem')

    klass = self.bind_mc()

    implem_lsdata.append(klass.structs['vtable'].to_c())
    implem_lsdata.append(klass.structs['metadata'].to_c())
    implem_lsdata.append('// end of class ' + self.name + ' implem\n')
    return fmt.sep('\n', implem_lsdata)

