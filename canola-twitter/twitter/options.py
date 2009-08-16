#!/usr/bin/env python

import ecore
import logging

from terra.core.manager import Manager
from terra.core.threaded_func import ThreadedFunction

from manager import TwitterManager
from client import AuthError, TwitterError

from renderers import SetReplyView, ConfirmDialogView, SetMessageView, ResultMessageView, WaitMessageView

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
        
        def do_operation():
            self.reply = reply
            self.view.hide()
            self.view = WaitMessageView(self.parent.last_panel, self.model.title, None, 'Operation in progress<br>Please Wait')
            self.view.show()
            return self.model.reply(reply)

        def operation_finished(exception, retval):
            
            msg = None
            
            if retval:
                msg = "Reply sent<br> Successfully"
                
            else:
                msg = "Unknow error.<br> Please try again"
                
            if exception is not None:
                if isinstance(exception, TwitterError):
                    msg = "Unable to connect<br> to server" + \
                        "Check your connection<br> and try again"
                elif isinstance(exception, AuthError):
                    msg = "Authentication error"
                else:
                    msg = "An unknown error<br> has occured<br>" + \
                        str(exception.message)

                log.error(exception)
            
            self.view.hide()
            self.view = ResultMessageView(self.parent.last_panel, self.model.title, None, msg)
            self.view.callback_ok_clicked = self.close
            self.view.show()
        
        ThreadedFunction(operation_finished, do_operation).start()

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
        
        def do_operation():
            self.view.hide()
            self.view = WaitMessageView(self.parent.last_panel, self.model.title, None, 'Operation in progress<br>Please Wait')
            self.view.show()
            return self.model.retweet()

        def operation_finished(exception, retval):
            
            msg = None
            
            if retval:
                msg = "Status retweeted<br> Successfully"
                
            else:
                msg = "Unknow error.<br> Please try again"
                
            if exception is not None:
                if isinstance(exception, TwitterError):
                    msg = "Unable to connect<br> to server" + \
                        "Check your connection<br> and try again."
                elif isinstance(exception, AuthError):
                    msg = "Authentication error"
                else:
                    msg = "An unknown error<br> has occured<br>" + \
                        str(exception.message)

                log.error(exception)
            
            self.view.hide()
            self.view = ResultMessageView(self.parent.last_panel, self.model.title, None, msg)
            self.view.callback_ok_clicked = self.close
            self.view.show()
        
        ThreadedFunction(operation_finished, do_operation).start()

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
        
        def do_operation():
            self.view.hide()
            self.view = WaitMessageView(self.parent.last_panel, self.model.title, None, 'Operation in progress<br>Please Wait')
            self.view.show()
            return self.model.deleteStatus()

        def operation_finished(exception, retval):
            
            msg = None
            
            if retval:
                msg = "Status Deleted<br> Successfully"
                
            else:
                msg = "Unknow error.<br> Please try again"
                
            if exception is not None:
                if isinstance(exception, TwitterError):
                    msg = "Unable to connect<br> to server" + \
                        "Check your connection<br> and try again."
                elif isinstance(exception, AuthError):
                    msg = "Authentication error"
                else:
                    msg = "An unknown error<br> has occured<br> " + \
                        str(exception.message)

                log.error(exception)
            
            self.view.hide()
            self.view = ResultMessageView(self.parent.last_panel, self.model.title, None, msg)
            self.view.callback_ok_clicked = self.close
            self.view.show()
        
        ThreadedFunction(operation_finished, do_operation).start()

    def delete(self):
        self.view.delete()
        self.view = None
        self.model = None
        
#####################################################################################
# Twitpic controllers
#####################################################################################

class UploadToTwitpicOptionsController(ModalController):
    terra_type = "Controller/Options/Folder/Image/Fullscreen/Submenu/Twitpic"

    def __init__(self, model, canvas, parent):
        ModalController.__init__(self, model, canvas, parent)
        self.model = model
        self.parent = parent
        self.view = SetMessageView(parent.last_panel, model.title, None)

        self.view.callback_ok_clicked = self._on_ok_clicked
        self.view.callback_cancel_clicked = self.close
        self.view.callback_escape = self.close
        self.view.show()

    def close(self):
        def cb(*ignored):
            self.back()
            self.parent.back()
        self.view.hide(end_callback=cb)

    def _on_ok_clicked(self, comment):
            
        self.message = comment

        self.view.hide()
        
        self.view = ConfirmDialogView('Do You want this photo <br>posted to your twitter <br>account?', self.parent.last_panel, self.model.title, None)
        self.view.callback_yes_clicked = self._UploadToTwitpicAndPostToTwitter
        self.view.callback_no_clicked = self._UploadToTwitpic
        self.view.show()
        
    def _UploadToTwitpic(self):
        
        def th_function():
            return self.model.uploadToTwitpic(self.message)

        def th_finished(exception, retval):
            self.view.hide()
            result = 'Your photo has been<br> uploaded'
            
            def view_close():
                self.close()
                
            if(retval is None):
                result = 'Error<br> Check your connection'
            elif(retval != 'ok'):
                result = 'Error<br> ' + retval
            
            self.view = ResultMessageView(self.parent.last_panel, self.model.title, None, result)
            self.view.callback_ok_clicked = self.close
            self.view.show()
            
        self.view.hide()
        
        self.view = WaitMessageView(self.parent.last_panel, self.model.title, None, 'Uploading photo<br>Please Wait')
        self.view.show()
        ThreadedFunction(th_finished, th_function).start()
    
    def _UploadToTwitpicAndPostToTwitter(self):
        
        def th_function():
            return self.model.uploadToTwitpicAndPostToTwitter(self.message)

        def th_finished(exception, retval):
            self.view.hide()
            result = 'Your photo has been<br> uploaded and posted in <br>twitter'
            
            def view_close():
                self.close()
            
            if(retval is None):
                result = 'Error<br> Check your connection'
            elif(retval != 'ok'):
                result = 'Error<br> ' + retval
            
            self.view = ResultMessageView(self.parent.last_panel, self.model.title, None, result)
            self.view.callback_ok_clicked = self.close
            self.view.show()
            
        self.view.hide()
        
        self.view = WaitMessageView(self.parent.last_panel, self.model.title, None, 'Uploading photo<br>Please Wait')
        self.view.show()
        ThreadedFunction(th_finished, th_function).start()

    def delete(self):
        self.view.delete()
        self.view = None
        self.model = None


