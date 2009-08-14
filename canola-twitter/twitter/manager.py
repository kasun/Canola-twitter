#!/usr/bin/env python

from terra.core.manager import Manager
from terra.core.singleton import Singleton
from client import Client
from twitpic import TwitPicClient
import utils

from terra.core.terra_object import TerraObject

mger = Manager()
network = mger.get_status_notifier("Network")

class TwitterManager(Singleton, Client, TerraObject):
    terra_type = "Manager/Twitter"
    
    def __init__(self):
        Singleton.__init__(self)
        Client.__init__(self)
        self.twitpic_client = TwitPicClient()
        
    def uploadToTwitpicAndPostToTwitter(self, filename, imagedata, message):
        
        username = self.getUserName()
        password = self.getPassWord()
        
        selector = '/api/uploadAndPost'
        
        fields = [('username', username),('password', password),('message',message)]
        files = [('media',filename,imagedata)]
        
        response = self.twitpic_client.post_multipart(fields,files, selector)
        
        status = utils.getStatusFromTwitpicResponse(response)
        
        return status
        
    def uploadToTwitpic(self, filename, imagedata, message):
        
        username = self.getUserName()
        password = self.getPassWord()
        
        selector = '/api/upload'
        
        fields = [('username', username),('password', password),('message',message)]
        files = [('media',filename,imagedata)]
        
        response = self.twitpic_client.post_multipart(fields,files, selector)
    
        status = utils.getStatusFromTwitpicResponse(response)
        
        return status

