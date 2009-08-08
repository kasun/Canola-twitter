#!/usr/bin/env python

import etk

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