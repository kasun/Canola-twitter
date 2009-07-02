#!/usr/bin/env python

from terra.core.singleton import Singleton
from client import Client

class TwitterManager(Singleton,Client):
    
    def __init__(self):
        Singleton.__init__(self)
        Client.__init__(self)

