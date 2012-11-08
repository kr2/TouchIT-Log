#License: BSD 2-clause license

""" gui
"""
__version__ = '1.0'
_debug = 0

from traits.api import HasTraits, List, Button, Date, Any, Unicode, Instance
from traitsui.api import View, Item,Group, VGroup,HGroup, ListStrEditor, DateEditor,  InstanceEditor

import tempfile


from output_stram import OutputStream


from pyface.image_resource import ImageResource

class FTPimport(HasTraits):
  LOG_FILE_DIR  = 'logger'


  ftpHost       = Unicode('touchit')
  ftpUser       = Unicode('')
  ftpPw         = Unicode('')

  retry         = Button('Retry')

  logFiles      = List()
  destDir       = Unicode()
  changeDestDir = Button('Change Directory')
  download      = Button('Download')


  comTestOutput = Instance(OutputStream)


  def _comTestOutput_default(self):
    return OutputStream()

  def _destDir_default(self):
    return unicode(tempfile.gettempdir())


  traits_view = View(
    Group(
      HGroup(
        VGroup(
          Item('ftpHost', label = 'Host'),
          Item('ftpUser', label = 'User'),
          Item('ftpPw', label = 'Password')
        ),
        VGroup(
          Item('retry', show_label = False, springy = True, full_size = True),
        ),
        label = 'FTP:',
        show_border = True
      ),
      VGroup(
        Item('logFiles',show_label = False, editor = ListStrEditor(), height = 0.5),
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
      VGroup(
        Item('comTestOutput', style='custom', editor = InstanceEditor(), show_label = False),
        label = 'Status Output:',
        show_border = True
      ),
      show_border = True
    ),
    title = 'FTP import',
    buttons = [ 'OK', 'Cancel' ],
    resizable = True,
    width = .5,
    height = .7,
    close_result = 0,
    icon = ImageResource('mainIcon', search_path=[r'images'])
  )



if __name__ == '__main__':
  ftpImport = FTPimport()
  print ftpImport.configure_traits()