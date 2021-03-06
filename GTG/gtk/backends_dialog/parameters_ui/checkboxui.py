from gi.repository import Gtk


class CheckBoxUI(Gtk.Box):
    '''
    It's a widget displaying a simple checkbox, with some text to explain its
    meaning
    '''

    def __init__(self, datastore, backend, width, text, parameter):
        '''
        Creates the checkbox and the related label.

        @param backend: a backend object
        @param width: the width of the gtk.Label object
        @param parameter: the backend parameter this checkbox should display
                           and modify
        '''
        super().__init__()
        self.backend   = backend
        self.datastore = datastore
        self.text      = text
        self.parameter = parameter
        self._populate_gtk(width)

    def _populate_gtk(self, width):
        '''Creates the checkbox and the related label

        @param width: the width of the Gtk.Label object
        '''
        self.checkbutton = Gtk.CheckButton(label=self.text)
        backend_parameters = self.backend.get_parameters()[self.parameter]
        self.checkbutton.set_active(backend_parameters)
        self.checkbutton.connect("toggled", self.on_modified)
        self.pack_start(self.checkbutton, False, True, 0)

    def commit_changes(self):
        '''Saves the changes to the backend parameter'''
        self.backend.set_parameter(self.parameter,
                                   self.checkbutton.get_active())

    def on_modified(self, sender=None):
        ''' Signal callback, executed when the user clicks on the checkbox.
        Disables the backend. The user will re-enable it to confirm the changes
        (s)he made.

        @param sender: not used, only here for signal compatibility
        '''
        if self.backend.is_enabled() and not self.backend.is_default():
            self.req.set_backend_enabled(self.backend.get_id(), False)
