#License: BSD 2-clause license
""" main
"""
__version__ = '1.0'
_debug = 0

import sys

from gui.FileSelect import FileOpener
from data.dataManager import DataManager
from gui.mainWindow import MainWindow

import glue.treeGlue as treeGlue
import glue.plotGlue as plotGlue
import glue.exportGlue as exportGlue


# File dialog
fileOpener = FileOpener()

if not fileOpener.configure_traits():
    sys.exit()


# data preperation
dm = DataManager(fileOpener.log_files, fileOpener.esf_files)


## Create project
mainWindow = MainWindow()

plotGlue = plotGlue.PlotGlue(mainWindow,dm)
exportGlue = exportGlue.ExportGlue(dm)


project = treeGlue.createProject(dm,plotGlue,exportGlue)

if _debug: print str(project)


## run main


# def onSelect(obj):
#     pass
    # if type(obj) == GroupAddress:
    #     _time = []
    #     _data = []
    #     for data in dm.gaRepDictonary[obj._gaBin]:
    #         _time.append(data[0])
    #         _data.append(data[1])

    #     ga = dm.gaRepDictonary[obj._gaBin]


    #     lastPlotName = ga.gaName + '(' + ga.gaStr + ')'
    #     mainWindow.plotPart.addData(_time,_data, ga.gaBin)
    #     mainWindow.plotPart.showData(lastPlotName,ga.gaBin)


    #     print obj.name
#mainWindow.onSelectHock = onSelect

mainWindow.treePart = project

mainWindow.configure_traits(context={'mainW':mainWindow})

