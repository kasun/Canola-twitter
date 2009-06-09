#!/usr/bin/env python

import logging

from terra.core.manager import Manager
from terra.core.task import Task
from terra.core.model import ModelFolder, Model

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
        
class ViewPublicModelFolder(ModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service/View/Public"
    
    empty_msg = "Empty"
    
    def __init__(self, name, parent):
        Task.__init__(self)
        ModelFolder.__init__(self, name, parent)

    def do_load(self):
        pass
    
class ViewFriendsModelFolder(ModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service/View/Friends"
    
    empty_msg = "Empty"
    
    def __init__(self, name, parent):
        Task.__init__(self)
        ModelFolder.__init__(self, name, parent)

    def do_load(self):
        pass
    
class SendModelFolder(ModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service/Send"
    
    empty_msg = "Empty"
    
    def __init__(self, name, parent):
        Task.__init__(self)
        ModelFolder.__init__(self, name, parent)
        self.query = None

    def do_load(self):
        text=self.do_getText()
    
    def do_getText(self):
        return self.query
    

