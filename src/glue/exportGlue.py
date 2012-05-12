#License: BSD 2-clause license

__version__ = '1.0'
_debug = 0

import data.gaCsvExport as gaCsvExport

_LOGPREFIX = 'exportGlue: '

class ExportGlue(object):

  def __init__(self,  dataManager):
    self.dataManager = dataManager

  def exportGroupAdress(self, gaObjct, filePath):
    if _debug == 1: print _LOGPREFIX+ 'exportGroupAdress\n' + str(gaObjct)

    gaRepresenation = self.dataManager.gaRepDictonary[gaObjct._gaBin]
    gaCsvExport.groupAddressExport(filePath, gaRepresenation)






