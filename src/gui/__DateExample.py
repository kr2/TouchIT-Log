import wxversion
wxversion.select('2.8')

from enthought.etsconfig.api import ETSConfig;
ETSConfig.toolkit = "wx";


#  Copyright (c) 2007-2009, Enthought, Inc.
#  License: BSD Style.

"""
A Traits UI editor that wraps a WX calendar panel.
"""

from enthought.traits.api import HasTraits, Date, List, Str, on_trait_change, Color, Any
from enthought.traits.ui.api import View, Item, DateEditor, Group


class DateEditorDemo(HasTraits):
    """ Demo class to show Date editors. """
    single_date = Date
    multi_date = List(Any)
    info_string = Str('The editors for Traits Date objects.  Showing both '\
                      'the defaults, and one with alternate options.')

    multi_select_editor = DateEditor(multi_select=True,
                                     months=3,
                                     allow_future=False,
                                     padding=0,
                                     on_mixed_select='toggle',
                                     shift_to_select=False)

    view = View(Item('info_string',
                     show_label=False,
                     style='readonly'),

                Group(Item('single_date',
                           label='Simple date editor'),
                      Item('single_date',
                           style='custom',
                           label='Default custom editor'),
                      Item('single_date',
                           style='readonly',
                           editor=DateEditor(strftime='You picked %B %d %Y',
                                             message='Click a date above.'),
                           label='ReadOnly editor'),
                      label='Default settings for editors'),

                Group(Item('multi_date',
                           editor=multi_select_editor,
                           style='custom',
                           label='Multi-select custom editor'),
                      label='More customized editor: multi-select; disallow '\
                            'future; two months; padding; selection '\
                            'style; etc.'),

                resizable=True)


    def _multi_date_changed(self):
        """ Print each time the date value is changed in the editor. """
        print self.multi_date

    def _simple_date_changed(self):
        """ Print each time the date value is changed in the editor. """
        print self.simple_date, self.single_date

    def _single_date_changed(self):
        """ Print each time the date value is changed in the editor. """
        print self.single_date


#-- Set Up The Demo ------------------------------------------------------------

demo = DateEditorDemo()

if __name__ == "__main__":
    demo.configure_traits()

#-- eof -----------------------------------------------------------------------
