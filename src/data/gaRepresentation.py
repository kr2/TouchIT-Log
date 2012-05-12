#License: BSD 2-clause license


""" grouaddr representataion
"""
__version__ = '1.0'
_debug = 0

import dptInterpreter


### Reader base class
class GAdata(object):

    NotReadyForPrinting = "The data is not ready for printing."

    def __init__(self):

        self.__dpt = None  # this is
        self.__length = None # in bit

        self.__eis = None # [1..15] if it is set it is used for data interpretion but it is updated if length or dpt is changed

        self.possibleDpt = []

        self.gaName = "Unknown"
        self.gaStr = ""
        self.gaBin = 0

        self.mainMidGAName = "Unknown"    ## DEPRECATED use gaNameList
        self.gaNameList = []

        self.data = [] # [timedata, rawData]
        self.interpretedData = [] # [timedata, interpreted data]

        self._isInterpreted = False

        self.iterCount = 0

    def getDpt(self):
        return self.__dpt
    def setDpt(self, value):
        oldDpt = self.__dpt
        self.__dpt = value

        if oldDpt != value and self.data != []:
            self._isInterpreted = False
            self.interpret();
    def delDpt(self):
        del self.__dpt
    dpt = property(getDpt, setDpt, delDpt)


    def getlength(self):
        return self.__length
    def setlength(self, value):
        oldLenght = self.__length
        self.__length = value

        if self.__dpt == None and self.__eis == None:
            self.__dpt = dptInterpreter.getDPT(dpt = None, eis=self.__eis, length = value)


        if oldLenght != value and self.data != []:
            self._isInterpreted = False
            self.interpret();
    def dellength(self):
        del self.__length
    length = property(getlength, setlength, dellength)


    def getEis(self):
        return self.__eis
    def setEis(self, value):
        oldEis = self.__eis
        self.__eis = value

        if self.__dpt == None:
            self.__dpt = dptInterpreter.getDPT(dpt = None, eis=value, length = self.__length)

        # interpret if necceary
        if oldEis != value and self.data != []:
            self._isInterpreted = False
            self.interpret();
    def delEis(self):
        del self.__eis
    eis = property(getEis, setEis, delEis)


#/*--------------------------------------+-------------------------------------*/


    def interpret(self):
        self.interpretedData = []
        for dataPoint in self.data:
            self.interpretedData.append(
                [
                dataPoint[0],
                dptInterpreter.interpret(dataPoint[1], dpt = self.__dpt, eis= self.__eis, length = self.__length)
                ])

        # sort data by time
        self.interpretedData.sort(key=lambda x: x[0])

        self.possibleDpt = dptInterpreter.getPosibleDPT(self.__length)

        if self.__dpt == None:
            self.__dpt = dptInterpreter.lengthDefaultDPT[self.__length]

        self._isInterpreted = True


    def next(self):
        if not self._isInterpreted:
            raise Exception(GAdata.NotReadyForPrinting)

        if self.iterCount >= len(self.interpretedData):
            self.iterCount = 0
            raise StopIteration
        else:
            c = self.iterCount
            self.iterCount = c + 1
            return self.interpretedData[c]

    def __getitem__(self, item):
        if self._isInterpreted:
            return self.interpretedData[item]
        else:
            raise Exception(GAdata.NotReadyForPrinting)

    def __iter__(self):
        return self

    def __del__(self):
        del(self.data)
        del(self.interpretedData)

    def __len__(self):
        if not self._isInterpreted:
            raise Exception(GAdata.NotReadyForPrinting)
        return len(self.printData)

    def __str__(self):
        ret = ""
        if not self._isInterpreted:
            raise Exception(GAdata.NotReadyForPrinting)
        else:
            ret += '=== {0} === \n{1} ({2}) \nEIS {3} ({4} bit) \n \n'.format(self.gaStr, self.gaName, self.mainMidGAName,self.eis, self.length)

            for printDataPoint in self.interpretedData:
                time =  printDataPoint[0].strftime("%d.%m.%Y %H:%M:%S.%f")
                ret = ret + '{0} | {1} \n'.format(time, printDataPoint[1])
        return ret


def _test():
    print "test not defined"



if __name__ == '__main__':
    _test()
