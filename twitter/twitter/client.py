#!/usr/bin/env python
import twitter
import utils

class Client:
    def __init__(self,uname=None,pword=None):
        self.auth = False
        if uname == None and pword == None:
            self.api = twitter.Api()
        else:
            self.api = twitter.Api(username=uname,password=pword)
            self.auth = True
        
    def getPublicTimeline(self):
        statuses = self.api.GetPublicTimeline()
        lst = utils.getMessageList_from_statuses(statuses)
        return lst
    
    def getFriendTimeline(self):
        if not self.auth:
            return
        else:
            statuses = self.api.GetFriendsTimeline()
            lst = utils.getMessageList_from_statuses(statuses)
            return lst
        
    def sendTweet(self,msg):
        if not self.auth:
            return
        else:
            statuses = self.api.PostUpdate(msg)