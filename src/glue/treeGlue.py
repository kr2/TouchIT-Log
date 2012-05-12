#License: BSD 2-clause license

_debug = 0

from gui.Tree import Project, GroupAdresses, AddrGroup, GroupAddress

import data.KNXAddressInterpreter as KNXAddressInterpreter

import data.dptInterpreter as dptInterpreter

def createProject(dataManager, plotGlue, exportGlue):
  dm = dataManager

  gaList = _createGroupAddressList(dataManager,plotGlue, exportGlue)

  groupAdresses = GroupAdresses(name = dm.projectName)
  for ga in gaList:
    if _debug: print ga.name + ':'
    _addGroupAdress(groupAdresses,dm.gaRepDictonary[ga._gaBin], ga)

  #if _debug: print groupAdresses.children[0].name

  return Project(name = dm.projectName, groupAddresses = groupAdresses)


def _addGroupAdress(groupAddresses, gaData, gaTreeObj):
  gaList = KNXAddressInterpreter.split(gaData.gaStr)

  lastAddrGroup = groupAddresses
  for layer in xrange(0,len(gaList) - 1):
    nr = gaList[layer]

    actChild = None
    for child in lastAddrGroup.children:
      if child.nr == nr and not isinstance(child, GroupAddress):
        actChild = child
        break

    if actChild == None:
      newGroup = AddrGroup(nr = nr, name =  gaData.gaNameList[layer])
      lastAddrGroup.children.append( newGroup )
      lastAddrGroup = newGroup
      if _debug: print 'new AddrGroup'
    else:
      lastAddrGroup = actChild
      if _debug: print 'existing AddrGroup'

    if _debug: print str(layer) + '  ' + str(type(lastAddrGroup))
  if _debug: print gaTreeObj.name
  lastAddrGroup.children.append(gaTreeObj)


def _createGroupAddressList(dataManager,plotGlue, exportGlue):
  dm = dataManager

  _groupAddresses = []

  for key in dm.getSortedKeys():
    ga = dm.gaRepDictonary[key]

    # make the default selectet dpt of the enume
    possibleDpt = ga.possibleDpt
    if possibleDpt != []:
      possibleDpt.remove(ga.dpt)
      possibleDpt.insert(0,ga.dpt)

    enumList = []

    for dpt in possibleDpt:
      enumList.append(dpt + ' | ' + dptInterpreter.dptTypes[dpt].discription )

    _groupAddresses.append(
        GroupAddress(
            name = ga.gaName,
            nr = KNXAddressInterpreter.split(ga.gaStr)[-1],
            groupAddress = ga.gaStr,
            possbileDataTypes = enumList,
            Length =  ga.length,
            dataPoints = len(ga.interpretedData),
            _gaBin = ga.gaBin,
            _isPlotable = dptInterpreter.dptTypes[ga.dpt].isPlotable,
            _addToPlot_hock = plotGlue.addToPlot,
            _removeFromPlot_hock = plotGlue.removeFromPlot,
            _updateData_hock = plotGlue.updateData,
            _exportCSV_hock = exportGlue.exportGroupAdress,
        )
    )

    if _debug: print dpt
    if _debug: print dptInterpreter.dptTypes[dpt].isPlotable

  return _groupAddresses