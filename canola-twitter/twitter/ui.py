#!/usr/bin/env python

import evas
import ecore
import locale
import logging

from terra.core.manager import Manager
from terra.core.controller import Controller
from terra.ui.base import PluginThemeMixin

from model import SendModelFolder,ViewFriendsModelFolder,ViewPublicModelFolder,ViewRepliesModelFolder

manager = Manager()

BaseListController = manager.get_class("Controller/Folder")
EntryDialogModel = manager.get_class("Model/EntryDialog")
BaseRowRenderer =  manager.get_class("Widget/RowRenderer")
OptionsControllerMixin = manager.get_class("OptionsControllerMixin")

log = logging.getLogger("plugins.twitter.ui")

class ListController(BaseListController):
    """This is used to initialize the twitter navigation list."""
    
    terra_type = "Controller/Folder/Task/Apps/Twitter"
    
    def __init__(self, model, canvas, parent):
        BaseListController.__init__(self, model, canvas, parent)
        self.model.callback_notify = self._show_notify
        
    def cb_on_clicked(self, view, index):
        model = self.model.children[index]
        
        if type(model) is not SendModelFolder:
            BaseListController.cb_on_clicked(self, view, index)
            return
        
        def do_search(ignored, text):
            if text is not None:
                model.query = text
                
                model.sendTweet(text)

        dialog = EntryDialogModel("Send Tweets", "Enter text to tweet:",
                                  answer_callback=do_search)
        self.parent.show_notify(dialog)
        
    def _show_notify(self, err):
        """Popup a modal with a notify message."""
        self.parent.show_notify(err)
        
class GeneralRowRenderer(PluginThemeMixin, BaseRowRenderer):
    '''RowRenderer to display status lists'''
    plugin = "twitter"

    def __init__(self, parent, theme=None):
        BaseRowRenderer.__init__(self, parent, theme)
        self.image = self.evas.FilledImage()
        self.part_swallow("contents", self.image)
        self.signal_emit("thumb,hide", "")
        
    def theme_changed(self, end_callback=None):
        def cb(*ignored):
            self.part_swallow("contents", self.image)
            if end_callback is not None:
                end_callback(self)

        BaseRowRenderer.theme_changed(self, cb)
        
    def cb_load_thumbnail(self):
        try:
            self.image.file_set(self._model.thumb)
            self.signal_emit("thumb,show", "")
        except Exception, e:
            log.error("could not load image %r: %s", self._model.thumb_url, e)
            self.signal_emit("thumb,hide", "")
        
    def value_set(self, model):
        """Apply the model properties to the renderer."""
        if not model or model is self._model:
            return

        self._model = model
        self.part_text_set("user_id", model.uname)
        self.part_text_set("text", model.text)
        self.part_text_set("status_info", model.info)
        
        model.request_thumbnail(self.cb_load_thumbnail)
        
    @evas.decorators.del_callback
    def __on_delete(self):
        """Free internal data on delete."""
        self.image.delete()

class RowRendererWidget(GeneralRowRenderer):
    row_group="list_item_twitter"
        
class ServiceController(BaseListController, OptionsControllerMixin):
    terra_type = "Controller/Folder/Task/Apps/Twitter/Service"
    row_renderer = RowRendererWidget

    def __init__(self, model, canvas, parent):
        self.empty_msg = model.empty_msg
        BaseListController.__init__(self, model, canvas, parent)
        OptionsControllerMixin.__init__(self)
        self.model.callback_notify = self._show_notify

    def _show_notify(self, err):
        """Popup a modal with a notify message."""
        self.parent.show_notify(err)
        
class GeneralStatusRenderer(PluginThemeMixin, BaseRowRenderer):
    '''Rowrenderer to display selected statuses'''
    plugin = "twitter"

    def __init__(self, parent, theme=None):
        BaseRowRenderer.__init__(self, parent, theme)
        self.image = self.evas.FilledImage()
        self.part_swallow("contents", self.image)
        self.signal_emit("thumb,hide", "")
        
    def theme_changed(self, end_callback=None):
        def cb(*ignored):
            self.part_swallow("contents", self.image)
            if end_callback is not None:
                end_callback(self)

        BaseRowRenderer.theme_changed(self, cb)
        
    def cb_load_thumbnail(self):
        try:
            self.image.file_set(self._model.thumb)
            self.signal_emit("thumb,show", "")
        except Exception, e:
            log.error("could not load image %r: %s", self._model.thumb_url, e)
            self.signal_emit("thumb,hide", "")
        
    def value_set(self, model):
        """Apply the model properties to the renderer."""
        if not model or model is self._model:
            return

        self._model = model
        self.part_text_set("user_id", model.uname)
        self.part_text_set("text", model.text)
        
        model.request_thumbnail(self.cb_load_thumbnail)
        
    @evas.decorators.del_callback
    def __on_delete(self):
        """Free internal data on delete."""
        self.image.delete()

class StatusRendererWidget(GeneralStatusRenderer):
    row_group="twitter_status"


class MessageController(BaseListController, OptionsControllerMixin):
    
    terra_type = "Controller/Folder/Task/Apps/Twitter/Message"
    row_renderer = StatusRendererWidget
    
    def __init__(self, model, canvas, parent):
        BaseListController.__init__(self, model, canvas, parent)
        OptionsControllerMixin.__init__(self)
        self.model.callback_notify = self._show_notify
        
    def options_model_get(self):
        try:
            return self.model.options_model_get(self)
        except:
            return None

    def _show_notify(self, err):
        """Popup a modal with a notify message."""
        self.parent.show_notify(err)
        
        