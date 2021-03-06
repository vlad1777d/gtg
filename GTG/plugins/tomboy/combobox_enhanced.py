# TODO: put this in a class extending Gtk.Combobox and place the file in
#      GTG.tools

from gi.repository import Gtk, Gdk
from gi.repository import GObject


def ifKeyPressedCallback(widget, key, callback):

    def keyPress(combobox, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == key:
            callback()
    widget.connect("key-press-event", keyPress)


def ifClipboardTextIsInListCallback(clipboard_obj, list_obj, callback):

    def clipboardCallback(clipboard_obj, text, list_obj):
        if len([x for x in list_obj if x == text]) != 0:
            callback(text)
    clipboard_obj.request_text(clipboardCallback, list_obj)


def listStoreFromList(list_obj):
    list_store = Gtk.ListStore(GObject.TYPE_STRING)
    for elem in list_obj:
        iter = list_store.append()
        list_store.set(iter, 0, elem)
    return list_store


def completionFromListStore(list_store):
    completion = Gtk.EntryCompletion()
    completion.set_minimum_key_length(0)
    completion.set_text_column(0)
    completion.set_inline_completion(True)
    completion.set_model(list_store)
    return completion


def smartifyComboboxEntry(combobox, list_obj, callback):
    entry = Gtk.Entry()
    # check if Clipboard contains an element of the list
    clipboard = Gtk.Clipboard()
    ifClipboardTextIsInListCallback(clipboard, list_obj, entry.set_text)
    # pressing Enter will cause the callback
    ifKeyPressedCallback(entry, "Return", callback)
    # wrap the combo-box if it's too long
    if len(list_obj) > 15:
        combobox.set_wrap_width(5)
    # populate the combo-box
    if len(list_obj) > 0:
        list_store = listStoreFromList(list_obj)
        entry.set_completion(completionFromListStore(list_store))
        combobox.set_model(list_store)
        combobox.set_active(0)
        entry.set_text(list_store[0][0])
    combobox.add(entry)
    combobox.connect('changed', setText, entry)
    # render the combo-box drop down menu
    cell = Gtk.CellRendererText()
    combobox.pack_start(cell, True)
    combobox.add_attribute(cell, 'text', 0)
    return entry


def setText(combobox, entry):
    model = combobox.get_model()
    index = combobox.get_active()
    if index > -1:
        entry.set_text(model[index][0])
