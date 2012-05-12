#License: BSD 2-clause license


""" dpt interpreter
"""
__version__ = '1.0'
_debug = 0

import struct

#Types:
# bit | posible
#  1  |  DPT
#  4  |  uint4 , string
#  8  |  uint8 , int8 , char
# 16  |  uint16, int16, float16, string(date)
# 24  |  string(time)
# 32  |  unit32, int32, float32
#112  |  string

class DPT(object):
  def __init__(self, name, length = 0, discription = 'None', interpret = None, isPlotable = False):
    self.name = name # e.g. DPT1.001
    self.length = length # length in bit
    self.discription = discription # e.g. values = [on,off]

    self.isPlotable = isPlotable # only true if it is posible and makes sens to plot value vs time

    self.interpreter = interpret  # foo to interpret (data)

  def __str__(self):
    ret = ''
    ret += self.name + ' ('
    if self.isPlotable:
      ret += 'is Plotable'
    else:
      ret += 'is not Plotable'
    ret += ') '
    ret += self.discription
    return ret

  def interpret(self, data):
    return self.interpreter(data)


#/******************************************************************************/
#/*                                   DPTs                                     */
#/******************************************************************************/
dptTypes = {}

#/*-----------------------------------DPT1.xxx----------------------------------*/

# DPT1.xxx
def __int1xxx(data):
  if int(data[0].encode("hex"),16) == 0:
    return 0
  else:
    return 1

dptTypes['DPT1.xxx'] = DPT(
    name = 'DPT1.xxx',
    length = 1,
    discription = '1 or 0',
    isPlotable = True,
    interpret = __int1xxx
  )

# DPT1.001
def __int1001(data):
  if int(data[0].encode("hex"),16) == 0:
    return 'Off'
  else:
    return 'On'

dptTypes['DPT1.001'] = DPT(
    name = 'DPT1.001',
    length = 1,
    discription = 'On or OFF',
    isPlotable = False,
    interpret = __int1001
  )

#/*-----------------------------------DPT2.xxx----------------------------------*/
#/*-----------------------------------DPT3.xxx----------------------------------*/
# DPT3.xxx   #TODO
def __int3xxx(data):
  _data = int(data[0].encode("hex"),16)
  direction = (_data & int('0b00001000',2)) >> 3
  stepsize  = (_data & int('0b00000111',2))

  val = 2 ** (int(stepsize)-1)

  if direction:
    return val * -1
  else:
    return val

dptTypes['DPT3.xxx'] = DPT(
    name = 'DPT3.xxx',
    length = 4,
    discription = '4 bit sigend int',
    isPlotable = True,
    interpret = __int3xxx
  )

#/*-----------------------------------DPT4.xxx----------------------------------*/
#/*-----------------------------------DPT5.xxx----------------------------------*/
# DPT5.010   #TODO
def __int5010(data):
  return int(data[0].encode("hex"),16)

dptTypes['DPT5.010'] = DPT(
    name = 'DPT5.010',
    length = 8,
    discription = '1 Byte unsigned',
    isPlotable = True,
    interpret = __int5010
  )
#/*-----------------------------------DPT6.xxx----------------------------------*/
#/*-----------------------------------DPT7.xxx----------------------------------*/
# DPT7.001   #TODO
def __int7001(data):
  return int(data[0:2].encode("hex"),16)

dptTypes['DPT7.001'] = DPT(
    name = 'DPT7.001',
    length = 16,
    discription = '2 Byte unsigend',
    isPlotable = True,
    interpret = __int7001
  )
#/*-----------------------------------DPT8.xxx----------------------------------*/
# DPT8.001   #TODO
def __int8001(data):
  s = struct.Struct('!h')
  return s.unpack(data[0:2])[0]

dptTypes['DPT8.001'] = DPT(
    name = 'DPT8.001',
    length = 16,
    discription = '2 Byte sigend',
    isPlotable = True,
    interpret = __int8001
  )


#/*-----------------------------------DPT9.xxx----------------------------------*/
# DPT9.xxx   #TODO
def __int9xxx(data):
  _data = int(data[0:2].encode("hex"),16)
  mant = _data & int('0b0000011111111111',2)
  exp  = (_data & int('0b0111100000000000',2)) >> 11
  sign = (_data & int('0b1000000000000000',2)) >> 15

  val = 0.01 * float(mant) * (2 ** exp)
  if sign == 0:
      return val
  else:
      return -1 * val

dptTypes['DPT9.xxx'] = DPT(
    name = 'DPT9.xxx',
    length = 16,
    discription = '2 Byte Float',
    isPlotable = True,
    interpret = __int9xxx
  )


#/*-----------------------------------DPT10.xxx---------------------------------*/
# DPT10.001
dayLookup = {
  0: 'no day',
  1: 'Monday',
  2: 'Tuesday',
  3: 'Wednesday',
  4: 'Thursday',
  5: 'Friday',
  6: 'Saturday',
  7: 'Friday'
}

def __int10001(data):
  _data  = int(data[0:2].encode("hex"),16)
  nrDay  = (_data & int('0b111000000000000000000000',2)) >> 21
  hour   = (_data & int('0b000111110000000000000000',2)) >> 16
  minute  = (_data & int('0b000000000011111100000000',2)) >> 8
  second = (_data & int('0b000000000000000000111111',2))

  day = dayLookup[nrDay]

  return '{0}, {1}:{2}:{3}'.format(day, hour, minute, second)

dptTypes['DPT10.001'] = DPT(
    name = 'DPT10.001',
    length = 24,
    discription = 'Time',
    isPlotable = False,
    interpret = __int10001
  )


#/*-----------------------------------DPT11.xxx---------------------------------*/
# DPT11.001
def __int11001(data):
  _data  = int(data[0:2].encode("hex"),16)
  day    = (_data & int('0b000111110000000000000000',2)) >> 16
  month  = (_data & int('0b000000000000111100000000',2)) >> 8
  nryear = (_data & int('0b000000000000000001111111',2))

  if nryear >= 90:
    year = 1900 + nryear
  else:
    year = 2000 + nryear

  return '{0}.{1}.{2}'.format(day, month, year
    )

dptTypes['DPT11.001'] = DPT(
    name = 'DPT11.001',
    length = 24,
    discription = 'Date',
    isPlotable = False,
    interpret = __int11001
  )


#/*-----------------------------------DPT12.xxx---------------------------------*/
# DPT12.xxx   #TODO
def __int12xxx(data):
  s = struct.Struct('!I')
  return s.unpack(data[0:4])[0]

dptTypes['DPT12.xxx'] = DPT(
    name = 'DPT12.xxx',
    length = 32,
    discription = '4 Byte unsigend',
    isPlotable = True,
    interpret = __int12xxx
  )

#/*-----------------------------------DPT13.xxx---------------------------------*/
# DPT13.xxx   #TODO
def __int13xxx(data):
  s = struct.Struct('!i')
  return s.unpack(data[0:4])[0]

dptTypes['DPT13.xxx'] = DPT(
    name = 'DPT13.xxx',
    length = 32,
    discription = '4 Byte sigend',
    isPlotable = True,
    interpret = __int13xxx
  )

#/*-----------------------------------DPT14.xxx---------------------------------*/
# DPT14.xxx   #TODO
def __int14xxx(data):
  s = struct.Struct('!f')
  return s.unpack(data[0:4])[0]

dptTypes['DPT14.xxx'] = DPT(
    name = 'DPT14.xxx',
    length = 32,
    discription = '4 Byte Float',
    isPlotable = True,
    interpret = __int14xxx
  )

#/*-----------------------------------DPT15.xxx---------------------------------*/
#/*-----------------------------------DPT16.xxx---------------------------------*/
# DPT16.xxx   #TODO
def __int16000(data):
  return str(data[0:14])

dptTypes['DPT16.000'] = DPT(
    name = 'DPT16.000',
    length = 14 * 8,
    discription = '14 Byte ASCII string',
    isPlotable = False,
    interpret = __int16000
  )

#/*-----------------------------------DPT17.xxx---------------------------------*/
#/*-----------------------------------DPT18.xxx---------------------------------*/
#/*-----------------------------------DPT19.xxx---------------------------------*/
#/*-----------------------------------DPT20.xxx---------------------------------*/
#/*-----------------------------------DPT21.xxx---------------------------------*/
#/*-----------------------------------DPT22.xxx---------------------------------*/
#/*-----------------------------------DPT23.xxx---------------------------------*/
#/*-----------------------------------DPT24.xxx---------------------------------*/
#/*-----------------------------------DPT25.xxx---------------------------------*/
#/*-----------------------------------DPT26.xxx---------------------------------*/
#/*-----------------------------------DPT27.xxx---------------------------------*/
#/*-----------------------------------DPT28.xxx---------------------------------*/
#/*-----------------------------------DPT29.xxx---------------------------------*/
#/*-----------------------------------DPT30.xxx---------------------------------*/
#/*-----------------------------------DPT31.xxx---------------------------------*/


# Unknown
def __unknown( data):
    return '0x' + data.encode("hex")

dptTypes[None] = DPT(
    name = 'Unknown',
    length = 0,
    discription = 'data Type kompleatly unknown',
    isPlotable = False,
    interpret = __unknown
  )



if _debug: print str(dptTypes)

#/*--------------------------------------+-------------------------------------*/



lengthDefaultDPT = {
  #bit length : string
  None : None,
  1  : 'DPT1.xxx',
  2  : None, #TODO
  4  : 'DPT3.xxx',
  8  : 'DPT5.010',
  16 : 'DPT9.xxx',
  24 : 'DPT10.001',
  32 : 'DPT14.xxx',
  14*8: 'DPT16.000'
}


lengthPosibleDPT = {None : []}
def __makeLengthPosibleDPT():
  for key in dptTypes.keys():
    if not dptTypes[key].length in lengthPosibleDPT:
      lengthPosibleDPT[dptTypes[key].length] = []

    lengthPosibleDPT[dptTypes[key].length].append(key)

__makeLengthPosibleDPT()
if _debug: print lengthPosibleDPT

def getPosibleDPT(length):
  if not length in lengthPosibleDPT:
    return []
  else:
    return lengthPosibleDPT[length]

#EIS datentypen:
# Schalter          | 1 Bit   | EIS 1  | DPT 1
# Dimmer            | 4 Bit   | EIS 2  | DPT 3
# Zeit              | 3 Byte  | EIS 3  | DPT 10
# Datum             | 2 Byte  | EIS 4  | DPT 11
# Gleitkomma        | 2 Byte  | EIS 5  | DPT 9
# Relativwert       | 1 Byte  | EIS 6  | DPT 5 & 6
# Jallousi/rollade  | 1 Bit   | EIS 7  | DPT 1
# Zwanssteuerung    | 2 Byte  | EIS 8  | DPT 2
# IEEE Gleitkomma   | 4 Byte  | EIS 9  | DPT 14
# 16 Bit Zaehlerwert | 2 Byte  | EIS 10 | DPT 7 & 8
# 32 Bit Zaehlerwert | 4 Byte  | EIS 11 | DPT 12 & 13
# Zugangskontrolle  | 4 Byte  | EIS 12 | DPT 15
# ASCII Zeichen     | 1 Byte  | EIS 13 | DPT 4
# 8 Bit Zaehlerwert  | 1 Byte  | EIS 14 | DPT 5 & 6
# Zeichenkette      | 14 Byte | EIS 15 | DPT 16
eis2DPT = {
  1: 'DPT1.xxx',
  2: 'DPT3.xxx',
  3: 'DPT10.001',
  4: 'DPT11.001',
  5: 'DPT9.xxx',
  6: None, #TODO
  7: 'DPT1.xxx',
  8: None, #TODO
  9: 'DPT14.xxx',
  10: 'DPT7.001',
  11: 'DPT12.xxx',
  12: None, #TODO
  13: None, #TODO
  14: 'DPT5.010',
  15: 'DPT16.000'
}


def getDPT(dpt=None, eis=None, length = None):
  """
  retunr None if unknown
  """

  retDpt = ''
  if _debug: print 'retDpt is: ' + str(retDpt)

  if dpt != None:
    if not dpt in dptTypes:
      retDpt = None
    else:
      retDpt = dpt

  elif eis == None and length == None:
    retDpt = None

  elif eis == None:
    if length in lengthDefaultDPT:
      retDpt = lengthDefaultDPT[length]
    else:
      retDpt = None

  elif eis in eis2DPT:
    retDpt = eis2DPT[eis]

  else:
    retDpt = None

  if _debug: print 'retDpt is: ' + str(retDpt)
  return retDpt


def interpret(data, dpt=None, eis = None, length = None):
  """
      data == str
      1 dpt == e.g.: 'DPT1.001'
      2 eis == 1 .. 15
      3 length == 1 ... 14*8  [bit]
  """
  if _debug: print str(data) + ' - ' + str(dpt) + ' - ' + str(eis) + ' - ' + str(length)

  _dpt = getDPT(dpt=dpt,eis=eis,length=length)

  if _debug: print 'dpt is: ' + str(_dpt)
  return dptTypes[_dpt].interpret(data)


def _test():

    tests = [
          # [dpt,        eis,    length, hexdata,                                       sould value]
           [None,        1,      1,      __HexToByte( '01000000000000' ),               1],  #EIS1
           [None,        None,   1,      __HexToByte( '00000000000000' ),               0],  #EIS1
           ['DPT1.xxx',  None,   1,      __HexToByte( '01000000000000' ),               1],  #DPT1.xxx
           [None,        5,      None,   __HexToByte( '350f0000000000' ),               828.8],         #EIS5
           [None,        None,   16,     __HexToByte( '350f0000000000' ),               828.8],         #EIS5
           ['DPT9.xxx',  None,   16,     __HexToByte( '350f0000000000' ),               828.8],         #DPT9.xxx
           [None,        15,     None,   __HexToByte( '68616c6c6f2077656c7400000000' ), 'hallo welt    '],          #EIS15
           [None,        None,   None,   __HexToByte( '350f0000000000' ),               '-'],          #unknown
           ['DPT14.xxx', None,   32,     __HexToByte( '47325892000000' ),               45656.57],          #DPT14.xxx

           ['DPT5.010',  None,   8,      __HexToByte( 'fb000000000000' ),               '251'],          #DPT5.010

           ['DPT3.xxx',  None,   4,      __HexToByte( '09000000000000' ),               '-1'],          #DPT3.xxx
           ['DPT3.xxx',  None,   4,      __HexToByte( '0e000000000000' ),               '-32'],          #DPT3.xxx
           ['DPT3.xxx',  None,   4,      __HexToByte( '04000000000000' ),               '8'],          #DPT3.xxx
           ['DPT3.xxx',  None,   4,      __HexToByte( '02000000000000 ' ),               '2'],          #DPT3.xxx

           ['DPT10.001', None,   24,     __HexToByte( '6a301600000000 ' ),               '?'],          #DPT10.001
           ['DPT10.001', None,   24,     __HexToByte( '30301600000000 ' ),               '?'],          #DPT10.001

           ['DPT11.001', None,   24,     __HexToByte( '12040c00000000 ' ),               '?'],          #DPT11.001
           ['DPT11.001', None,   24,     __HexToByte( '0d040c00000000 ' ),               '?'],          #DPT11.001
            ]


    for test in tests:
        print  'DPT {0:10} EIS {1:5} length {2:5} Test: {3:14} == {4:14} (is == should)'.format(
          str(test[0]),
          str(test[1]),
          str(test[2]),
          interpret(test[3],
            dpt = test[0],
            eis = test[1],
            length = test[2]) ,
          test[4])


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
