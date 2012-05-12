#License: BSD 2-clause license

""" gui
"""
__version__ = '1.0'
_debug = 0


# Major library imports
from numpy import random
import time
import datetime
import copy
#from os import path

from chaco.example_support import COLOR_PALETTE
#from enthought.enable.example_support import DemoFrame, demo_main

# Enthought library imports
from traits.api import HasTraits, Instance, Button, Int
from traitsui.api import Item, View
# Chaco imports
from chaco.api import  PlotAxis, add_default_grids, PlotGraphicsContext
from chaco.tools.api import PanTool, ZoomTool


from chaco.scales.api import CalendarScaleSystem
from chaco.scales_tick_generator import ScalesTickGenerator


from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor

from pyface.file_dialog import FileDialog
from pyface.constant import OK


numpoints = 10000
timeSec = [random.random()*100000000 + 1000000000 for i in xrange(numpoints)]
timeSec.sort()
testTime = [datetime.datetime.fromtimestamp(x) for x in timeSec]
testData = [random.random()*100 for i in xrange(numpoints)]
testData.sort()
testData2 = [random.random()*100 for i in xrange(numpoints)]
testData2.sort()


from scipy.special import jn


class MainPlot(HasTraits):

    plot = Instance(Plot)

    traits_view = View(
        Item('plot', editor=ComponentEditor(), show_label=False),
        width=800, height=600, resizable=True,
        title="Plot")

    def __init__(self):
        # list of allready added data
        # self.data[name] = [timeData,yData]
        self.data = {}

        # next color index from map
        self.colNr = 0

        self.plotdata = ArrayPlotData()

        self.plot = Plot(self.plotdata)
        self.plot.legend.visible = True

        self.__existingData = []  ## legenLabels

        # time axis
        time_axis = PlotAxis(self.plot, orientation="bottom", tick_generator=ScalesTickGenerator(scale=CalendarScaleSystem()))
        #self.plot.overlays.append(time_axis)
        self.plot.x_axis = time_axis

        hgrid, vgrid = add_default_grids(self.plot)
        self.plot.x_grid = None
        vgrid.tick_generator = time_axis.tick_generator

        # drag tool only time dir
        self.plot.tools.append(PanTool(self.plot, constrain=False,
                                #    constrain_direction="x"
                                      )
                                )

        # zoom tool only y dir
        self.plot.overlays.append(
        	#ZoomTool(self.plot, drag_button="right", always_on=True, tool_mode="range", axis="value" )
        	ZoomTool(self.plot, tool_mode="box", always_on=False)
        	)

        # init plot
        self.plot.plot(
            (
                self.plotdata.set_data(name = None, new_data = [time.mktime(testTime[i].timetuple()) for i in xrange(len(testTime))], generate_name=True),
                self.plotdata.set_data(name = None, new_data = testData, generate_name=True)
            ),
            name = 'temp')
        self.plot.request_redraw()
        self.plot.delplot('temp')

        #self.showData(testTime,testData,'ga1')

    def addData(self, _time, y , dataKey, overwriteData = False):
        """
        if name already exists the existing is overwritten if overwriteData
        """
        if not dataKey in self.data or overwriteData:
            x = [time.mktime(_time[i].timetuple()) for i in xrange(len(_time))]
            self.data[dataKey] = [
                self.plotdata.set_data(name = None, new_data = x, generate_name=True),
                self.plotdata.set_data(name = None, new_data = y, generate_name=True)
            ]


    def showData(self, legendLabel, dataKey):
        if not dataKey in self.data:
            raise Exception('No entry for that dataKey plz first use addData')

        #if not legendLabel in self.__existingData:
        self.plot.plot((self.data[dataKey][0], self.data[dataKey][1]), name = legendLabel, color=self._getColor())
        #else:
        #    self.plot.plot.showplot(legendLabel)

        zoomrange = self._get_zoomRange()
        self.plot.range2d.set_bounds(zoomrange[0],zoomrange[1])


        self.plot.request_redraw()

    def _get_zoomRange(self):
        values = []
        indices = []
        for renderers in self.plot.plots.values():
            for renderer in renderers:
                indices.append(renderer.index.get_data())
                values.append(renderer.value.get_data())

        indMin = None
        indMax = None

        valMin = None
        valMax = None

        for indice in indices:
            _min = min(indice)
            _max = max(indice)

            if indMin:
                indMin = min(indMin,_min)
            else:
                indMin = _min

            if indMin:
                indMax = max(indMax,_max)
            else:
                indMin = _max

        for value in values:
            _min = min(value)
            _max = max(value)

            if valMin:
                valMin = min(valMin,_min)
            else:
                valMin = _min

            if valMax:
                valMax = max(valMax,_max)
            else:
                valMax = _max

        if indMin and indMax and valMin and valMax:
            return ((indMin,valMin),(indMax,valMax))
        else:
            return None






    def hideData(self, legendLabel):
    	self.plot.delplot(legendLabel)
        #self.plot.hideplot(legendLabel)
        zoomrange = self._get_zoomRange()
        if zoomrange:
            self.plot.range2d.set_bounds(zoomrange[0],zoomrange[1])

        self.plot.request_redraw()

    def _getColor(self):
    	temp = self.colNr

    	self.colNr += 1
    	if self.colNr >= len(COLOR_PALETTE):
    		self.colNr = 0

    	return tuple(COLOR_PALETTE[temp])


class ExportButtons(HasTraits):
    pdf_export = Button("PDF")
    png_export = Button("PNG")
    svg_export = Button("SVG")
    width = Int(1600)
    height = Int(1200)
    dpi = Int(144)
    __DEF_FILE_NAME = 'Plot'

    def __init__(self, plot):
        self.plot = plot

    def _png_export_fired(self):
        outfileName = self._getFilePath(defFileName=self.__DEF_FILE_NAME + '.png')

        if outfileName != None:
            from chaco.api import PlotGraphicsContext
            container = self.plot
            tempSize = copy.deepcopy( container.outer_bounds )
            container.outer_bounds = list((self.width-1,self.height-1))
            container.do_layout(force=True)
            # gc = PlotGraphicsContext((self.width,self.height), dpi=self.dpi)
            gc = PlotGraphicsContext((self.width-1,self.height-1))
            gc.render_component(container)
            gc.save( outfileName )
            container.outer_bounds = tempSize
            self.plot.request_redraw()

    def _svg_export_fired(self):
        outfileName = self._getFilePath(defFileName=self.__DEF_FILE_NAME + '.svg')

        if outfileName != None:
            from chaco.svg_graphics_context import SVGGraphicsContext
            container = self.plot
            tempSize = copy.deepcopy( container.outer_bounds )
            container.outer_bounds = list((self.width,self.height))
            container.do_layout(force=True)
            gc = SVGGraphicsContext((self.width,self.height))
            gc.render_component(container)
            gc.save( outfileName )
            container.outer_bounds = tempSize
            self.plot.request_redraw()

    def _pdf_export_fired(self):
        outfileName = self._getFilePath(defFileName=self.__DEF_FILE_NAME + '.pdf')

        if outfileName != None:
            from chaco.pdf_graphics_context import PdfPlotGraphicsContext
            container = self.plot
            tempSize = copy.deepcopy( container.bounds )
            container.bounds = list((self.width,self.height))
            container.do_layout(force=True)

            gc = PdfPlotGraphicsContext(filename=outfileName, dest_box = (0.5, 0.5, -0.5, -0.5), pagesize = 'A4', dest_box_units = 'mm')
            gc.render_component(container)
            gc.save()
            container.bounds = tempSize
            #component.draw(self, view_bounds=(0, 0, tempSize[0], tempSize[1]))
            container.do_layout(force=True)
            #self.plot.request_redraw()
            self.invalidate_and_redraw()


        #container = self.plot
        #container.bounds = list(size)
        #container.do_layout(force=True)
        #gc = PdfPlotGraphicsContext(filename=filename, dest_box = (0.5, 0.5, 5.0, 5.0))
        #gc.render_component(container)
        #gc.save()

    def _getFilePath(self, defFileName):
        dlg = FileDialog()
        dlg.action = 'save as'
        dlg.default_filename = defFileName
        if dlg.open() == OK:
            return dlg.path
        else:
            return None


if __name__ == "__main__":
    temp = MainPlot()
    temp.addData(testTime,testData, 1)
    temp.addData(testTime,testData2, 2)
    temp.showData('ga1',1)
    temp.showData('ga2',2)
    temp.hideData('ga1')
    temp.configure_traits()
