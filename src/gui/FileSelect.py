#License: BSD 2-clause license

""" gui
"""
__version__ = '1.0'
_debug = 0

from traits.api import HasTraits, List, Button
from traitsui.api import View, Item, VGroup, ListStrEditor

from pyface.file_dialog import FileDialog
from pyface.constant import OK

from pyface.image_resource import ImageResource

class FileOpener(HasTraits):
  esf_files = List
  open_esffiles = Button("Add esf Files")

  log_files = List
  open_logfiles = Button("Add log Files")

  def __init__(self):
    if _debug == 1:
      self.esf_files = ["C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//TestData//CO2_und_TEMPERATUR.esf"]
      self.log_files = ["C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//TestData//15446",
                        "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//TestData//15447",
                        "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//TestData//15448",
                        "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//TestData//15449",
                        "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//TestData//15450",
                        "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//TestData//15451",
                        "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//TestData//15452",
                        "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//TestData//15453"
                        ]
      # self.esf_files = ["C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//ExampleData//MesseTafeln.esf"]
      # self.log_files = ["C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//ExampleData//15313",
      #                   "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//ExampleData//15311",
      #                   "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//ExampleData//15310",
      #                   "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//ExampleData//14583",
      #                   "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//ExampleData//14582",
      #                   "C://Users//KR2//Documents//workspace_eclipse_Phyton//ArcLog//src//data//ExampleData//15309",
      #                   ]

  listEditor = ListStrEditor(
    multi_select = True,
    #horizontal_lines = True,
    auto_add = True,
    operations = ['delete', 'edit',]
    )

  traits_view = View(
    VGroup(
      VGroup(
        Item('esf_files', editor = ListStrEditor()),
        Item('open_esffiles'),
        show_labels = False,
        label = 'ESF Files:',
        show_border = True
      ),
      VGroup(
        Item('log_files', editor = ListStrEditor()),
        Item('open_logfiles'),
        show_labels = False,
        label = 'Log Files:',
        show_border = True
      ),
    ),
    title = 'File Select',
    buttons = [ 'OK', 'Cancel' ],
    resizable = True,
    width = .5,
    height = .7,
    close_result = 0,
    icon = ImageResource('mainIcon', search_path=[r'images'])
  )

  def _open_logfiles_changed(self):
      dlg = FileDialog()
      dlg.action = 'open files'
      if dlg.open() == OK:
          paths = dlg.paths
          for filePath in paths:
            self.log_files.append(filePath)

  def _open_esffiles_changed(self):
      dlg = FileDialog()
      dlg.wildcard = "*.esf"
      dlg.action = 'open files'
      if dlg.open() == OK:
          paths = dlg.paths
          for filePath in paths:
            self.esf_files.append(filePath)

if __name__ == '__main__':
  fileOpener = FileOpener()
  print fileOpener.configure_traits()