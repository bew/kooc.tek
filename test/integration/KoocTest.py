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
        self.koocRet = koocRes.returnCode
        
        cFile = NamedTemporaryFile()
        cFile.write(self.koocOutput)

        ccRes = Popen([ccBin, cFile.name], stdout=PIPE, stderr=PIPE)
        self.ccOutput = ccRes.communicate()
        self.ccRet = ccRes.returnCode
        
        res = Popen(["echo \"" + input + "\"" + " | ./a.out"], stdout=PIPE, stderr=PIPE, shell = True)
        self.output = res.communicate()
        self.ret = res.returnCode

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

    def assert_transpiled():
        if not self.koocRet:
            print("{result} {name}: transpilation failed with status {status}\n{cause}".format(
                result = KoocTestEntry.failString,
                name = self.testnName,
                status = self.koocRet,
                cause = self.koocOutput[1]
            ))
        else:
            print("{result} {name}: transpilation".format(
                result = KoocTestEntry.okString,
                name = self.testName
            ))

    def assert_compiled():
        if not self.ccRet:
            print("{result} {name}: compilation failed with status {status}\n{cause}".format(
                result = KoocTestEntry.failString,
                name = self.testnName,
                status = self.ccRet,
                cause = self.ccOutput[1]
            ))
        else:
            print("{result} {name}: compilation".format(
                result = KoocTestEntry.okString,
                name = self.testName
            ))

    def assert_executed():
        if not self.ret:
            print("{result} {name}: execution failed with status {status}\n{cause}".format(
                result = KoocTestEntry.failString,
                name = self.testnName,
                status = self.ret,
                cause = self.output[1]
            ))
        else:
            print("{result} {name}: execution".format(
                result = KoocTestEntry.okString,
                name = self.testName
            ))

    def assert_output():
        if self.output[0] != self.expectedOutput:
            print("{result} {name}: output does not match\n{cause}".format(
                result = KoocTestEntry.failString,
                name = self.testnName,
                cause = self.output[0]
            ))

KoocTestEntry("basic", "basic_test.kc", "", "hello wolrd !")
KoocTestEntry.runAll("../../koocexe", "cc")