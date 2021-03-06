from gi.repository import Gtk


class TextUI(Gtk.Box):
    '''A widget to display a simple textbox and a label to describe its content
    '''

    def __init__(self, datastore, backend, width, description, parameter_name):
        '''
        Creates the textbox and the related label. Loads the current
        content.

        @param backend: a backend object
        @param width: the width of the Gtk.Label object
        '''
        super().__init__()
        self.backend        = backend
        self.datastore      = datastore
        self.parameter_name = parameter_name
        self.description    = description
        self._populate_gtk(width)

    def _populate_gtk(self, width):
        '''Creates the gtk widgets

        @param width: the width of the Gtk.Label object
        '''
        label = Gtk.Label(label="%s:" % self.description)
        label.set_line_wrap(True)
        label.set_alignment(xalign=0, yalign=0.5)
        label.set_size_request(width=width, height=-1)
        self.pack_start(label, False, True, 0)
        align = Gtk.Alignment.new(0, 0.5, 1, 0)
        align.set_padding(0, 0, 10, 0)
        self.pack_start(align, True, True, 0)
        self.textbox = Gtk.Entry()
        backend_parameters = self.backend.get_parameters()[self.parameter_name]
        self.textbox.set_text(backend_parameters)
        self.textbox.connect('changed', self.on_text_modified)
        align.add(self.textbox)

    def commit_changes(self):
        '''Saves the changes to the backend parameter'''
        self.backend.set_parameter(self.parameter_name,
                                   self.textbox.get_text())

    def on_text_modified(self, sender):
        ''' Signal callback, executed when the user changes the text.
        Disables the backend. The user will re-enable it to confirm the changes
        (s)he made.

        @param sender: not used, only here for signal compatibility
        '''
        if self.backend.is_enabled() and not self.backend.is_default():
            self.datastore.set_backend_enabled(self.backend.get_id(), False)
