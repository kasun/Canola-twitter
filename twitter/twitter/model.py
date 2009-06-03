#!/usr/bin/env python

from terra.core.manager import Manager
from terra.core.task import Task
from terra.core.model import ModelFolder, Model

manager = Manager()

PluginDefaultIcon = manager.get_class("Icon/Plugin")

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
        pass

