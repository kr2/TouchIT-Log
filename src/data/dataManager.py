#License: BSD 2-clause license

""" data Manager
"""
__version__ = '1.0'
_debug = 0

import opcReader
import logReader

import gaRepresentation
import KNXAddressInterpreter


class DataManager(object):
    def __init__(self, logFiles, opcFiles):
        self.projectName = "Unknown"
        self.opcDictonary = {}  # {binGAadd:[,,,]}

        self.gaRepDictonary = {}  # {binGAadd:[,,,]}

        self.__readOpcs(opcFiles)
        self.__readLogs(logFiles)

        for key in self.gaRepDictonary.keys():
            self.gaRepDictonary[key].interpret()

    def __readOpcs(self, opcFiles):
        for opcFile in opcFiles:
            opcR = opcReader.Reader(opcFile)
            for gaLine in opcR:
                self.opcDictonary[gaLine[0]] = gaLine

            if opcR.ProjectName != None:
                self.projectName = opcR.ProjectName

    def __readLogs(self, logFiles):
        for logfile in logFiles:
            logR = logReader.Reader(logfile)
            logR.interpret()

            for telegramm in logR:
                if not (telegramm[2] in self.gaRepDictonary):
                    self.__newGaRepDictEntry(telegramm)
                self.__addTelegramToGaRepDict(telegramm)

    def __addTelegramToGaRepDict(self, telegramm):
        opcKey = telegramm[2]
        self.gaRepDictonary[opcKey].data.append([telegramm[0], telegramm[4]])

    def __newGaRepDictEntry(self, telegramm):
        opcKey = telegramm[2]
        gaRep = gaRepresentation.GAdata()
        if opcKey in self.opcDictonary:
            gaRep.eis           = self.opcDictonary[opcKey][4]
            gaRep.length        = self.opcDictonary[opcKey][6]
            gaRep.gaName        = self.opcDictonary[opcKey][2]
            gaRep.gaStr         = self.opcDictonary[opcKey][3]
            gaRep.gaBin         = self.opcDictonary[opcKey][0]
            gaRep.mainMidGAName = self.opcDictonary[opcKey][1]

            gaRep.gaNameList.extend(self.opcDictonary[opcKey][1].split('.'))
            gaRep.gaNameList.extend([self.opcDictonary[opcKey][2]])

        else:
            gaRep.eis           = None
            gaRep.length        = telegramm[3]
            gaRep.gaName        = "Unknown"
            gaRep.gaStr         = KNXAddressInterpreter.int2str(telegramm[2])
            gaRep.gaBin         = telegramm[2]
            gaRep.mainMidGAName = "Unknown"
            gaRep.gaNameList    = ['Unknown', 'Unknown', 'Unknown']


        self.gaRepDictonary[opcKey] = gaRep

    def getSortedKeys(self):
        keys = self.gaRepDictonary.keys()
        if _debug: print keys
        if _debug: print KNXAddressInterpreter.compare(keys[0], keys[1])
        if _debug: print KNXAddressInterpreter.compare(keys[1], keys[0])
        keys.sort(cmp=KNXAddressInterpreter.compare)
        if _debug: print keys
        return keys




def _test():
    # logFiles = [
    #         "TestData//15446",
    #         "TestData//15447",
    #         "TestData//15448",
    #         "TestData//15449"
    #     ]
    logFiles = [
            "ExampleData//15313",
            "ExampleData//15311",
            "ExampleData//15310",
            "ExampleData//14583",
            "ExampleData//14582",
            "ExampleData//15309"
        ]
    # ocpFiles = ["TestData//CO2_und_TEMPERATUR.esf"]
    ocpFiles = ["ExampleData//MesseTafeln.esf"]

    outDir = './out//'

    dm = DataManager(logFiles, ocpFiles)


    overalDatapoints = 0

    for key in dm.gaRepDictonary.keys():
        print str(dm.gaRepDictonary[key])
        overalDatapoints += len(dm.gaRepDictonary[key].interpretedData)

    print overalDatapoints

    # gaCsvExport.compleatExport(outDir,dm.gaRepDictonary.values(), projectName = dm.projectName, oneFile = False)
    # gaCsvExport.compleatExport(outDir,dm.gaRepDictonary.values(), projectName = dm.projectName, oneFile = True)

if __name__ == '__main__':
    _test()