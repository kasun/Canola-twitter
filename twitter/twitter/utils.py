#!/usr/bin/env python

def getDummyModel():
    return

def getMessageList_from_statuses(statuses):
    messageList = []
    for s in statuses:
        status = {};
        status["uname"] = s.user.screen_name
        status["update"] = s.text
        status["thumb_url"] = s.user.profile_image_url
        messageList.append(status)
    return messageList
