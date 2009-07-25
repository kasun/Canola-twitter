#!/usr/bin/env python

from terra.core.singleton import Singleton
from client import Client
from twitpic import TwitPicClient

class TwitterManager(Singleton,Client):
    
    def __init__(self):
        Singleton.__init__(self)
        Client.__init__(self)
        self.twitpic_client = TwitPicClient()
        
    def uploadAndPostToTwitpic(self, filename, imagedata, message):
        username = self.getUserName()
        password = self.getPassWord()
        
        fields = [('username', username),('password', password),('message',message)]
        files = [('media',filename,imagedata)]
        
        self.twitpic_client.post_multipart(fields,files)
        
    #def uploadToTwitpic(self, filename, imagedata):

