#License: BSD 2-clause license

""" gui
"""
__version__ = '1.0'
_debug = 0

from traits.api import HasTraits, Str, Button, Enum, Any, Int, Property, List, Instance, cached_property, Bool
from traitsui.api import TreeEditor, TreeNode, View, Item, Group, ButtonEditor
from pyface.file_dialog import FileDialog
from pyface.constant import OK

import data.dptInterpreter as dptInterpreter

class TreeRepresentation(HasTraits):
  _treeLabel = Property( depends_on = ['name','nr'])
  name = Any('Unknown')
  nr = Int(0)

  @cached_property
  def _get__treeLabel(self):
    return str(self.nr) + ' ' + self.name


class GroupAddress(TreeRepresentation):
  groupAddress = Str('x/x/x')
  Length = Any(0)#Int(0)
  dataPoints = Int(0)
  _gaBin = Int(0)

  possbileDataTypes = List(Str)
  dataType = Enum(values = 'possbileDataTypes')
  def getDataType(self):
    return self.dataType.split(' | ')[0]

  _addRemoveButtonLabel = Str('Add to Plot')
  addRemove = Button("")
  _isPloted = Bool(False)
  _isPlotable = Bool(True)

  exportCSV = Button("Export to CSV")

  # event hoocks
  _addToPlot_hock = Any(None)
  _removeFromPlot_hock = Any(None)
  _updateData_hock = Any(None)

  _exportCSV_hock = Any(None)

  def _addRemove_changed(self):
    if self._isPloted:
      self._isPloted = False
      self._addRemoveButtonLabel= 'Add to Plot'

      if self._removeFromPlot_hock != None:
        self._removeFromPlot_hock(self)
    else:
      self._isPloted = True
      self._addRemoveButtonLabel = 'Remove from Plot'

      if self._addToPlot_hock != None:
        self._addToPlot_hock(self)

  def __isPloted_changed(self):
    if not self._isPloted:
      self._addRemoveButtonLabel= 'Add to Plot'
    else:
      self._addRemoveButtonLabel = 'Remove from Plot'


  def _dataType_changed(self):
    dpt = self.getDataType()

    self._isPlotable = dptInterpreter.dptTypes[dpt].isPlotable
    if _debug: print dpt + ': ' + str(self._isPlotable)
    self.plotUpdateRequierd();

  def plotUpdateRequierd (self):
    if self._updateData_hock != None:
      self._updateData_hock(self)

  def getDefaultLegendLabel(self):
    return self.name + ' (' + self.groupAddress + ')'

  def _exportCSV_changed(self):
    dlg = FileDialog()
    dlg.action = 'save as'
    dlg.default_filename = self.groupAddress.replace("/", "-") + '_' + self.name + '.csv'
    if dlg.open() != OK:
      return

    if self._exportCSV_hock != None:
      self._exportCSV_hock(self, dlg.path)


  _plotLegendLabel = Property(Str, depends_on = ['name','groupAddress'])
  @cached_property
  def _get__plotLegendLabel(self):
    return self.name + ' (' + self.groupAddress + ')'

  view1 = View(
            Group(
              Item(name = 'groupAddress', style = 'readonly'),
              Item(name = 'name', style = 'readonly'),
              Item(name = 'Length', style='readonly'),
              Item(name = 'dataPoints', style='readonly'),
              Item(name = 'dataType'),
              Item(name = 'addRemove', enabled_when='_isPlotable', editor = ButtonEditor(label_value = '_addRemoveButtonLabel')),
              Item(name = 'exportCSV', ),
              #label = 'Group Address'
             )
          )


class AddrGroup( TreeRepresentation):
  children = List(Any)

  view1 = View(
            Item(name='nr', style='readonly'),
            Item(name='name')
           )


class GroupAdresses (HasTraits):
    name = Str('Root', style='readonly')
    children = List(TreeRepresentation)



class Project (HasTraits):
    name           = Str('Unknown')
    groupAddresses = Instance( GroupAdresses )

    def __str__(self):
      retStr = 'Project: \n'
      retStr += self.name + '\n'
      if self.groupAddresses:
        for lay1 in self.groupAddresses.children:
          retStr += '\t' + lay1.name  + '\n'
          for lay2 in lay1.children:
            retStr += '\t\t' + lay2.name  + '\n'
            for lay3 in lay2.children:
              retStr += '\t\t\t' + lay3.name  + '\n'
      else:
        retStr += str(type(self.groupAddresses)) + '\n'

      return retStr

## Example Data
if __name__ == '__main__':
  ga1 = GroupAddress(name='ga1', groupAddress='1/1/1', possbileDataTypes=['EIS 1','EIS 2'], Length = 10, _gaBin = 10, _isPlotable=False)
  ga2 = GroupAddress(name='ga2', groupAddress='1/1/2', possbileDataTypes=['EIS 3'], Length = 10, _gaBin = 10, _isPlotable=True)
  ga3 = GroupAddress(name='ga3', groupAddress='1/1/3', possbileDataTypes=['EIS 5','EIS 2'], Length = 10, _gaBin = 10, _isPlotable=True)
  ga4 = GroupAddress(name='ga4', groupAddress='2/3/4', possbileDataTypes=['EIS 1','EIS 2'], Length = 10, _gaBin = 10, _isPlotable=False)
  ga5 = GroupAddress(name='ga5', groupAddress='2/3'  , possbileDataTypes=['EIS 1','EIS 2'], Length = 10, _gaBin = 10, _isPlotable=False)

  project = Project(
      name = 'test Project',
      groupAddresses = GroupAdresses(
        name = 'Group Adresses',
        children = [
          AddrGroup(
              name = 'main 1',
              nr = 1,
              children = [
                  AddrGroup(
                      name = 'mid 1',
                      nr = 1,
                      children = [ga1, ga2, ga3]
                      )
                  ]
              ),
          AddrGroup(
              name = 'main 2',
              nr = 2,
              children = [
                  AddrGroup(
                      name = 'mid 3',
                      nr = 3,
                      children = [ga4]
                      ),
                  ga5]
              )
        ]
      )
    )

#print project
no_view = View()

def test1(obj):
  print obj
  print obj.name


def getTreeEditor(onSelectFoo = None, onDoubelClickFoo = None):
  return TreeEditor(
      nodes = [
          TreeNode( node_for  = [ GroupAdresses ],
                    auto_open = True,
                    children  = 'children',
                    label     = 'name',
                    view      = View( Group('name',
                                     orientation='vertical',
                                     show_left=True )),
                    copy = False,
                    delete = False,
                    delete_me = False,
                    rename = False,
                    rename_me = False,
                    icon_path = r'images',
                    icon_group = r'treeRoot',
                    icon_open = r'treeRoot',
                    icon_item = r'treeFolder',
                    ),

          TreeNode( node_for  = [ AddrGroup ],
                    auto_open = False,
                    children  = 'children',
                    label     = '_treeLabel',
                    copy = False,
                    delete = False,
                    delete_me = False,
                    rename = False,
                    rename_me = False,
                    icon_path = r'images',
                    icon_group = r'treeFolder',
                    icon_open = r'treeFolder',
                    icon_item = r'treeFolder',
                    ),

          TreeNode( node_for  = [ GroupAddress ],
                    auto_open = False,
                    children  = '',
                    label     = '_treeLabel',
                    copy = False,
                    delete = False,
                    delete_me = False,
                    rename = False,
                    rename_me = False,
                    icon_path = r'images',
                    icon_group = r'groupAdress',
                    icon_open = r'groupAdress',
                    icon_item = r'groupAdress',
                    ),
      ],
      orientation = 'vertical',
      on_select = onSelectFoo,
      on_dclick = onDoubelClickFoo
  )

view = View(
           Group(
               Item(
                    name = 'groupAddresses',
                    editor = getTreeEditor(onSelectFoo=test1),
                    resizable = True),
                orientation = 'vertical',
                show_labels = False,
                show_left = True ),
            title = 'LogPlot',
            dock = 'horizontal',
            resizable = True,
            width = .3,
            height = .3
            )

if __name__ == '__main__':
  project.configure_traits( view = view )