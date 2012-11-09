#License: BSD 2-clause license

""" gui
"""
__version__ = '1.0'
_debug = 0

from traits.api import *
from traitsui.api import View, Item, VGroup,HGroup, ListStrEditor

from pyface.file_dialog import FileDialog
from pyface.constant import OK

from pyface.image_resource import ImageResource

from FTPimport import FTPimport

import os

class FileOpener(HasTraits):
  esf_files = List()
  open_esffiles = Button("Add esf Files")

  log_files = List()
  open_logfiles = Button("Add log Files")
  load_ftp_logfiles = Button("Load Files from FTP")


  def __checkPaths(self, pathList):
    delIndex = []
    for i, path in enumerate(pathList):
      path = str(path)
      if not os.path.exists(path):
        pathList[i] = path.rsplit(')',1)[0].split('(',1)[1]
      if not os.path.exists(pathList[i]):
        delIndex.append(i)

    delIndex.sort(reverse =True)

    for i in delIndex:
      del(pathList[i])


  def _esf_files_items_changed(self):
    self.__checkPaths(self.esf_files)

  def _log_files_items_changed(self):
    self.__checkPaths(self.log_files)





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

  # listEditor = ListStrEditor(
  #   multi_select = True,
  #   #horizontal_lines = True,
  #   auto_add = True,
  #   operations = ['delete', 'edit',]
  #   )

  traits_view = View(
    VGroup(
      VGroup(
        Item('esf_files', editor = ListStrEditor()
        ),
        Item('open_esffiles'),
        show_labels = False,
        label = 'ESF Files:',
        show_border = True
      ),
      VGroup(
        Item('log_files', editor = ListStrEditor()),
        HGroup(
          Item('open_logfiles',width = .5),
          Item('load_ftp_logfiles',width = .5),
          show_labels = False,
          # springy = True,
          # label = 'Log Files:',
          # show_border = True
        ),
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




  def _open_logfiles_fired(self):
    dlg = FileDialog()
    dlg.action = 'open files'
    if dlg.open() == OK:
        paths = dlg.paths
        for filePath in paths:
          self.log_files.append(filePath)

  def _open_esffiles_fired(self):
    dlg = FileDialog()
    dlg.wildcard = "*.esf"
    dlg.action = 'open files'
    if dlg.open() == OK:
        paths = dlg.paths
        for filePath in paths:
          self.esf_files.append(filePath)

  def _load_ftp_logfiles_fired(self):
    ftpImport = FTPimport()
    if ftpImport.configure_traits(kind = 'modal'):
      for filePath in ftpImport.downloadedFiles:
        self.log_files.append(filePath)

if __name__ == '__main__':
  fileOpener = FileOpener()
  fileOpener.configure_traits()
  # print fileOpener.configure_traits()

