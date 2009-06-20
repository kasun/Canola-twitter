#!/usr/bin/env python
import twitter
import utils
from urllib2 import URLError
from urllib2 import HTTPError

class AuthError(Exception):
    pass
class TwitterError(Exception):
    pass
    

class Client(object):
    def __init__(self,uname=None,pword=None):
        self.api = twitter.Api()
        self.auth = False
        self.userName = None
        #self.login(uname,pword)
        
    def getPublicTimeline(self):
        try:
            statuses = self.api.GetPublicTimeline()
            lst = utils.getMessageList_from_statuses(statuses)
            return lst
        except URLError:
            raise TwitterError("No network")
    
    def getFriendTimeline(self):
        try:
            statuses = self.api.GetFriendsTimeline()
            lst = utils.getMessageList_from_statuses(statuses)
            return lst
        except URLError:
            raise TwitterError("No Network")
        except HTTPError:
            raise AuthError("Authentication failed")
        
    def sendTweet(self,msg):
        try:
            statuses = self.api.PostUpdate(msg)
        except URLError:
            raise TwitterError("No Network")
        except HTTPError:
            raise AuthError("Authentication failed")
            
    def login(self,uname=None,pword=None):
        if not uname and not pword:
            self.api = twitter.Api()
            self.userName = None
            self.auth = False
            
            try:
                self.api.GetPublicTimeline()
            except URLError:
                raise TwitterError("No Network")
        else:
            self.api = twitter.Api(username=uname,password=pword)
            
            try:
                self.api.GetFriendsTimeline()
            except HTTPError:
                raise AuthError("Authentication failed")
            except URLError:
                raise TwitterError("No Network")
                
            self.userName = uname
            self.auth = True
    
    def logout(self):    
        self.api = twitter.Api()
        self.userName = None
        self.auth = False
        
    def getUserName(self):
        return self.userName    
        
    def isLogged(self):
        return self.auth