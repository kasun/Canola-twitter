#!/usr/bin/env python
import twitter
import utils
from urllib2 import URLError
from urllib2 import HTTPError

from terra.core.plugin_prefs import PluginPrefs

class AuthError(Exception):
    pass
class TwitterError(Exception):
    pass
    

class Client(object):
    def __init__(self,uname=None,pword=None):
        self.api = twitter.Api()
        self.setSourceAsCanola()
        self.auth = False
        self.userName = None
        self.password = None
        self.prefs = PluginPrefs("twitter")
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
            
    def getReplies(self):
        try:
            statuses = self.api.GetReplies()
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
            self.api.ClearCredentials()
            self.auth = False
            self.userName = None
            self.password = None
            
            try:
                self.api.GetPublicTimeline()
            except URLError:
                raise TwitterError("No Network")
        else:
            self.api.SetCredentials(username=uname,password=pword)
            
            try:
                self.api.GetFriendsTimeline()
            except HTTPError:
                raise AuthError("Authentication failed")
            except URLError:
                raise TwitterError("No Network")
            
            self.auth = True    
            self.userName = uname
            self.password = pword
            
            
        self.saveSettings(uname,pword)
    
    def logout(self):    
        self.api.ClearCredentials()
        self.auth = False
        self.userName = None
        self.password = None
        self.saveSettings(None,None)
        
    def saveSettings(self,uname,pword):
        self.prefs["twitter_username"] = uname
        self.prefs["twitter_password"] = pword
        self.prefs.save()
        
    def loadSettings(self):
        try:
            uname = self.prefs["twitter_username"]
            pword = self.prefs["twitter_password"]
            self.login(uname,pword)
        except KeyError:
            return
        
    def getUserName(self):
        return self.userName
    
    def getPassWord(self):
        return self.password
        
    def isLogged(self):
        return self.auth
    
    def setSourceAsCanola(self):
        self.api.SetSource("canola")