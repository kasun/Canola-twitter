#!/usr/bin/env python

import etk
import ecore
import evas.decorators

from terra.ui.modal import Modal
from terra.ui.panel import PanelContentFrame

from terra.core.terra_object import TerraObject
from terra.core.manager import Manager

class TextBoxItemRenderer(etk.KineticRenderer, TerraObject):
    terra_type = "Renderer/EtkList/LabeledEntryItem"

    def __init__(self, label="", *a, **ka):
        etk.KineticRenderer.__init__(self, *a, **ka)
        self.label = label
        self.args = a
        self.kargs = ka

    def create_cell(self, canvas):
        #self.entry = etk.Entry(text=self.label)
        #self.entry = etk.Textblock(text="")
        self.entry = etk.TextView()
        self.entry.size_request_set(150,300)
        self.entry.textblock_get().text_set(self.label,10)
        self.entry.show()
        
        label = etk.Label(self.label)
        label.alignment_set(0.0, 0.0)

        vbox = etk.VBox()
        vbox.border_width_set(0)
        vbox.size_request_set(150,300)
        #vbox.append(label, etk.VBox.START, etk.VBox.FILL, 0)
        vbox.append(self.entry, etk.VBox.START, etk.VBox.FILL, 0)

        embed = etk.Embed(canvas)
        embed.add(vbox)
        embed.show_all()

        return embed.object

    def press(self, cell, row):
        pass

    def release(self, cell, row):
        pass

    def update_cell(self, cell, row):
        pass

    def show_cell(self, cell, x, y, w, h):
        cell.resize(w - 40, h - 10)
        cell.move(int(x + 5), int(y + 5))
        cell.show()
        
    def getText(self):
        return self.entry.textblock_get().text_get(0)
        
class MessageItemRenderer(etk.KineticRenderer, TerraObject):
    terra_type = "Renderer/EtkList/LabeledEntryItem"

    def __init__(self, label="", *a, **ka):
        etk.KineticRenderer.__init__(self, *a, **ka)
        self.label = label
        self.args = a
        self.kargs = ka

    def create_cell(self, canvas):
        label = etk.Label(self.label)
        label.alignment_set(0.0, 0.0)

        vbox = etk.VBox()
        vbox.border_width_set(0)
        vbox.append(label, etk.VBox.START, etk.VBox.FILL, 0)

        embed = etk.Embed(canvas)
        embed.add(vbox)
        embed.show_all()

        return embed.object

    def press(self, cell, row):
        pass

    def release(self, cell, row):
        pass

    def update_cell(self, cell, row):
        pass

    def show_cell(self, cell, x, y, w, h):
        cell.resize(w - 40, h - 10)
        cell.move(int(x + 5), int(y + 5))
        cell.show()
        
class SetReplyView(Modal):
    def __init__(self, user_id, parent, title, old_value, theme=None):
        Modal.__init__(self, parent.view, title, theme,
                       hborder=16, vborder=50)
        self.callback_ok_clicked = None
        self.callback_cancel_clicked = None
        self.callback_escape = None

        label = etk.Label("Reply")
        label.alignment_set(0.0, 1.0)
        label.show()

        self.entry = etk.TextView()
        self.entry.textblock_get().text_set('@' + user_id,10)
        self.entry.size_request_set(150,150)
        self.entry.show()


        vbox = etk.VBox()
        vbox.border_width_set(25)
        vbox.append(label, etk.VBox.START, etk.VBox.FILL, 0)
        vbox.append(self.entry, etk.VBox.START, etk.VBox.EXPAND, 0)
        vbox.show()

        self.modal_contents = PanelContentFrame(self.evas)
        self.modal_contents.frame.add(vbox)
        self.ok_button = self.modal_contents.button_add("OK")
        self.ok_button.on_clicked(self._on_button_clicked)
        self.cancel_button = self.modal_contents.button_add("  Cancel  ")
        self.cancel_button.on_clicked(self._on_button_clicked)
        self.contents_set(self.modal_contents.object)

    def _on_ok_clicked(self):
        text = self.entry.textblock_get().text_get(0)
        self.callback_ok_clicked(text)

    def _on_button_clicked(self, bt):
        if bt == self.ok_button:
            self._on_ok_clicked()
        elif bt == self.cancel_button:
            if self.callback_cancel_clicked:
                self.callback_cancel_clicked()

    @evas.decorators.del_callback
    def _destroy_contents(self):
        self.modal_contents.destroy()
        
class ConfirmDialogView(Modal):
    def __init__(self, label, parent, title, old_value, theme=None):
        Modal.__init__(self, parent.view, title, theme,
                       hborder=16, vborder=50)
        self.callback_yes_clicked = None
        self.callback_no_clicked = None
        self.callback_escape = None

        label = etk.Label('<center><font_size=20>' + label + '<font_size><center>')
        label.alignment_set(0.5, 0.5)
        label.show()

        vbox = etk.VBox()
        vbox.border_width_set(25)
        vbox.append(label, etk.VBox.START, etk.VBox.FILL, 0)
        vbox.show()

        self.modal_contents = PanelContentFrame(self.evas)
        self.modal_contents.frame.add(vbox)
        self.yes_button = self.modal_contents.button_add("Yes")
        self.yes_button.on_clicked(self._on_button_clicked)
        self.no_button = self.modal_contents.button_add("No")
        self.no_button.on_clicked(self._on_button_clicked)
        self.contents_set(self.modal_contents.object)

    def _on_yes_clicked(self):
        self.callback_yes_clicked()

    def _on_button_clicked(self, bt):
        if bt == self.yes_button:
            self._on_yes_clicked()
        elif bt == self.no_button:
            if self.callback_no_clicked:
                self.callback_no_clicked()

    @evas.decorators.del_callback
    def _destroy_contents(self):
        self.modal_contents.destroy()