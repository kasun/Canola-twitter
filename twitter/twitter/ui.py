#!/usr/bin/env python

import evas
import ecore
import locale
import logging

from terra.core.manager import Manager
from terra.ui.base import PluginThemeMixin

from model import SendModelFolder,ViewFriendsModelFolder,ViewPublicModelFolder

manager = Manager()

BaseListController = manager.get_class("Controller/Folder")
EntryDialogModel = manager.get_class("Model/EntryDialog")
BaseRowRenderer =  manager.get_class("Widget/RowRenderer")
OptionsControllerMixin = manager.get_class("OptionsControllerMixin")

log = logging.getLogger("plugins.twitter.ui")

class ListController(BaseListController):
    """This is used to initialize the twitter navigation list.
    Namely send tweets and recieve tweets"""
    
    terra_type = "Controller/Folder/Task/Apps/Twitter"

    def cb_on_clicked(self, view, index):
        model = self.model.children[index]
        
        if type(model) is ViewFriendsModelFolder or type(model) is ViewPublicModelFolder:
            BaseListController.cb_on_clicked(self, view, index)
            return
        
        def do_search(ignored, text):
            if text is not None:
                model.query = text

        dialog = EntryDialogModel("Send Tweets", "Enter text to tweet:",
                                  answer_callback=do_search)
        self.parent.show_notify(dialog)
        
class ServiceController(BaseListController, OptionsControllerMixin):
    terra_type = "Controller/Folder/Task/Apps/Twitter/Service"
    #row_renderer = RowRendererWidget
    #list_group = "list_video"

    def __init__(self, model, canvas, parent):
        self.empty_msg = model.empty_msg
        BaseListController.__init__(self, model, canvas, parent)
        OptionsControllerMixin.__init__(self)
        self.model.callback_notify = self._show_notify

    def _show_notify(self, err):
        """Popup a modal with a notify message."""
        self.parent.show_notify(err)

class GeneralRowRenderer(PluginThemeMixin, BaseRowRenderer):
    plugin = "twitter"

    def __init__(self, parent, theme=None):
        BaseRowRenderer.__init__(self, parent, theme)

class RowRendererWidget(GeneralRowRenderer):
    row_group="list_item_twitter"
        
        