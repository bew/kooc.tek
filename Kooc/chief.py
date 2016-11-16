from Kooc.utils import KError, KUnsupportedFeature

class KLoadingError(KError):
    """There were errors when loading files in Kooc"""

    def __init__(self, errors):
        """TODO: to be defined1. """

        KError.__init__(self, 'Cannot load files, see .errors for the list')
        self.errors = errors



class KBadExtensionError(KError):
    """The given file extension is not supported"""

    def __init__(self, file_path):
        """TODO: doc"""

        KError.__init__(self, 'Bad file extension of file \'{}\', must be .kc or .kh'.format(file_path))
        self.file_path = file_path


from Kooc.passes.visitors import VisitorRunner

def apply_visitors(ast):
    vr = VisitorRunner(ast)

    # pass some visitors...
    # - bind implem to module/class
    vr.bind_implem()

    # - resolve context type in call/lookup (before/after ast typing ?)
    vr.resolve_expr_context()

    # - apply expr_type from C cast (This could be done in full typing system)
    vr.type_c_cast()

    # - add parent (allow reverse traversal)
    #visit_add_parents(ast)

    # - type the AST


    # VISITOR DESIGN
    # -> need a generator on all KcExpr of the AST
    #    (ex: for KcLookup to resolve context type)
    #
    # -> need something else for the visitor 'resolve_type'
    pass


class Koocer:
    """Where shit happens"""

    def __init__(self, source_file_path):
        self.source_file = source_file_path
        self.ast = None

    def parse(self):
        if self.ast:
            return

        from Kooc.directive import Directive
        parser = Directive()

        self.ast = parser.parse_file(self.source_file)

    def run(self):
        self.parse()

        # TODO: print() -> log.verbose()
        #print("====== AST ======")
        #print(self.ast.to_yml())
        #print("==== END AST ====")

        apply_visitors(self.ast)

        # TODO: log.debug(self.ast.to_yml())
        print("====== AST after visitors ======")
        print(self.ast.to_yml())
        print("==== END AST after visitors ====")

        from Kooc.passes import to_c
        return self.ast.to_c()


class ChiefKooc:
    """This is the koocer manager, it knows what to do and distribute work"""

    def __init__(self, files = None, just_parse = False):
        self.just_parse = just_parse
        self.verbose = None
        self.debug = None
        self.files = []
        if files:
            self.load_files(files)

    def load_files(self, files):
        if self.just_parse:
            self.files = files
            return True

        file_errors = []

        for fpath in files:
            if fpath == '-':
                file_errors.append(KUnsupportedFeature('Load source from stdin'))
                continue

            try:
                # try to open/read file
                fhandle = open(fpath, 'r')
                fhandle.close()
            except OSError as e:
                file_errors.append(e)
                continue

            if not (fpath[-3:] == '.kh' or fpath[-3:] == '.kc'):
                file_errors.append(KBadExtensionError(fpath))
                continue


            self.files.append(fpath)

        if len(file_errors) > 0:
            raise KLoadingError(file_errors)

        return True

    def nb_valid_files(self):
        return len(self.files)

    # FIXME: this function should return a dict of (file => ast)
    def run_just_parse(self):
        for fpath in self.files:
            print()
            print("====================================")
            print("Processing file '" + fpath + "'")
            print()

            koocer = Koocer(fpath)
            koocer.parse()

            print("#    AST    #")
            print(koocer.ast.to_yml())

    def run(self):
        if self.just_parse:
            self.run_just_parse()
            return

        # TODO: move this in other function
        for fpath_in in self.files:
            print()
            print("====================================")
            print("Processing file '" + fpath_in + "'")
            print()

            koocer = Koocer(fpath_in)
            result_c_code = koocer.run()

            print()
            print("#    Result C code:   #")
            print(result_c_code)


