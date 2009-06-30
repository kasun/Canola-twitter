#!/usr/bin/env python

def getDummyModel():
    return

def getMessageList_from_statuses(statuses):
    messageList = []
    for s in statuses:
        status = {};
        status["uname"] = getUTF8String(s.user.screen_name)
        status["update"] = getUTF8String(s.text)
        status["thumb_url"] = getUTF8String(s.user.profile_image_url)
        messageList.append(status)
    return messageList

def getUTF8String(str):
    #unicodeString = unicode(str,"ascii")
    return str.encode("utf8")
