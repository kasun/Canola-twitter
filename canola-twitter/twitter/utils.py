#!/usr/bin/env python

import os

from terra.core.plugin_prefs import PluginPrefs

def getDummyModel():
    return

def getMessageList_from_statuses(statuses):
    messageList = []
    for s in statuses:
        status = {};
        status["uname"] = getUTF8String(s.user.screen_name)
        status["update"] = getUTF8String(s.GetText())
        status["info"] =  getUTF8String(s.GetRelativeCreatedAt())
        status["thumb_url"] = getUTF8String(s.user.profile_image_url)
        messageList.append(status)
    return messageList

def getUTF8String(str):
    #unicodeString = unicode(str,"ascii")
    return str.encode("utf8")
    
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
