#!/usr/bin/env python

import logging

from terra.core.manager import Manager
from terra.core.task import Task
from terra.core.model import ModelFolder, Model
from terra.core.threaded_func import ThreadedFunction

from manager import TwitterManager
from client import AuthError, TwitterError

manager = Manager()
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

    def do_load(self):
        #if True:
        #    return
        
        ViewPublicModelFolder("View Public Timeline",self)
        if twitter_manager.isLogged():
            ViewFriendsModelFolder("View Friend's Tweets",self)
            SendModelFolder("Send Tweet",self)
        
class MessageModel(ModelFolder):
    '''Model for incoming messages'''
    
    terra_type = "Model/Task/Apps/Twitter/Message"
    
    def __init__(self, name, parent):
        ModelFolder.__init__(self,name,parent)
        self.uname = None
        self.text = None
        self.thumb = None
        
class ServiceModelFolder(ModelFolder):
    terra_type = "Model/Folder/Task/Apps/Twitter/Service"
    
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
        
        #if not self.threaded_search:
        #    for model in self.do_search():
        #        self.children.append(model)
        #return
    
        def refresh():
            return self.do_search()

        def refresh_finished(exception, retval):
            log.warning("search finished")

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

            #if end_callback:
            #    end_callback()

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
        display = data["uname"] + " : " + data["update"]
        model = MessageModel(display,self)
        model.uname = data["uname"]
        model.text = data["update"]
        model.thumb = data["thumb_url"]
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
# twitter Options Model
################################################################################

class OptionsModel(ModelFolder):
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
