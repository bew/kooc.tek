from Kooc.utils import KError

class KLoadingError(KError):
    """There were errors when loading files in Kooc"""

    def __init__(self, errors):
        """TODO: to be defined1. """

        KError.__init__(self)
        self.errors = errors



class KBadExtensionError(KError):
    """The given file extension is not supported"""

    def __init__(self, file_path):
        """TODO: doc"""

        KError.__init__(self)
        self.file_path = file_path



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

    def apply_visitors(self):
        # pass some visitors...
        # - bind implem to module/class
        # - type the AST

        # - resolve context type in call/lookup (before/after ast typing ?)

        # VISITOR DESIGN
        # -> need a generator on all KcExpr of the AST
        #    (ex: for KcLookup to resolve context type)
        #
        # -> need something else for the visitor 'resolve_type'
        pass

    def run(self):
        self.parse()
        ast = self.ast

        # TODO: print() -> log.debug()
        print("====== AST ======")
        print(ast.to_yml())
        print("==== END AST ====")

        self.apply_visitors()

        from Kooc.passes import to_c
        return ast.to_c()


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
            if not (fpath[-3:] == '.kh' or fpath[-3:] == '.kc'):
                file_errors.append(KBadExtensionError(fpath))
                continue

            try:
                fhandle = open(fpath, 'r')
                fhandle.close()
            except OSError as e:
                file_errors.append(e)
                continue

            self.files.append(fpath)

        if len(file_errors) > 0:
            raise KLoadingError(file_errors)

        return True

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

            print("#    Result C code:   #")
            print(result_c_code)


