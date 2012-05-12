#License: BSD 2-clause license

""" opc reader
"""
__version__ = '1.0'
_debug = 0


import csv
import KNXAddressInterpreter

### Reader base class

class Reader(object):

    NotInterpretedExeptionMessage = "The values are not interpreted, they are only raw data."

    def __init__(self, file):

        # List of telegrams, each being a list of strings
        self.rawLines = []

        # List of telegrams, each being a list. Only valid if interpret all ist done.
        # [0 addr (2 Byte bin),1 MainGroupName.MidGroupName,2 SubGroupName,3 addrString,4 EIS,5 DPT,6 Length,7 Prioity]
        self.interpretedLines = []

        self.ProjectName = None

        self._isInterpeted = False

        self._load(file)
        self._interpret()


        self.iterCount = 0


    def _flush(self):
        """ Empty the object and reset errors
        """
        self.rawLines = []
        self.interpretedLines = []

    def __utf_8_encoder(self,unicode_csv_data):
        for line in unicode_csv_data:
            yield unicode(line, errors='ignore')

    def _load(self, file):
        if isinstance(file, basestring):
            f = open(file,'rb')
        else:
            f = file

        f = self.__utf_8_encoder(f)
        try:
            opcfile = csv.reader(f, delimiter='\t')
            for row in opcfile:
                self.rawLines.append(row);
            self.ProjectName = self.rawLines[0][0]
            del(self.rawLines[0])
        finally:
            f.close()
        #print "name: " + self.ProjectName
        #print self.rawLines


    # representation
    # tab seperated
    # MainGroupName.MidGroupName.MainGroupNr/MidGroupNr/SubGroupNr  SubGroupName    DataType (Length)   Pryority
    def _interpret(self):
        for rawLine in self.rawLines:

            groupNameing = rawLine[0].split( '.' )
            addrNrStr = groupNameing[-1]
            MainMidGroupName = ".".join(groupNameing[0:-1])
            SubGroupName = rawLine[1]

            datatype = rawLine[2].split(' (')
            lengthStr = datatype[1][:-1].split(' ')
            if lengthStr[1] == "Byte":
                length = int(lengthStr[0]) * 8
            else:
                length = int(lengthStr[0])

            if datatype[0] != "Uncertain":
                temp = datatype[0].split(' ')
                EIS = int(temp[1])
                DPT = temp[2]
            else:
                EIS = None
                DPT = None

            self.interpretedLines.append([
                    self.__interpAddr(addrNrStr), # addr 2 byte bin
                    MainMidGroupName, #  MainGroupName.MidGroupName
                    SubGroupName, # SubGroupName
                    addrNrStr, # addrString
                    EIS, # EIS
                    DPT, # DPT
                    length, # Length
                    rawLine[3] # Prioity
                ])
        self._isInterpeted = True

    def getDictionary(self):
        """retuns dictionara with the bin sourcaddr as key
        """
        dictonary = {}

        for x in self.interpretedLines:
            dictonary[x[0]] = x
        return dictonary

    def __interpAddr(self,addrStr):
        return KNXAddressInterpreter.str2int(addrStr)

    def next(self):
        if not self._isInterpeted:
            raise Exception(Reader.NotInterpretedExeptionMessage)

        if self.iterCount >= len(self.interpretedLines):
            self.iterCount = 0
            raise StopIteration
        else:
            c = self.iterCount
            self.iterCount = c + 1
            return self.interpretedLines[c]

    def __getitem__(self, item):
        if not self._isInterpeted:
            raise Exception(Reader.NotInterpretedExeptionMessage)

        return self.interpretedLines[item]

    def __iter__(self):
        return self

    def __del__(self):
        self._flush()
        del(self.interpretedLines)
        del(self.rawLines)

    def __len__(self):
        return len(self.rawTelegrams)

    def __str__(self):
        ret = ""
        if not self._isInterpeted:
            raise Exception(Reader.NotInterpretedExeptionMessage)
        else:
            for line in self.interpretedLines:
                ret = ret + '{0:5} | {1:20} | {2:20} | {3:5} | {4:5} | {5:5} | {6:5} | {7:5} \n'.format(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
        return ret


def _test():
   #testFile = "TestData//CO2_und_TEMPERATUR.esf"
    testFile = "ExampleData//MesseTafeln.esf"
    testReader = Reader(testFile)

    print str(testReader)

   # for test in testReader:
       # print test

   # print testReader[1]

    #print testReader.getDictionary()

    #for i in xrange(1,100):
        #print testReader.interprTelegrams[i]



if __name__ == '__main__':
    _test()
