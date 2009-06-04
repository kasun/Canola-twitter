#!/usr/bin/env python

import evas
import ecore
import locale
import logging

from terra.core.manager import Manager

manager = Manager()

BaseListController = manager.get_class("Controller/Folder")
EntryDialogModel = manager.get_class("Model/EntryDialog")
OptionsControllerMixin = manager.get_class("OptionsControllerMixin")

log = logging.getLogger("plugins.twitter.ui")

class ListController(BaseListController):
    """This is used to initialize the twitter navigation list.
    Namely send twits and recieve twits"""
    
    terra_type = "Controller/Folder/Task/Apps/Twitter"

    def cb_on_clicked(self, view, index):

        if True:
            BaseListController.cb_on_clicked(self, view, index)
            return