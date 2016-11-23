#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

class KoocTestEntry:
    tests = []
    okString = '[\033[92mPASSED\033[0m]'
    failString = '[\033[91mFAILED\033[0m]'
    separator = "\n------------------------------------------\n"

    def __init__(self, testName, kcFileName, input, expectedOutput):
        self.testName = testName
        self.kcFileName = kcFileName
        self.input = input
        self.expectedOutput = expectedOutput
        
        self.koocRet = None
        self.kookOutput = None
        self.ccRet = None
        self.ccOutput = None
        self.ret = None
        self.output = None

        KoocTestEntry.tests.append(self)

    def run(self, koocBin, ccBin):
        koocRes = Popen([koocBin, self.kcFileName], stdout=PIPE, stderr=PIPE)
        self.koocOutput = koocRes.communicate()
        self.koocRet = koocRes.returncode
        cFile = NamedTemporaryFile()
        cFile.write(self.koocOutput[0])        
        ccRes = Popen([ccBin, cFile.name], stdout=PIPE, stderr=PIPE)
        self.ccOutput = ccRes.communicate()
        self.ccRet = ccRes.returncode
        res = None
        if self.input != None:
            res = Popen(["echo \"" + self.input + "\"" + " | ./a.out"], stdout=PIPE, stderr=PIPE, shell = True)
        else:
            res = Popen(["./a.out"], stdout=PIPE, stderr=PIPE, shell = True)    
        self.output = res.communicate()
        self.ret = res.returncode

        cFile.close()
        pass

    @staticmethod
    def runAll(koocBin, ccBin):
        for test in KoocTestEntry.tests:
            test.run(koocBin, ccBin)
            test.assert_transpiled()
            test.assert_compiled()
            test.assert_executed()
            test.assert_output()
            print(KoocTestEntry.separator)

    def assert_transpiled(self):
        if self.koocRet:
            print("{result} {name}: transpilation failed with status {status}\n{cause}".format(
                result = KoocTestEntry.failString,
                name = self.testName,
                status = self.koocRet,
                cause = self.koocOutput[1]
            ))
        else:
            print("{result} {name}: transpilation".format(
                result = KoocTestEntry.okString,
                name = self.testName
            ))

    def assert_compiled(self):
        if self.ccRet:
            print("{result} {name}: compilation failed with status {status}\n{cause}".format(
                result = KoocTestEntry.failString,
                name = self.testName,
                status = self.ccRet,
                cause = self.ccOutput[1]
            ))
        else:
            print("{result} {name}: compilation".format(
                result = KoocTestEntry.okString,
                name = self.testName
            ))

    def assert_executed(self):
        if self.ret:
            print("{result} {name}: execution failed with status {status}\n{cause}".format(
                result = KoocTestEntry.failString,
                name = self.testName,
                status = self.ret,
                cause = self.output[1]
            ))
        else:
            print("{result} {name}: execution".format(
                result = KoocTestEntry.okString,
                name = self.testName
            ))

    def assert_output(self):
        if self.output[0] != self.expectedOutput:
            print("{result} {name}: output does not match\n\"{expect}\"!=\"{cause}\"".format(
                result = KoocTestEntry.failString,
                name = self.testName,
                cause = self.output[0],
                expect = self.expectedOutput
            ))

KoocTestEntry("basic", "basic_test.kc", None, "hello wolrd !")
KoocTestEntry("type", "typage_test.kc", None, "42 0.1337 42.1337");
KoocTestEntry.runAll("../../koocexe", "cc")
