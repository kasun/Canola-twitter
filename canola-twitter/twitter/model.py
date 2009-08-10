#!/usr/bin/env python

import os
import urllib
import logging

from terra.core.manager import Manager
from terra.core.task import Task
from terra.core.model import ModelFolder, Model
from terra.core.threaded_func import ThreadedFunction

from manager import TwitterManager
from client import AuthError, TwitterError
from renderers import TextBoxItemRenderer, MessageItemRenderer
import utils

manager = Manager()
OptionsModelFolder = manager.get_class("Model/Options/Folder")
CanolaError = manager.get_class("Model/Notify/Error")
network = manager.get_status_notifier("Network")
twitter_manager = TwitterManager()

PluginDefaultIcon = manager.get_class("Icon/Plugin")

log = logging.getLogger("plugins.canola-tube.twitter.model")

class Icon(PluginDefaultIcon):
    terra_type = "Icon/Folder/Task/Apps/Twitter"
    icon = "icon/main_item/twitter"
    plugin = "twitter"
    
class MainModelFolder(ModelFolder, Task):
    """Main model.

    This initializes the other two models.
    """
    terra_type = "Model/Folder/Task/Apps/Twitter"
    terra_task_type = "Task/Folder/Task/Apps/Twitter"

    def __init__(self, parent):
        Task.__init__(self)
        ModelFolder.__init__(self, "Twitter", parent)
        try:
            twitter_manager.loadSettings()
        except AuthError:
            return
        except TwitterError:
            return
        
    '''def options_model_get(self, controller):
        return MainOptionsModelFolder(None, controller)'''
        
    def do_load(self):
        #if True:
        #    return
        
        ViewPublicModelFolder("View Public Timeline",self)
        if twitter_manager.isLogged():
            ViewFriendsModelFolder("Home",self)
            ViewRepliesModelFolder("@"+str(twitter_manager.getUserName()),self)
            SendModelFolder("Update my status",self)
            
class StatusModel(Model):
    '''model for statuses'''
    
    terra_type = "Model/Task/Apps/Twitter/Message/Status"
    
    def __init__(self, name, parent):
        #Model.__init__(self,name,parent)
        self.name = ''
        self.uname = None
        self.text = None
        self.thumb_url = None
        self.thumb = None
        
    def request_thumbnail(self, end_callback=None):
        def request(*ignored):
            urllib.urlretrieve(self.thumb_url, self.thumb)

        def request_finished(exception, retval):
            if end_callback:
                end_callback()

        if not self.thumb_url or os.path.exists(self.thumb):
            if end_callback:
                end_callback()
        else:
            ThreadedFunction(request_finished, request).start()
        
class MessageModel(ModelFolder):
    '''Model for incoming messages'''
    
    terra_type = "Model/Folder/Task/Apps/Twitter/Message"
    empty_msg = "Empty"
    
    def __init__(self, name, parent):
        ModelFolder.__init__(self,name,parent)
        self.id = None
        self.uname = None
        self.text = None
        self.info = None
        self.thumb_url = None
        self.thumb = None
        self.is_deletable = False
        
        
    def request_thumbnail(self, end_callback=None):
        def request(*ignored):
            urllib.urlretrieve(self.thumb_url, self.thumb)

        def request_finished(exception, retval):
            if end_callback:
                end_callback()

        if not self.thumb_url or os.path.exists(self.thumb):
            if end_callback:
                end_callback()
        else:
            ThreadedFunction(request_finished, request).start()
            
    def options_model_get(self, controller):
        return TwitterOptionsModelFolder(None,controller)
        
    def do_load(self):
        self.search()
        
    def search(self,end_callback=None):
        del self.children[:]
        
        status_model = self.create_model()
        self.children.append(status_model)
        
    def create_model(self):
        model = StatusModel('Status',self)
        model.uname = self.uname
        model.text = self.text
        model.thumb_url = self.thumb_url
        model.thumb = self.thumb
        
        return model
    
    def options_model_get(self, controller):
        return TwitterOptionsModelFolder(None, controller)
        
class ServiceModelFolder(ModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service"
    threaded_search = True
    empty_msg = "Empty"
    
    def __init__(self, name, parent):
        ModelFolder.__init__(self, name, parent)
        #self.client = Client()
        
    def do_load(self):
        #if True:
        #    self.callback_info("Network is down")
        #    return
        self.search()
        
    def search(self,end_callback=None):
        del self.children[:]
        
        if not self.threaded_search:
            for c in self.do_search():
                self.children.append(c)
            return
        
        #if not self.threaded_search:
        #    for model in self.do_search():
        #        self.children.append(model)
        #return
    
        def refresh():
            return self.do_search()

        def refresh_finished(exception, retval):
            log.warning("search finished")
            
            if retval is None:
                return

            if not self.is_loading:
                log.info("model is not loading")
                return

            if exception is not None:
                if isinstance(exception, TwitterError):
                    emsg = "Unable to connect to server.<br>" + \
                        "Check your connection and try again."
                elif isinstance(exception, AuthError):
                    emsg = "Authentication error "
                else:
                    emsg = "An unknown error has occured.<br>" + \
                        str(exception.message)

                log.error(exception)

            for item in retval:
                self.children.append(item)

            if end_callback:
                end_callback()

            #if self.callback_search_finished:
            #    self.callback_search_finished()

            self.inform_loaded()

        self.is_loading = True
        ThreadedFunction(refresh_finished, refresh).start()
        
    def do_search(self):
        raise NotImplementedError("must be implemented by subclasses")
        
    def parse_entry_list(self, lst):
        return [self._create_model_from_entry(item) for item in lst]
        
    def _create_model_from_entry(self, data):
        
        model = MessageModel("",self)
        model.id = data["id"]
        model.uname = data["uname"]
        model.text = data["update"]
        model.info = data["info"]
        model.thumb_url = data["thumb_url"]
        model.thumb = utils.get_thumb_path(data["uname"])
        return model
        
    
        
class ViewPublicModelFolder(ServiceModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service/View/Public"
    
    def __init__(self, name, parent):
        ServiceModelFolder.__init__(self, name, parent)

    def do_search(self):
        statusList = twitter_manager.getPublicTimeline()
        return self.parse_entry_list(statusList)
    
class ViewFriendsModelFolder(ServiceModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service/View/Friends"
    
    def __init__(self, name, parent):
        ServiceModelFolder.__init__(self, name, parent)

    def do_search(self):
        statusList = twitter_manager.getFriendTimeline()
        return self.parse_entry_list(statusList)
        
class ViewRepliesModelFolder(ServiceModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service/View/Replies"
    
    def __init__(self, name, parent):
        ServiceModelFolder.__init__(self, name, parent)

    def do_search(self):
        statusList = twitter_manager.getReplies()
        return self.parse_entry_list(statusList)
    
class SendModelFolder(ModelFolder):
    def __init__(self, name, parent):
        ModelFolder.__init__(self, name, parent)
        self.query = None

    def do_load(self):
        text=self.do_getText()
    
    def do_getText(self):
        return self.query
    
    def sendTweet(self,text):
        twitter_manager.sendTweet(text)
    
################################################################################
# twitter settings Models
################################################################################

class SettingsModel(ModelFolder):
    terra_type = "Model/Settings/Folder/InternetMedia/Twitter"
    title = "Twitter"

    def __init__(self, parent=None):
        ModelFolder.__init__(self, self.title, parent)
        
    def do_load(self):
        UserPassOptionsModel(self)
    
MixedListItemDual = manager.get_class("Model/Settings/Folder/MixedList/Item/Dual")
class UserPassOptionsModel(MixedListItemDual):
    terra_type = "Model/Settings/Folder/InternetMedia/Twitter/UserPass"
    title = "Login to Twitter"

    def __init__(self, parent=None):
        MixedListItemDual.__init__(self, parent)
        #self.username = lastfm_manager.get_username()
        #self.password = lastfm_manager.get_password()

    def get_title(self):
        if not self.isLogged():
            return "Login to Twitter"
        else:
            return "Logged in as %s" % twitter_manager.getUserName()
    
    def get_left_button_text(self):
        if not self.isLogged():
            return "Log on"
        else:
            return "Log off"

    def get_right_button_text(self):
        return "Change user"
    
    def on_clicked(self):
        if not self.isLogged():
            self.callback_use(self)
    
    def on_left_button_clicked(self):
        if not self.isLogged():
            self.callback_use(self)
        else:
            self.logout()
            self.callback_update(self)
            self.callback_killall()

    def on_right_button_clicked(self):
        self.callback_use(self)
        
    def isLogged(self):
        return twitter_manager.isLogged()
        
    def logout(self):
        twitter_manager.logout()
        
################################################################################
# twitter options Models
################################################################################

'''class MainOptionsModelFolder(OptionsModelFolder):
    terra_type = "Model/Options/Folder/Apps/Twitter"
    title = "options"

    def __init__(self, parent, screen_controller=None):
        OptionsModelFolder.__init__(self, parent, screen_controller)
    
    def do_load(self):
        TwitterOptionsModelFolder(self)'''
    
class TwitterOptionsModelFolder(OptionsModelFolder):
    terra_type = "Model/Options/Folder/Apps/Twitter/Message"
    title = "Options"
    
    def __init__(self, parent, screen_controller=None):
        OptionsModelFolder.__init__(self, parent, screen_controller)
        parent_model = screen_controller.model
        self.status_user_id = parent_model.uname
        self.status_text = parent_model.text
        self.status_id = parent_model.id
        
    def do_load(self):
        TwitterReplyOptionsModelFolder(self, self.status_user_id)
        #TwitterFavoriteOptionsModelFolder(self)
        TwitterRetweetOptionsModelFolder(self, self.status_user_id, self.status_text)
        
        if(self.status_user_id == twitter_manager.getUserName()):
            TwitterDeleteOptionsModelFolder(self, self.status_id)
    
class TwitterReplyOptionsModelFolder(OptionsModelFolder):
    terra_type = "Model/Options/Folder/Apps/Twitter/Message/Reply"
    title = "Reply"
    
    def __init__(self, parent, user_id):
        OptionsModelFolder.__init__(self, parent)
        self.user_id = user_id
        
    def reply(self, reply):
        twitter_manager.sendTweet(reply)
        
    def do_load(self):
        #TwitterReplyTextModelFolder('@' + self.user_id + ' ', self)
        pass
    
class TwitterFavoriteOptionsModelFolder(OptionsModelFolder):
    terra_type = "Model/Options/Folder/Apps/Twitter/Message/Favorite"
    title = "Mark Favorite"
    
    
        
    def do_load(self):
        #TwitterFavoriteMessageModelFolder(self)
        pass
    
class TwitterRetweetOptionsModelFolder(OptionsModelFolder):
    terra_type = "Model/Options/Folder/Apps/Twitter/Message/Retweet"
    title = "Retweet"
    
    def __init__(self, parent, user_id, status_text):
        OptionsModelFolder.__init__(self, parent)
        self.user_id = user_id
        self.status_text = status_text

    def retweet(self):
        retweetMessage = 'RT: @' + self.user_id + ' ' + self.status_text
        twitter_manager.sendTweet(retweetMessage)
        
    def do_load(self):
        #TwitterRetweetMessageModelFolder(self)
        pass
    
class TwitterDeleteOptionsModelFolder(OptionsModelFolder):
    terra_type = "Model/Options/Folder/Apps/Twitter/Message/Delete"
    title = "Delete Status"
    
    def __init__(self, parent, status_id):
        OptionsModelFolder.__init__(self, parent)
        self.status_id = status_id

    def deleteStatus(self):
        twitter_manager.deleteStatus(self.status_id)

class MixedListItemTextBox(ModelFolder):
    ''' Model for text box'''
    terra_type = "Model/Settings/Folder/MixedList/Item/TextBlock"

    def __init__(self, label, parent=None):
        ModelFolder.__init__(self, label, parent)
        self.renderer = TextBoxItemRenderer(label=label)

    def do_load(self):
        pass

    def getText(self):
        return self.renderer.getText()
    
class MixedListItemMessage(ModelFolder):
    ''' Model for Message'''
    terra_type = "Model/Settings/Folder/MixedList/Item/Message"
    label = ""

    def __init__(self, parent=None):
        ModelFolder.__init__(self, self.label, parent)
        self.renderer = MessageItemRenderer(label=self.label)

    def do_load(self):
        pass
    
class TwitterReplyTextModelFolder(MixedListItemTextBox):
    terra_type = "Model/Options/Folder/Apps/Twitter/Message/Reply/Text"
    
    def __init__(self, label, parent=None):
        MixedListItemTextBox.__init__(self, label, parent)
    
class TwitterFavoriteMessageModelFolder(MixedListItemMessage):
    terra_type = "Model/Options/Folder/Apps/Twitter/Message/Favorite/Message"
    label = "<font_size=20>Are you sure you want to <br>mark this status as Favorite?</font_size>"
    
class TwitterRetweetMessageModelFolder(MixedListItemMessage):
    terra_type = "Model/Options/Folder/Apps/Twitter/Message/Retweet/Message"
    label = "<font_size=20>Are you sure you want to <br>Retweet this?</font_size>"

