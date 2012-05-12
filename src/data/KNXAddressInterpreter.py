#License: BSD 2-clause license


""" KNX addres interpreter
"""
__version__ = '1.0'
_debug = 0

def str2int(addrStr, sep='/'):
    if _debug==1: print addrStr

    splitAddStr = addrStr.split(sep)

    if _debug==1: print splitAddStr

    if len(splitAddStr) == 3:
        ret = int(splitAddStr[2]) << 8 # sub
        ret |= int(splitAddStr[0]) << 3 # main
        ret |= int(splitAddStr[1]) #mid
    elif len(splitAddStr) == 2:
        ret = int(splitAddStr[1])  # sub
        ret |= int(splitAddStr[0]) << 8 # main
    else:
        ret = (int(splitAddStr[0])  >> 8) & int('0b0000000001111111',2)
        ret |= (int(splitAddStr[0]) << 8) & int('0b1111111100000000',2)

    return ret

def int2str(addrInt ,outType = "3stage", sep='/'):
    """ outType == 3stage or 2stage or 1stage
    """
    ret = []

    if outType == "3stage":
        ret.append( (addrInt & int('0b0000000001111000',2)) >> 3 ) # main
        ret.append( (addrInt & int('0b0000000000000111',2)) ) # mid
        ret.append( (addrInt & int('0b1111111100000000',2)) >> 8 ) #sub
        if _debug == 2:
            print '+++++++++++'
            print addrInt
            print ret
            print '+++++++++++'
    elif outType == "2stage":
        ret.append( (addrInt & int('0b0000000001111111',2)) ) # main
        ret.append( (addrInt & int('0b1111111100000000',2)) >> 8 ) #sub
    elif outType == "1stage":
        temp  = (addrInt & int('0b0000000001111111',2)) << 8
        temp |= (addrInt & int('0b1111111100000000',2)) >> 8
        return str( temp )
    else:
        raise Exception("out stage type not defined")

    return sep.join([str(i) for i in ret])

def split(addrStr,sep='/'):
    """ Splits addr string and returns array with int2str
    """
    temp =  addrStr.split(sep)
    return [int(i) for i in temp]

def compare(a,b):
    _a = int2str(a ,outType = "1stage", sep='/')
    _b = int2str(b ,outType = "1stage", sep='/')
    if int(_a) > int(_b):
        return 1
    elif int(_a) < int(_b):
        return -1
    else:
        return 0

def _test():
    print "no test defined"


if __name__ == '__main__':
    _test()
