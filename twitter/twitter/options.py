#!/usr/bin/env python

import logging

from terra.core.manager import Manager

manager = Manager()

MixedListController = manager.get_class("Controller/Settings/Folder/MixedList")

log = logging.getLogger("plugins.twitter.options")

class OptionsController(MixedListController):
    terra_type = "Controller/Settings/Folder/InternetMedia/Twitter"