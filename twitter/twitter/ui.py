#!/usr/bin/env python

import evas
import ecore
import locale
import logging

from terra.core.manager import Manager

from model import SendModelFolder,ViewModelFolder

manager = Manager()

BaseListController = manager.get_class("Controller/Folder")
EntryDialogModel = manager.get_class("Model/EntryDialog")
OptionsControllerMixin = manager.get_class("OptionsControllerMixin")

log = logging.getLogger("plugins.twitter.ui")

class ListController(BaseListController):
    """This is used to initialize the twitter navigation list.
    Namely send tweets and recieve tweets"""
    
    terra_type = "Controller/Folder/Task/Apps/Twitter"

    def cb_on_clicked(self, view, index):
        model = self.model.children[index]
        
        if type(model) is ViewModelFolder:
            BaseListController.cb_on_clicked(self, view, index)
            return
        
        def do_search(ignored, text):
            if text is not None:
                model.query = text

        dialog = EntryDialogModel("Send Tweets", "Enter text to tweet:",
                                  answer_callback=do_search)
        self.parent.show_notify(dialog)