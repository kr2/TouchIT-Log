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

from output_stram import OutputStream


from pyface.image_resource import ImageResource


class FileItem(HasTraits):
  date = Property()
  fileName = Unicode()

  def _get_date ( self ):
    if self.fileName.isdigit():
      return unicode(datetime.datetime.fromtimestamp(int(self.fileName) * 24*60*60))
    else:
      return u'No defined'


class HandlerFTPimport(Handler):

  def closed(self, info, is_ok):
    if info.object._ftp:
      info.object._ftp.close()


class FTPimport(HasTraits):
  LOG_FILE_DIR  = u'logger'


  ftpHost       = Unicode('touchit')
  ftpUser       = Unicode('')
  ftpPw         = Unicode('')

  retry         = Button('Retry')

  logFiles        = List(FileItem)
  selectedIndices = Instance(FileItem)
  selected        = Instance(FileItem)

  destDir       = Unicode()
  changeDestDir = Button('Change Directory')
  download      = Button('Download')

  comTestOutput = Instance(OutputStream)

  downloadedFiles = List(Unicode)

  _ftp = Any()

  #todo FTP to another thread
  def __connect(self):
    self._ftp =  ftplib.FTP(host=self.ftpHost, user=self.ftpUser, passwd=self.ftpPw)

  def _download_fired(self):
    print self.selectedIndices
    print self.selected

    # self.__connect()
    # for i, logFile in enumerate(self.selectedIndices):
    #   _targetPath = os.path.join(self.destDir, logFile)
    #   self.OutputStream.write('Downloading file (' + str(i) + '/' + len(self.selectedIndices) + '): ' + logFile + '\n')
    #   f = open(_targetPath,'wb')
    #   self._ftp.retrbinary('RETR '+logFile, f.write)
    #   f.close()
    #   self.downloadedFiles.append(_targetPath)


  def __readFileNames(self):
    self.__connect() # because of timeout
    if not self.LOG_FILE_DIR in self._ftp.nlst():
      self.OutputStream.write('No ' + self.LOG_FILE_DIR + ' directory found. Check if correct host and if data available.\n')
      return

    self._ftp.cwd(self.LOG_FILE_DIR)

    if self._ftp.nlst() == []:
      self.OutputStream.write('No logg files available.\n')
      return

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
          Item('logFiles',
            style = 'readonly',
            show_label=False,
            editor = TableEditor(
              editable  = False,
              sortable  = False,
              auto_size = False,
              configurable = False,
              show_column_labels = False,
              # columns   = [ ObjectColumn( name = 'date', editable = False ),
              #               ObjectColumn( name = 'fileName',  editable = False)],

              # selection_mode = 'rows',
              selected_indices = 'selectedIndices',
              # selected = 'selected'
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
    handler=HandlerFTPimport(),
    resizable = True,
    width = .5,
    height = .7,
    close_result = 0,
    icon = ImageResource('mainIcon', search_path=[r'images'])
  )



if __name__ == '__main__':
  ftpImport = FTPimport()
  print ftpImport.configure_traits()