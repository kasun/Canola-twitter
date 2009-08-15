#!/usr/bin/env python

import os
from xml.dom import minidom

from terra.core.plugin_prefs import PluginPrefs

def getDummyModel():
    return

def getMessageList_from_statuses(statuses): 
    messageList = []
    for s in statuses:
        dic = s.AsDict()
        status = {};
        status["id"] = s.id
        status["uname"] = getUTF8String(s.user.screen_name)
        status["update"] = getUTF8String(s.GetText())
        status["info"] =  getUTF8String(s.GetRelativeCreatedAt() + " from " + getSourceFromXML(dic["source"]))
        status["thumb_url"] = getUTF8String(s.user.profile_image_url)
        messageList.append(status)
    return messageList

def getUTF8String(str):
    #unicodeString = unicode(str,"ascii")
    return str.encode("utf8")
    
def getSourceFromXML(str):
    try:
        doc = minidom.parseString(str)
        element=doc.firstChild
        text=element.firstChild
        source = text.data
        return source
    except Exception:
        return str
    
def breakStringIntoLines(str):
    if len(str) > 90:
        words = str.split(' ')
        numOfSpaces = len(words)
        newText = " ".join(words[:numOfSpaces/2]) + "<br />" + " ".join(words[numOfSpaces/2 + 1:])
        return newText
    else:
        return str
    
def get_thumb_path(id=None):
    prefs = PluginPrefs("twitter")
    try:
        path = prefs["twitter_thumbs"]
    except KeyError:
        path = os.path.join(os.path.expanduser("~"),
                            ".canola", "twitter", "thumbs")
        prefs["twitter_thumbs"] = path
        prefs.save()

    if not os.path.exists(path):
        os.makedirs(path)

    if id is not None:
        path = os.path.join(path, "%s.jpg" % id)

    return path

def getStatusFromTwitpicResponse(response):
    doc = minidom.parseString(response)
    element=doc.firstChild
    
    if((element.getAttribute('stat') or element.getAttribute('status')) == 'ok'):
        return 'ok'
    else:
        error = element.childNodes[1]
        return error.getAttribute('msg')
        
def getNameFromPath(path):
    '''Method to get the filename from a filepath'''
    
    parts = path.split('/')
    return parts[-1]
    
def getImageDataFromPath(path):
    '''Method to get imagedata from file path'''
    
    image = None
    
    try:
        image = open(path)
        imagedata = image.read()
        image.close()
        return imagedata
    except:
        image.close()
        return None
    
        

if __name__ == '__main__':
    res = '<?xml version="1.0" encoding="UTF-8"?> \
    <rsp status="ok"> \
    <statusid>3283227129</statusid> \
    <userid>53358552</userid> \
    <mediaid>dpn7l</mediaid> \
    <mediaurl>http://twitpic.com/dpn7l</mediaurl> \
    </rsp>'
    
    '''res = '<?xml version="1.0" encoding="UTF-8"?> \
    <rsp stat="fail"> \
    <err code="1001" msg="Invalid twitter username or password" /> \
    </rsp>' '''

    print getStatusFromTwitpicResponse(res)

