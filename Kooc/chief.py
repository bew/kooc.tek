import os
import subprocess

from Kooc.utils import KError, KUnsupportedFeature
from Kooc.passes.visitors import VisitorRunner


class KLoadingError(KError):
    """There were errors when loading files in Kooc"""

    def __init__(self, errors):
        KError.__init__(self, 'Cannot load files, see .errors for the list')
        self.errors = errors



class KBadExtensionError(KError):
    """The given file extension is not supported"""

    def __init__(self, file_path):
        KError.__init__(self, 'Bad file extension of file \'{}\', must be .kc or .kh'.format(file_path))
        self.file_path = file_path


def apply_visitors(ast):
    vr = VisitorRunner(ast)

    # pass some visitors...
    # - bind implem to module/class
    vr.bind_implem()

    # - resolve context type in call/lookup (before/after ast typing ?)
    vr.resolve_expr_context()

    # - apply expr_type from C cast (This could be done in full typing system)
    vr.type_c_cast()

    # - type the AST

    pass


class Koocer:
    """Where shit happens"""

    cache_ast = {}

    def __init__(self, source_file_path):
        self.source_file = source_file_path
        self.source_code = None
        self.ast = None

        # is there cache for this file ?
        if self.source_file in Koocer.cache_ast:
            self.ast = Koocer.cache_ast[self.source_file]

    def preprocess(self):
        cpp_options = ['cpp']

        try:
            cpp_options.extend([self.source_file])
            output = subprocess.check_output(cpp_options)
            self.source_code = output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            raise KError('Cannot pass \'cpp\' preprocessor on ' + self.source_file + ' : ' + str(e))

    def parse(self):
        if self.ast:
            return

        if not self.source_code:
            self.preprocess()

        from Kooc.directive import Directive
        parser = Directive(Koocer)

        self.ast = parser.parse(self.source_code, os.path.dirname(self.source_file))

        # Cache the ast for future use and to keep AST (k)types alive
        Koocer.cache_ast[self.source_file] = self.ast

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


