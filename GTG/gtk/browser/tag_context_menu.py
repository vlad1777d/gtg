"""
tag_context_menu:
Implements a context (pop-up) menu for the tag item in the sidebar.
Right now it is just a void shell It is supposed to become a more generic
sidebar context for all kind of item displayed there.
Also, it is supposed to handle more complex menus (with non-std widgets,
like a color picker)
"""

from gi.repository import Gtk

from GTG.core.translations import translate
from GTG.gtk.colors import generate_tag_color, color_add, color_remove


class TagContextMenu(Gtk.Menu):
    """Context menu fo the tag i the sidebar"""

    def __init__(self, datastore, vmanager, tag=None):
        super().__init__()
        self.datastore = datastore
        self.vmanager  = vmanager
        self.tag       = tag
        # Build up the menu
        self.set_tag(tag)
        self.__build_menu()

    def __build_menu(self):
        """Build up the widget"""
        # Reset the widget
        for i in self:
            self.remove(i)
            i   .destroy()
        if self.tag is not None:
            # Color chooser FIXME: SHOULD BECOME A COLOR PICKER
            self.mi_cc   = Gtk.MenuItem()
            self.mi_ctag = Gtk.MenuItem()
            self.mi_cc  .set_label(translate("Edit Tag..."))
            self.mi_ctag.set_label(translate("Generate Color"))
            self.append(self.mi_cc)
            self.append(self.mi_ctag)
            self.mi_cc  .connect('activate', self.on_mi_cc_activate)
            self.mi_ctag.connect('activate', self.on_mi_ctag_activate)
            if self.tag.is_search_tag():
                self.mi_del = Gtk.MenuItem()
                self.mi_del.set_label(translate("Delete"))
                self.append(self.mi_del)
                self.mi_del.connect('activate', self.on_mi_del_activate)
        # Make it visible
        self.show_all()

    # PUBLIC API ##############################################################
    def set_tag(self, tag):
        """Update the context menu items using the tag attributes."""
        self.tag = tag
        self.__build_menu()

    # CALLBACKS ###############################################################
    def on_mi_cc_activate(self, widget):
        """Callback: show the tag editor upon request"""
        self.vmanager.open_tag_editor(self.tag)

    def on_mi_ctag_activate(self, widget):
        random_color = generate_tag_color()
        present_color = self.tag.get_attribute('color')
        if(present_color is not None):
                color_remove(present_color)
        self.tag.set_attribute('color', random_color)
        color_add(random_color)

    def on_mi_del_activate(self, widget):
        """ delete a selected search """
        self.datastore.remove_tag(self.tag.get_name())
