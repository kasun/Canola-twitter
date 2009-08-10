#!/usr/bin/env python

import ecore
import logging

from terra.core.manager import Manager
from terra.core.threaded_func import ThreadedFunction

from manager import TwitterManager
from client import AuthError, TwitterError

from renderers import SetReplyView, ConfirmDialogView

manager = Manager()
twitter_manager = TwitterManager()

OptionsController = manager.get_class("Controller/Options/Folder")
ModalController = manager.get_class("Controller/Modal")
UsernamePasswordModal = manager.get_class("Widget/Settings/UsernamePasswordModal")

EntryModal = manager.get_class("Widget/Settings/EntryModal")

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

'''class TwitterReplyOptionsController(MixedListController):
    terra_type = "Controller/Options/Folder/Apps/Twitter/Message/Reply"
    
    def __init__(self, model, canvas, parent):
        MixedListController.__init__(self, model, canvas, parent)
        self.view.button_add(label="Cancel", func=self.callback_cancel)
        self.view.button_add(label="OK", func=self.callback_ok)
        
        
    def callback_ok(self, button):
        if self.model.callback_ok:
            self.model.callback_ok()
        self.back()
        
    def callback_cancel(self, button):
        self.back()
        
class TwitterFavoriteOptionsController(MixedListController):
    terra_type = "Controller/Options/Folder/Apps/Twitter/Message/Favorite"
    
    def __init__(self, model, canvas, parent):
        MixedListController.__init__(self, model, canvas, parent)
        self.view.button_add(label="No", func=self.callback_no)
        self.view.button_add(label="Yes", func=self.callback_yes)
        
        
    def callback_yes(self, button):
        if self.model.callback_yes:
            self.model.callback_yes()
        self.back()
        
    def callback_no(self, button):
        self.back()
        
class TwitterRetweetOptionsController(MixedListController):
    terra_type = "Controller/Options/Folder/Apps/Twitter/Message/Retweet"
    
    def __init__(self, model, canvas, parent):
        MixedListController.__init__(self, model, canvas, parent)
        self.view.button_add(label="No", func=self.callback_no)
        self.view.button_add(label="Yes", func=self.callback_yes)
        
        
    def callback_yes(self, button):
        if self.model.callback_yes:
            self.model.callback_yes()
        self.back()
        
    def callback_no(self, button):
        self.back()'''
        
class TwitterReplyOptionsController(ModalController):
    terra_type = "Controller/Options/Folder/Apps/Twitter/Message/Reply"

    def __init__(self, model, canvas, parent):
        ModalController.__init__(self, model, canvas, parent)
        self.model = model
        self.parent = parent
        self.view = SetReplyView(model.user_id, parent.last_panel, model.title, None)

        self.view.callback_ok_clicked = self._on_ok_clicked
        self.view.callback_cancel_clicked = self.close
        self.view.callback_escape = self.close
        self.view.show()

    def close(self):
        def cb(*ignored):
            self.back()
            self.parent.back()
        self.view.hide(end_callback=cb)

    def _on_ok_clicked(self, reply):
            
        self.reply = reply
        self.view.hide()
        self.model.reply(reply)
        #self.view = MessageView(self.parent.last_panel, "please wait")
        #self.view.message()
        #ThreadedFunction(th_finished, th_function).start()

    def delete(self):
        self.view.delete()
        self.view = None
        self.model = None
        
class TwitterRetweetOptionsController(ModalController):
    terra_type = "Controller/Options/Folder/Apps/Twitter/Message/Retweet"
    
    def __init__(self, model, canvas, parent):
        ModalController.__init__(self, model, canvas, parent)
        self.model = model
        self.parent = parent
        label = 'Are you sure you <br>want to retweet this <br>status?'
        self.view = ConfirmDialogView(label, parent.last_panel, model.title, None)

        self.view.callback_yes_clicked = self._on_yes_clicked
        self.view.callback_no_clicked = self.close
        self.view.callback_escape = self.close
        self.view.show()

    def close(self):
        def cb(*ignored):
            self.back()
            self.parent.back()
        self.view.hide(end_callback=cb)

    def _on_yes_clicked(self):
        self.view.hide()
        self.model.retweet()

    def delete(self):
        self.view.delete()
        self.view = None
        self.model = None
        
class TwitterDeleteOptionsController(ModalController):
    terra_type = "Controller/Options/Folder/Apps/Twitter/Message/Delete"
    
    def __init__(self, model, canvas, parent):
        ModalController.__init__(self, model, canvas, parent)
        self.model = model
        self.parent = parent
        label = 'Are you sure you <br>want to delete this <br>status?'
        self.view = ConfirmDialogView(label, parent.last_panel, model.title, None)

        self.view.callback_yes_clicked = self._on_yes_clicked
        self.view.callback_no_clicked = self.close
        self.view.callback_escape = self.close
        self.view.show()

    def close(self):
        def cb(*ignored):
            self.back()
            self.parent.back()
        self.view.hide(end_callback=cb)

    def _on_yes_clicked(self):
        self.view.hide()
        self.model.deleteStatus()

    def delete(self):
        self.view.delete()
        self.view = None
        self.model = None

