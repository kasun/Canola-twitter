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
        return statuses
    
    def getFriendTimeline(self):
        if not self.auth:
            return
        else:
            statuses = self.api.GetFriendsTimeline()
            return statuses
        
    def sendTweet(self,msg):
        if not self.auth:
            return
        else:
            statuses = self.api.PostUpdate(msg)
            
if __name__ == "__main__":
    client = Client()
    #client = Client("kasunh01","clearme")
    #statuses = client.getPublicTimeline()
    statuses = client.getFriendTimeline()
    
    if statuses is not None:
        lst = utils.getMessageList_from_statuses(statuses)
        print "size: ",len(lst)
        for msg in lst:
            print msg["uname"],msg["update"]
            
    client.sendTweet("Testing twitter library")