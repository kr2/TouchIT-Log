#License: BSD 2-clause license


""" dpt interpreter
"""
__version__ = '1.0'
_debug = 0



#EIS datentypen:
# Schalter          | 1 Bit   | EIS 1  | DPT 1        | DONE  | u_int1
# Dimmer            | 4 Bit   | EIS 2  | DPT 3        | TODO  | string
# Zeit              | 3 Byte  | EIS 3  | DPT 10       | TODO  |
# Datum             | 2 Byte  | EIS 4  | DPT 11       | TODO  |
# Gleitkomma        | 2 Byte  | EIS 5  | DPT 9        | DONE  | float16
# Relativwert       | 1 Byte  | EIS 6  | DPT 5 & 6    | TODO  | u_int8
# Jallousi/rollade  | 1 Bit   | EIS 7  | DPT 1        | TODO  | u_int1
# Zwanssteuerung    | 2 Byte  | EIS 8  | DPT 2        | TODO  |
# IEEE Gleitkomma   | 4 Byte  | EIS 9  | DPT 14       | TODO
# 16 Bit Zaehlerwert | 2 Byte  | EIS 10 | DPT 7 & 8    | TODO
# 32 Bit Zaehlerwert | 4 Byte  | EIS 11 | DPT 12 & 13  | TODO
# Zugangskontrolle  | 4 Byte  | EIS 12 | DPT 15       | TODO
# ASCII Zeichen     | 1 Byte  | EIS 13 | DPT 4        | TODO
# 8 Bit Zaehlerwert  | 1 Byte  | EIS 14 | DPT 5 & 6    | TODO
# Zeichenkette      | 14 Byte | EIS 15 | DPT 16       | DONE

def __eis1( data):
    if int(data[0].encode("hex"),16) == 0:
        return False
    else:
        return True

def __eis2( data):
    return __unknown( data)

def __eis3( data):
    return __unknown( data)

def __eis4( data):
    return __unknown( data)

# MEEE EMMM MMMM MMMM
# E = 0..15
# M = [-2048..2047]
# Val = (0,01*M)*2**(E)
def __eis5( data):
    _data = int(data[0:2].encode("hex"),16)
    mant = _data & int('0b0000011111111111',2)
    exp  = (_data & int('0b0111100000000000',2)) >> 11
    sign = (_data & int('0b1000000000000000',2)) >> 15

    val = 0.01 * float(mant) * (2 ** exp)
    if sign == 0:
        return val
    else:
        return -1 * val

def __eis6( data):
    return __unknown( data)

def __eis7( data):
    return __unknown( data)

def __eis8( data):
    return __unknown( data)

def __eis9( data):
    return __unknown( data)

def __eis10( data):
    return __unknown( data)

def __eis11( data):
    return __unknown( data)

def __eis12( data):
    return __unknown( data)

def __eis13( data):
    return __unknown( data)

def __eis14( data):
    return __unknown( data)

def __eis15( data):
    _data = str(data[0:14])

    return _data

def __unknown( data):
    return '0x' + data.encode("hex")

eisInterpreter = {
    1 : __eis1,
    2 : __eis2,
    3 : __eis3,
    4 : __eis4,
    5 : __eis5,
    6 : __eis6,
    7 : __eis7,
    8 : __eis8,
    9 : __eis9,
    10 : __eis10,
    11 : __eis11,
    12 : __eis12,
    13 : __eis13,
    14 : __eis14,
    15 : __eis15,

    None : __unknown
}


lengthEisLookup = {
    #bitLength: eis type
    1: 1,
    4: 2,
    3*8: 3,
    2*8: 5,
    8: 14,  ## unsigend is prefered more common?
    4*8: 11, ## unsigend counter value
    14*8: 15
}

lenghtPossibleEisLookup = {
    1 : [1,7],
    4 : [2],
    1*8 : [6,13,14],
    2*8 : [4,5,8,10],
    3*8 : [3],
    4*8 : [9,11,12],
    14*8 : [15]
}

def interpret(data,eis=None, length = None):
    """
        data == str
        eis == 1 .. 15
        length == 1 ... 14*8  [bit]
    """

    if eis == None and length == None:
        _eis = None
    elif eis == None:
        if length in lengthEisLookup:
            _eis = lengthEisLookup[length]
        else:
            _eis = None
    else:
        _eis = eis

    return eisInterpreter[_eis](data)





def _test():

    tests = [
            # [eis, length, hexdata, sould value]
           [1, 1 , __HexToByte( '01000000000000' ) , True],      #EIS1
           [None, 1,  __HexToByte( '00000000000000' ) , False],  #EIS1
           [5,None, __HexToByte( '350f0000000000' ) , 828.8],         #EIS5
           [None, 16, __HexToByte( '350f0000000000' ) , 828.8],         #EIS5
           [15,None, __HexToByte( '68616c6c6f2077656c7400000000' ) , 'hallo welt    '],          #EIS15
           [None,None, __HexToByte( '350f0000000000' ) , '-']          #unknown
            ]


    for test in tests:
        print  'EIS {0:5} length {1:5} Test: {2:14} == {3:14} (is == should)'.format(str(test[0]), str(test[1]), interpret(test[2], eis = test[0],length = test[1]) , test[3])


def __HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )

    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )


if __name__ == '__main__':
    _test()
