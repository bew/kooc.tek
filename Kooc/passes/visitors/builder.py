from Kooc import knodes
from cnorm import nodes

import copy

from . import KVisitorError, VisitorRunner

# given a class 'Class'

# available functions:
# From Object:
# - isKindOf(Class *, Class *other);     -> libkrt: isKindOf
# - isKindOf(Class *, char *class_name); -> libkrt: isKindOfStr
# - isInstanceOf(Class *, Class *other);     -> libkrt: isInstanceOf
# - isInstanceOf(Class *, char *class_name); -> libkrt: isInstanceOfStr
# FIXME: verify functions types

# ClassBuiltin.alloc: (en gros)
#--------------------------------
# return malloc(sizeof(Class))

# ClassBuiltin.new:
#--------------------------------
# self = ClassBuiltin.alloc
# if Class.init exists:
#    call Class.init(self, *args)
# else:
#    set default members values # if any given in @class
#

# ctor de copie:
#--------------------------------
# self = ClassBuiltin.alloc
# if Class.init exists:
#    call Class.init(self, other)
# else:
#    use memcpy

# ClassBuiltin.delete:
#--------------------------------
# Class.clean(self) if Class.clean
# free(self)




# structures:

# kc_{class}_vtable
# {
#   les methodes virtuals triées parentes
#   les methodes virtuals triées de {class}
# }

# kc_{class}_metadata
# {
#   char *name;
#   char *inheritance_list;
#   kc_{class}_vtable vtable;
# }

# kc_{class}_instance
# {
#   type1 member1;
#   type2 member2;
#   type3 member3;
# }


# kc_{class}_interface & {class}
# {
#   kc_{class}_metadata *meta;
#   kc_{class}_instance instance;
# }


def func_add_param_self(func, class_name):
    instance_type = nodes.PrimaryType(class_name)
    instance_type.push(nodes.PointerType())

    self_param = nodes.Decl('self', instance_type)
    func._params.insert(0, self_param)



class ClassBuilder(VisitorRunner):

    def register(self):
        self.register_visitor(self.methods_add_self)
        self.register_visitor(self.group_member_methods_virtuals)

        # should be last
        self.register_visitor(self.build_class_structs)

    #--------------------------------
    def add_ktype_object(self):
        """Add Object base class to ktypes"""

    #--------------------------------
    def methods_add_self(self):
        """add 'self' param to methods & virtuals functions"""

        for klass in self.ast.body:
            if not isinstance(klass, knodes.KcClass):
                continue

            for decl in klass.body:
                if isinstance(decl, (knodes.KcMethodDecl, knodes.KcVirtualDecl)):
                    func_add_param_self(decl._ctype, klass.name)


    #--------------------------------
    # architecture for klass.{members,methods,virtuals} :
    #    'decl_name'  => [ decl1, decl2 ]
    #    'decl_name2' => [ decl3, decl4 ]
    #
    # architecture for klass.parents_{virtuals,members} :
    #    'Object'  => {
    #        'isKindOf'     => [ decl5, decl6 ]
    #        'isInstanceOf' => [ decl7, decl8 ]
    #    },
    #    'Parent1' => {
    #        'some_function' => [ decl9 ]
    #        'do_stuff'      => [ decl10, decl11 ]
    #    }
    #--------------------------------
    def group_member_methods_virtuals(self):

        # Helper functions

        def add_decl_to_group(group_holder, name, decl):
            """add a declaration to a group holder, under a specific name"""

            if not name in group_holder:
                group_holder[name] = []

            group_holder[name].append(decl)

        def remove_decls_from_body(body, group_holder):
            """remove all declarations contained in group holder from the body"""

            for name in group_holder:
                decls = group_holder[name]
                for decl in decls:
                    body[:] = [x for x in body if x is not decl] # body.remove(decl)

        def extract_decl_from_body_to_group(body, group_holder, type_matching):
            """extract declarations matching specific type, from body to group holder"""

            for decl in body:
                if not isinstance(decl, type_matching):
                    continue
                add_decl_to_group(group_holder, decl._name, decl)

            remove_decls_from_body(body, group_holder)


        object_virtual_methods = self.get_object_virtual_methods()

        # for each classes
        for klass in self.ast.body:
            if not isinstance(klass, knodes.KcClass):
                continue

            # Group instance member variables
            klass.members = {}
            extract_decl_from_body_to_group(klass.body, klass.members, knodes.KcMemberDecl)

            # Group methods
            klass.methods = {}
            extract_decl_from_body_to_group(klass.body, klass.methods, knodes.KcMethodDecl)

            # Group virtual methods
            klass.virtuals = {}
            extract_decl_from_body_to_group(klass.body, klass.virtuals, knodes.KcVirtualDecl)

            # Group virtuals & members from parents
            klass.parents_members = {}
            klass.parents_members['Object'] = {} # no members for Object

            klass.parents_virtuals = {}
            klass.parents_virtuals['Object'] = object_virtual_methods

            # find instance variables for each parents
            for parent_name in klass.parents:
                parent = self.ast.ktypes[parent_name]()

                klass.parents_members[parent_name] = parent.members

            # find virtuals for each parents
            for parent_name in klass.parents:
                parent = self.ast.ktypes[parent_name]()

                klass.parents_virtuals[parent_name] = parent.virtuals

            # add Object as first parent:
            klass.parents.insert(0, 'Object')


    def get_object_virtual_methods(self):
        class_instance_ctype = nodes.PrimaryType('Object')
        class_instance_ctype.push(nodes.PointerType())
        class_instance_decl = nodes.Decl('', class_instance_ctype)

        string_ctype = nodes.PrimaryType('char')
        string_ctype.push(nodes.PointerType())
        string_decl = nodes.Decl('', string_ctype)

        virtuals = {}
        virtuals['isKindOf'] = []
        virtuals['isInstanceOf'] = []

        # int isKindOf(Class *, Class *other)
        isKindOf_ctype = nodes.FuncType('int', [class_instance_decl, class_instance_decl])
        virtuals['isKindOf'].append(nodes.Decl('isKindOf', isKindOf_ctype))

        # int isKindOf(Class *, char *name)
        isKindOfStr_ctype = nodes.FuncType('int', [class_instance_decl, string_decl])
        virtuals['isKindOf'].append(nodes.Decl('isKindOfStr', isKindOfStr_ctype))

        # int isInstanceOf(Class *, Class *other)
        isInstanceOf_ctype = nodes.FuncType('int', [class_instance_decl, class_instance_decl])
        virtuals['isInstanceOf'].append(nodes.Decl('isInstanceOf', isInstanceOf_ctype))

        # int isInstanceOf(Class *, char *name)
        isInstanceOfStr_ctype = nodes.FuncType('int', [class_instance_decl, string_decl])
        virtuals['isInstanceOf'].append(nodes.Decl('isInstanceOfStr', isInstanceOfStr_ctype))

        return virtuals



    def build_class_structs(self):
        """Build vtable, metadata, instance, interface C structures"""

        for klass in self.ast.body:
            if not isinstance(klass, knodes.KcClass):
                continue

            klass.structs = {}
            klass.structs['vtable'] = self.build_vtable_struct(klass)
            klass.structs['metadata'] = self.build_metadata_struct(klass)
            klass.structs['instance'] = self.build_instance_struct(klass)
            klass.structs['interface'] = self.build_interface_struct(klass)






    # build class vtable
    #--------------------------------
    def build_vtable_struct(self, klass):

        def add_decl_fields_from_group(group_holder, fields_holder):
            for name in sorted(group_holder.keys()):
                for decl in group_holder[name]:
                    fields_holder.append(decl)

        vtable_struct_ctype = nodes.ComposedType('kc_' + klass.name + '_vtable')
        vtable_struct_ctype._specifier = nodes.Specifiers.STRUCT
        vtable_struct_ctype.fields = []

        # add virtuals from class's parents
        for parent_name in klass.parents:
            virtuals = klass.parents_virtuals[parent_name]
            add_decl_fields_from_group(virtuals, vtable_struct_ctype.fields)

        # add virtuals from current class
        add_decl_fields_from_group(klass.virtuals, vtable_struct_ctype.fields)

        return nodes.Decl('', vtable_struct_ctype)


    # build class metadata
    #--------------------------------
    def build_metadata_struct(self, klass):

        struct_ctype = nodes.ComposedType('kc_' + klass.name + '_metadata')
        struct_ctype._specifier = nodes.Specifiers.STRUCT
        struct_ctype.fields = []

        # class name
        cname_ctype = nodes.PrimaryType('char')
        cname_ctype.push(nodes.PointerType())
        struct_ctype.fields.append(nodes.Decl('name', cname_ctype))

        # inheritance list
        inhlist_ctype = nodes.PrimaryType('char')
        inhlist_ctype.push(nodes.PointerType())
        struct_ctype.fields.append(nodes.Decl('inheritance_list', inhlist_ctype))

        # vtable
        vtable_ctype = nodes.PrimaryType('kc_' + klass.name + '_vtable')
        struct_ctype.fields.append(nodes.Decl('vtable', vtable_ctype))

        return nodes.Decl('', struct_ctype)

    # build class instance
    #--------------------------------
    def build_instance_struct(self, klass):

        def add_decl_fields_from_group(group_holder, fields_holder):
            for name in sorted(group_holder.keys()):
                for decl in group_holder[name]:
                    decl_no_assign = copy.deepcopy(decl)
                    if hasattr(decl_no_assign, '_assign_expr'):
                        delattr(decl_no_assign, '_assign_expr')

                    fields_holder.append(decl_no_assign)


        instance_struct_ctype = nodes.ComposedType('kc_' + klass.name + '_instance')
        instance_struct_ctype._specifier = nodes.Specifiers.STRUCT
        instance_struct_ctype.fields = []

        # assemble struct fields (instance member variables)
        for parent_name in klass.parents:
            members = klass.parents_members[parent_name]
            add_decl_fields_from_group(members, instance_struct_ctype.fields)


        add_decl_fields_from_group(klass.members, instance_struct_ctype.fields)

        return nodes.Decl('', instance_struct_ctype)

    # build class interface
    #--------------------------------
    def build_interface_struct(self, klass):

        interface_struct_ctype = nodes.ComposedType('kc_' + klass.name + '_interface')
        interface_struct_ctype._specifier = nodes.Specifiers.STRUCT
        interface_struct_ctype.fields = []

        # meta field
        meta_ctype = nodes.PrimaryType('kc_' + klass.name + '_metadata')
        meta_ctype.push(nodes.PointerType())
        interface_struct_ctype.fields.append(nodes.Decl('meta', meta_ctype))

        # instance field
        instance_ctype = nodes.PrimaryType('kc_' + klass.name + '_instance')
        interface_struct_ctype.fields.append(nodes.Decl('instance', instance_ctype))

        return nodes.Decl('', interface_struct_ctype)



# KcClass after ClassBuilder pass

# - body: ?
#
# - members:
#     'my_var' => [decl1, decl2]
#     'age' => [decl3] ( decl3 is just PrimaryType('int') )
#
# - methods:
#     'my_func' => [decl4]
#     'do_something' => [decl5, decl6]
#
# - virtuals:
#     'isKindOf' => [decl7, decl8]
#
