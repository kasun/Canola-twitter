#!/usr/bin/env python

import ecore
import logging

from terra.core.manager import Manager
from terra.core.threaded_func import ThreadedFunction

from manager import TwitterManager
from client import AuthError, TwitterError

manager = Manager()
twitter_manager = TwitterManager()

OptionsController = manager.get_class("Controller/Options/Folder")
ModalController = manager.get_class("Controller/Modal")
UsernamePasswordModal = manager.get_class("Widget/Settings/UsernamePasswordModal")

MixedListController = manager.get_class("Controller/Settings/Folder/MixedList")

log = logging.getLogger("plugins.twitter.options")

class SettingsController(MixedListController):
    terra_type = "Controller/Settings/Folder/InternetMedia/Twitter"
    
class UserPassController(ModalController):
    terra_type = "Controller/Settings/Folder/InternetMedia/Twitter/UserPass"

    def __init__(self, model, canvas, parent):
        ModalController.__init__(self, model, canvas, parent)
        self.parent_controller = parent
        self.model = model
        self.view = UsernamePasswordModal(parent, self.model.get_title(),parent.view.theme,vborder=50)
        self.view.callback_ok_clicked = self._on_ok_clicked
        self.view.callback_cancel_clicked = self.close
        self.view.callback_escape = self.close
        self.view.show()
        
    def close(self):
        def cb(*ignored):
            self.parent_controller.view.list.redraw_queue()
            self.back()
        self.view.hide(end_callback=cb)
        
    def _on_ok_clicked(self):
        def cb_close(*ignored):
                self.close()
                self.parent.killall()

        if not self.view.username or not self.view.password:
            self.view.message("Username and <br>Password can't be null")
            ecore.timer_add(1.5, cb_close)
            return

        #twitter_manager.login(self.view.username,self.view.password)
        def refresh(session):
            session.login(self.view.username,self.view.password)
            
        def refresh_finished(exception, retval):
            def cb_close(*ignored):
                self.close()
                self.parent.killall()

            if exception is None:
                self.model.title = "Logged in as %s" % \
                    twitter_manager.getUserName()

                self.view.message("You are now logged in")
                ecore.timer_add(1.5, cb_close)
        
            elif isinstance(exception, AuthError):
                self.view.message("Login error.<br>%s" % exception.message)
                ecore.timer_add(1.5, cb_close)
            else:
                self.view.message("Unable to connect to server."
                                  "<br>Check your connection and <br>try again.")
            ecore.timer_add(1.5, cb_close)
        
        self.view.message_wait("  Trying to login...")
        ThreadedFunction(refresh_finished, refresh, twitter_manager).start()
        
    def delete(self):
        self.view.delete()
        self.view = None
        self.model = None
        
        
#####################################################################################
# Twitter options
#####################################################################################


