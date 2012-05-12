#License: BSD 2-clause license

__version__ = '1.0'
_debug = 0

from gui.Tree import  GroupAddress

_LOGPREFIX = 'plotGlue: '

class PlotGlue(object):

  def __init__(self, mainWindows, dataManager):
    self.plot = mainWindows.plotPart
    self.tree = mainWindows.treePart

    self.dataManager = dataManager

    mainWindows.onSelectHock = self.treeElementSelect
    mainWindows.onDoubleClickHock = self.treeElementDoubleclick


  def treeElementSelect(self, treeElement):
    if _debug == 1: print _LOGPREFIX+ 'treeElementSelect\n' + str(treeElement)
    pass

  def treeElementDoubleclick(self, treeElement):
    if _debug == 1: print _LOGPREFIX+ 'treeElementDoubleclick\n' + str(treeElement)

    if type(treeElement) == GroupAddress and treeElement._isPlotable:
      if treeElement._isPloted:
        treeElement._isPloted = False
        self.removeFromPlot(treeElement)
      else:
        treeElement._isPloted = True
        self.addToPlot(treeElement)

  def updateData(self, gaObjct):
    if _debug == 1: print _LOGPREFIX+ 'updateData\n' + str(gaObjct)

    if gaObjct._isPloted:
      self.removeFromPlot(gaObjct)

    self.dataManager.gaRepDictonary[gaObjct._gaBin].dpt = gaObjct.getDataType()

    ga = self.dataManager.gaRepDictonary[gaObjct._gaBin]
    _time, _data = self.__splitData(ga)

    self.plot.addData(_time,_data, ga.gaBin, overwriteData = True)


    if gaObjct._isPloted:
      self.plot.showData(gaObjct._plotLegendLabel, ga.gaBin)

  def addToPlot(self, gaObjct):
    if _debug == 1: print _LOGPREFIX+ 'addToPlot\n' + str(gaObjct)

    dm = self.dataManager
    ga = dm.gaRepDictonary[gaObjct._gaBin]

    _time, _data = self.__splitData(ga)


    self.plot.addData(_time,_data, ga.gaBin)
    self.plot.showData(gaObjct._plotLegendLabel, ga.gaBin)

  def removeFromPlot(self, gaObjct):
    if _debug == 1: print _LOGPREFIX+ 'removeFromPlot\n' + str(gaObjct)

    self.plot.hideData(gaObjct._plotLegendLabel)


  def __splitData(self, data):
    _time = []
    _data = []
    for i in data:
        _time.append(i[0])
        _data.append(i[1])

    return (_time, _data)




