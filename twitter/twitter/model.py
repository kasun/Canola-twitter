#!/usr/bin/env python

import logging

from terra.core.manager import Manager
from terra.core.task import Task
from terra.core.model import ModelFolder, Model

from client import Client

manager = Manager()

PluginDefaultIcon = manager.get_class("Icon/Plugin")

log = logging.getLogger("plugins.canola-tube.twitter.model")

class Icon(PluginDefaultIcon):
    terra_type = "Icon/Folder/Task/Apps/Twitter"
    icon = "icon/main_item/photos_local"
    plugin = "twitter"
    
class MainModelFolder(ModelFolder, Task):
    """Main model.

    This initializes the other two models.
    """
    terra_type = "Model/Folder/Task/Apps/Twitter"
    terra_task_type = "Task/Folder/Task/Apps/Twitter"

    def __init__(self, parent):
        Task.__init__(self)
        ModelFolder.__init__(self, "Twitter", parent)

    def do_load(self):
        ViewPublicModelFolder("View Public Timeline",self)
        ViewFriendsModelFolder("View Friend's Tweets",self)
        SendModelFolder("Send Tweet",self)
        
class MessageModel(Model):
    '''Model for incoming messages'''
    
    terra_type = "Model/Task/Apps/Twitter/Message"
    
    def __init__(self, name, parent):
        Model.__init__(self,name,parent)
        self.uname = None
        self.text = None
        self.thumb = None
        
class ServiceModelFolder(ModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service"
    
    empty_msg = "Empty"
    
    def __init__(self, name, parent):
        ModelFolder.__init__(self, name, parent)
        self.client = Client()
        
    def do_load(self):
        self.search()
        
    def search(self,end_callback=None):
        del self.children[:]
        
        for model in self.do_search():
            self.children.append(model)
        
    def do_search(self):
        raise NotImplementedError("must be implemented by subclasses")
        
    def parse_entry_list(self, lst):
        return [_create_model_from_entry(item) for item in lst]
        
    def _create_model_from_entry(self, data):
        model = MessageModel("Message",self)
        model.uname = data["uname"]
        model.text = data["update"]
        model.thumb = data["thumb_url"]
        return model
        
    
        
class ViewPublicModelFolder(ServiceModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service/View/Public"
    
    def __init__(self, name, parent):
        ServiceModelFolder.__init__(self, name, parent)

    def do_search(self):
        statusList = self.client.getPublicTimeline()
        return parse_entry_list(statusList)
    
class ViewFriendsModelFolder(ServiceModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service/View/Friends"
    
    def __init__(self, name, parent):
        ServiceModelFolder.__init__(self, name, parent)

    def do_search(self):
        statusList = self.client.getFriendTimeline()
        return parse_entry_list(statusList)
    
class SendModelFolder(ModelFolder):
    def __init__(self, name, parent):
        ModelFolder.__init__(self, name, parent)
        self.query = None

    def do_load(self):
        text=self.do_getText()
    
    def do_getText(self):
        return self.query
    

