#License: BSD 2-clause license

""" gui
"""
__version__ = '1.0'
_debug = 0

if __name__ == '__main__':
  import wxversion
  wxversion.select('2.8.12')

  from enthought.etsconfig.api import ETSConfig;
  ETSConfig.toolkit = "wx";

from traits.api import HasTraits, List, Button, Date, Any, Unicode, Instance, Property, Int
from traitsui.api import View, Item,Group, VGroup,HGroup, ListStrEditor, DateEditor,  InstanceEditor, TableEditor, Handler,ObjectColumn

import tempfile
import datetime
import ftplib
import os

from pyface.directory_dialog import DirectoryDialog
from pyface.constant import OK

from output_stram import OutputStream


from pyface.image_resource import ImageResource


class FileItem(HasTraits):
  date = Property()
  fileName = Unicode()

  def _get_date ( self ):
    if self.fileName.isdigit():
      return unicode(datetime.datetime.fromtimestamp(int(self.fileName) * 24*60*60).strftime("%d. %B %Y"))
    else:
      return u'No defined'

  def __str__(self):
    return unicode(self.fileName) + ' (' + unicode(self.date) + ')'


class HandlerFTPimport(Handler):

  def closed(self, info, is_ok):
    if info.object._ftp:
      info.object._ftp.close()
    return is_ok


class FTPimport(HasTraits):
  LOG_FILE_DIR  = u'logger'


  ftpHost       = Unicode('touchit')
  ftpUser       = Unicode('')
  ftpPw         = Unicode('')

  retry         = Button('Retry')

  infoStr       = Unicode('Dont use the Shift key to select.\nCtrl+Click or drawin an box works fine.')
  logFiles        = List(FileItem)
  selectedIndices = Any()

  destDir       = Unicode()
  changeDestDir = Button('Change Directory')
  download      = Button('Download')

  comTestOutput = Instance(OutputStream)

  downloadedFiles = List(Unicode)

  _ftp = Any()

  #todo FTP to another thread
  def __connect(self):
    self._ftp =  ftplib.FTP(host=self.ftpHost, user=self.ftpUser, passwd=self.ftpPw)
    self._ftp.connect()

  def _download_fired(self):
    # print self.selectedIndices

    self.__connect()
    self.__changeToLogDir()
    for i, logFile in enumerate([self.logFiles[i] for i in self.selectedIndices]):
      _targetPath = os.path.join(self.destDir, logFile.fileName)
      self.comTestOutput.write('Downloading file (' + str(i+1) + '/' + str(len(self.selectedIndices)) + '): ' + logFile.fileName + '\n')
      f = open(_targetPath,'wb')
      self._ftp.retrbinary('RETR '+logFile.fileName, f.write)
      f.close()
      if not _targetPath in self.downloadedFiles:
        self.downloadedFiles.append(_targetPath)
        # print _targetPath
        # print self.downloadedFiles



  def __changeToLogDir(self):
    if not self.LOG_FILE_DIR in self._ftp.nlst():
      self.OutputStream.write('No ' + self.LOG_FILE_DIR + ' directory found. Check if correct host and if data available.\n')
      return

    self._ftp.cwd(self.LOG_FILE_DIR)

    if self._ftp.nlst() == []:
      self.OutputStream.write('No logg files available.\n')
      return

  def __readFileNames(self):
    self.__changeToLogDir()

    self.logFiles = [FileItem(fileName=x) for x in self._ftp.nlst()]

    self.logFiles = sorted(self.logFiles, key=lambda x: x.fileName)



  def _retry_fired(self):
    if self._ftp:
      del(self._ftp)

    try:
      self.__connect()
      self.comTestOutput.write(unicode(self._ftp.getwelcome()) + '\n')
    except Exception, e:
      self.comTestOutput.write(unicode(e) + '\n')

    if self._ftp:
      self.comTestOutput.write('Connection OK\n')
      self.__readFileNames()


  def _changeDestDir_changed(self):
      dlg = DirectoryDialog()
      if dlg.open() == OK:
          self.destDir = dlg.path



  def _comTestOutput_default(self):
    return OutputStream()

  def _destDir_default(self):
    return unicode(tempfile.gettempdir())



  def __init__(self):
    self._retry_fired()


  traits_view = View(
    Group(
      HGroup(
        VGroup(
          VGroup(
            Item('ftpHost', label = 'Host'),
            Item('ftpUser', label = 'User'),
            Item('ftpPw', label = 'Password'),
            Item('retry', show_label = False),
            label = 'FTP:',
            show_border = True
          ),
          VGroup(
            Item('comTestOutput', style='custom', editor = InstanceEditor(), show_label = False),
            label = 'Status Output:',
            show_border = True
          ),
        ),
        VGroup(
          Item('infoStr', show_label=False, style = 'readonly'),
          Item('logFiles',
            style = 'readonly',
            show_label=False,
            editor = ListStrEditor(
              editable = False,
              multi_select = True,
              selected_index = 'selectedIndices',
            )
          ),
          HGroup(
            Item('download', show_label = False),
            HGroup(
              Item('destDir',show_label = False),
              Item('changeDestDir',show_label = False)
            ),
          ),
          label = 'Files:',
          show_border = True
        ),
      ),
    ),
    title = 'FTP import',
    buttons = [ 'OK', 'Cancel' ],
    # handler=HandlerFTPimport(),
    resizable = True,
    width = .5,
    height = .7,
    icon = ImageResource('mainIcon', search_path=[r'images'])
  )



if __name__ == '__main__':
  ftpImport = FTPimport()
  print ftpImport.configure_traits()