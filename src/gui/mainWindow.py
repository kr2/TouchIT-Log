#License: BSD 2-clause license

""" gui
"""
__version__ = '1.0'
_debug = 0

import Plot
import Tree

from traits.api import HasTraits, Instance
from traitsui.api import View, Item, Group, HGroup, VGroup, HSplit
from enable.component_editor import ComponentEditor

from pyface.image_resource import ImageResource


#class MainWindow(HasTraits):
#    treePart = Instance( Tree.Project )
#    plotPart = Instance( Plot.MainPlot )

#    def __init__(self):
#        self.treePart = Tree.project # for test
#        self.plotPart = Plot.MainPlot()

# Sample class
class MainWindow(HasTraits):
    treePart = Instance( Tree.Project )
    plotPart = Instance( Plot.MainPlot )
    exportButton = Instance(Plot.ExportButtons)

    def __init__(self):
        if _debug == 1:
            self.treePart = Tree.project
        self.plotPart = Plot.MainPlot()
        self.exportButton = Plot.ExportButtons(self.plotPart.plot)

        onSelectHock = None # calld if tree element is selected def onSelect(obj):
        onDoubleClickHock = None

    view1 = View(
        HSplit(
            VGroup(
                Item('mainW.treePart.groupAddresses', editor = Tree.getTreeEditor(onSelectFoo='mainW.onSelectHock', onDoubelClickFoo ='mainW.onDoubleClickHock'), height = 0.9),

                Group(
                    VGroup(
                        Item('mainW.exportButton.height',label='height [px]', show_label=True, springy = True),
                        Item('mainW.exportButton.width',label='width [px]', show_label=True, springy = True),
                        #Item('mainW.exportButton.dpi',label='DPI', show_label=True, springy = True),
                        #show_border = True
                    ),
                    HGroup(
                        #Item('mainW.exportButton.pdf_export', show_label=False,springy = True),
                        Item('mainW.exportButton.png_export', show_label=False,springy = True),
                        #Item('mainW.exportButton.svg_export', show_label=False,springy = True),
                        #show_labels = False,
                    ),
                    label = 'Plot Picture Export',
                    show_border = True,
                    show_labels=True
                ),
                show_labels = False,
                show_left = True,
            ),
            Item('mainW.plotPart.plot', editor=ComponentEditor(), show_label=False, width = 0.65),
        ),
        title = 'TouchIT Log',
        resizable = True,
        width = 800,
        height = 600,
        icon = ImageResource('mainIcon', search_path=[r'images'])
        )

if __name__ == '__main__':
    mainWindow = MainWindow()
    #mainWindow.plotPart.addData(Plot.testTime,Plot.testData, 2)
    #mainWindow.plotPart.showData('ga1',2)
    mainWindow.configure_traits( context={'mainW':mainWindow})