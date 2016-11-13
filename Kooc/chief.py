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

    def __init__(self, fpath_in):
        self.file_in = fpath_in

        self.header = False
        self.source = False
        if fpath_in[-3:] == '.kh':
            self.header = True
        else:
            self.source = True

    # later: split this function
    def run(self):
        from Kooc.directive import Directive
        parser = Directive()

        # get AST: parse file
        ast = parser.parse_file(self.file_in)
        print("====== AST ======")
        print(ast.to_yml())
        print("==== END AST ====")
        return ""

        # pass some visitors...

        # get c_ast:
        if self.header:
            # - generate function prototypes
            # - generate extern variable declarations
            pass
        if self.source:
            # - generate module variable definition
            pass
        c_ast = ast # make a copy ?
        # cleanup c_ast to remove all kooc mentions
        return c_ast.to_c()


class ChiefKooc:
    """This is the koocer manager, it knows what to do and distribute work"""

    def __init__(self, files = None):
        self.verbose = None
        self.debug = None
        self.files = []
        if files:
            self.load_files(files)

    def load_files(self, files):
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

    def run(self):
        for fpath_in in self.files:
            print()
            print("====================================")
            print("Processing file '" + fpath_in + "'")
            print()

            koocer = Koocer(fpath_in)
            result_c_code = koocer.run()

            print("#    Result C code:   #")
            print(result_c_code)


