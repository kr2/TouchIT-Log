#License: BSD 2-clause license


""" log reader
"""
__version__ = '1.0'
_debug = 0


import struct
import datetime


### Reader base class
class Reader(object):

    NotInterpretedExeptionMessage = "The values are not interpreted, they are only raw binaray data. call interpret"

    def __init__(self, file):
        if _debug == 2:
            print '##############New File #####################'
            print file
        # List of telegrams, each being a list of strings
        self.rawTelegrams = []

        # List of telegrams, each being a list. Only valid if interpret all ist done.
        # [time, source (2 Byte Plain), dest (2 Byte Plain) , length, data]
        self.interprTelegrams = []


        self._isInterpeted = False

        self._load(file)


        self.iterCount = 0


    def _flush(self):
        """ Empty the object and reset errors
        """
        self.rawTelegrams = []
        self.interprTelegrams = []

    def _load(self, file, chunksize=16):
        if isinstance(file, basestring):
            f = open(file,'rb')
        else:
            f = file
        try:
            rawTeleg = f.read(chunksize)
            while rawTeleg != b"":
                self.rawTelegrams.append(rawTeleg)
                rawTeleg = f.read(chunksize)
        finally:
            f.close()

        if _debug == 2:
            print self.rawTelegrams[0].encode("hex")
            print self.rawTelegrams[-1].encode("hex")
            print len(self.rawTelegrams)

    # returns bit
    realLengthLookUp = {
        0: None,  # for telegrams with two parts (the second telegram hat length = 0)
        1: 1,
        2: 1*8,
        3: 2*8,
        4: 3*8,
        5: 4*8,
        15: 14*8

    }
    # representation of an Telegram
    # byte
    # 1   time
    # 2   time
    # 3   time
    # 4   time
    # 5   sourc addr
    # 6   sourc addr
    # 7   dest addr
    # 8   dest addr
    # 9.1 [lower nibble] milliseconds
    # 9.2 [upper nibble] length
    # 10  Data
    # 11  Data
    # 12  Data
    # 13  Data
    # 14  Data
    # 15  Data
    # 16  Data
    def interpret(self):
        s = struct.Struct('I H H B 7s')
        i = 0
        for telegramm in self.rawTelegrams:
            data = s.unpack(telegramm)

            tenthSeconds = (int('0b11110000', 2) & data[3]) >> 4
            length = (int('0b00001111', 2) & data[3] )
            if length in Reader.realLengthLookUp:
                realLength = Reader.realLengthLookUp[length]
            else:
                if _debug: print 'length not in tabel realLengthLookUp:' + str(length)
                continue
                #realLength = lenght

            # todo data interpretion with sourcaddr
            self.interprTelegrams.append(
                [
                    #datetime.timedelta( milliseconds = (data[0] * 1000 + tenthSeconds * 100) ), # time
                    datetime.datetime.fromtimestamp( float(data[0]) + float(tenthSeconds)/10), # time
                    data[1], # source
                    data[2], # dest
                    realLength, # length
                    data[4]  # data
                ])
            i += 1
            if realLength == None and _debug == 2:
                print '---------START-------------'
                print 'length == none @: ' + str(i)
                print length
                print telegramm.encode("hex")
                print self.interprTelegrams[-1]
                print '----------END--------------'


        if _debug == 2:
            print self.interprTelegrams[0]
            print self.interprTelegrams[-1]
            print len(self.interprTelegrams)
        # check if length is 0xF and append data
        i = 0
        delList = []
        while i < len(self.interprTelegrams):
            if self.interprTelegrams[i][3] > 7*8:
                self.interprTelegrams[i][4] += self.interprTelegrams[i+1][4]
                i += 1
                delList.append(i)
            i +=1

        if _debug==1: print len(self.interprTelegrams)
        delList.sort( reverse=True) ## sort reverse since else the indes would be wrong if elements were deleated
        if _debug==1: print str(delList)
        for x in delList:
            del(self.interprTelegrams[x])
        if _debug==1: print len(self.interprTelegrams)

        self._isInterpeted = True

    def next(self):
        if not self._isInterpeted:
            raise Exception(Reader.NotInterpretedExeptionMessage)

        if self.iterCount >= len(self.interprTelegrams):
            self.iterCount = 0
            raise StopIteration
        else:
            c = self.iterCount
            self.iterCount = c + 1
            return self.interprTelegrams[c]


    def __getitem__(self, item):
        if self._isInterpeted:
            return self.interprTelegrams[item]
        else:
            raise Exception(Reader.NotInterpretedExeptionMessage)

    def __iter__(self):
        return self

    def __del__(self):
        self._flush()
        del(self.rawTelegrams)
        del(self.interprTelegrams)

    def __len__(self):

        return len(self.rawTelegrams)

    def __str__(self):
        ret = ""
        if not self._isInterpeted:
            raise Exception(Reader.NotInterpretedExeptionMessage)
        else:
            for telegram in self.interprTelegrams:
                time =  telegram[0].strftime("%d.%m.%Y %H:%M:%S.%f")
                ret = ret + '{0} | {1:4} | {2:4} | {3:2} | {4} \n'.format(time, telegram[1],telegram[2], telegram[3], telegram[4].encode("hex"))
        return ret


def _test():
    testFile = "TestData//15447"
    # testFile = "ExampleData//15313"
    testReader = Reader(testFile)

    testReader.interpret()

    print str(testReader)

    #for temp in testReader:
     #   print temp

    #print testReader[1]

    #for i in xrange(1,100):
        #print testReader.interprTelegrams[i]



if __name__ == '__main__':
    _test()
