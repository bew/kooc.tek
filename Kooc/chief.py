import os
import subprocess

from Kooc.utils import KError, KUnsupportedFeature
from Kooc.passes import visitors



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

        file_dirname = os.path.dirname(self.source_file)
        if len(file_dirname) > 0:
            file_dirname += '/'
        self.ast = parser.parse(self.source_code, file_dirname)

        # Cache the ast for future use and to keep AST (k)types alive
        Koocer.cache_ast[self.source_file] = self.ast


    def apply_visitors(self):
        runners = [
                visitors.linkchecks.LinkChecks(Koocer),

                #visitors.types.ModuleBuilding(),
                #visitors.types.ClassBuilding(),

                #last: type the AST
                visitors.typing.Typing(),
                ]

        # Register all visitors
        for r in runners:
            r.register()

        # Run
        for r in runners:
            r.run(self.ast)


    def run(self):
        self.parse()

        # TODO: print() -> log.verbose()
        #print("====== AST ======")
        #print(self.ast.to_yml())
        #print("==== END AST ====")

        # pass some visitors...
        self.apply_visitors()

        # TODO: log.debug(self.ast.to_yml())
        print("====== AST after visitors ======")
        print(self.ast.to_yml())
        print("==== END AST after visitors ====")

        from Kooc.passes import to_c
        return self.ast.to_c()


class ChiefKooc:
    """This is the koocer manager, it knows what to do and distribute work"""

    def __init__(self, files = None, just_parse = False, write_c = True):
        self.just_parse = just_parse
        self.write_c = write_c
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

            if not self.get_out_path(fpath):
                file_errors.append(KBadExtensionError(fpath))
                continue


            self.files.append(fpath)

        if len(file_errors) > 0:
            raise KLoadingError(file_errors)

        return True

    def nb_valid_files(self):
        return len(self.files)

    def get_out_path(self, file_in):
        ext = file_in[-3:]
        no_ext = file_in[:-3]

        if ext == '.kh':
            return no_ext + '.h'
        elif ext == '.kc':
            return no_ext + '.c'
        else:
            return False

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

            if self.write_c:
                fpath_out = self.get_out_path(fpath_in)
                handle_out = open(fpath_out, 'w')
                handle_out.write(str(result_c_code))
                handle_out.close()

            print()
            print("#    Result C code:   #")
            print(result_c_code)


