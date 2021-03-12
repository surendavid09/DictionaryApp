from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
import json, glob
from datetime import datetime
from pathlib import Path
import random
from sqlconnector import dictionary_sql

Builder.load_file('design.kv')

#classes need to have same nane -- Same string--- as design.kv file
class LoginScreen(Screen):
    """
    Login screen for application. If new user, will redirect to signup
    screen. If current user, will check for user name and password match
    """

    def sign_up(self):
        self.manager.current="sign_up_screen"

    def forgot_password(self):
        self.manager.current="forgot_password_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password']==pword:
            self.manager.current= 'login_screen_success'
        else:
            self.ids.login_wrong.text = "Wrong username or password!"


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    """
    Renders screen for signup. Will input signup information into
    json file, which is used to verify login information. If email is in use, not valid
    or the password does not match the user name, sign up screen success
    will not load.
    """

    def add_user(self, uname,pword):
        with open("users.json") as file:
            users=json.load(file)

        users[uname] = {'username': uname, 'password': pword,
        'created': datetime.now().strftime("%Y--%m-%d  %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
        """
        Redirects user to login screen after successful signup
        """

        def back_to_login(self):
            self.manager.transition.direction ="right"
            self.manager.current="login_screen"

class LoginScreenSuccess(Screen):
        """
        Once logged in, home page will load for application. Screen will feature logout button,
        button to retrieve quote and display on application.
        """
        def log_out(self):
            self.manager.transition.direction ="right"
            self.manager.current = "login_screen"

        def get_quote(self, feel):
            #self.ids.quote.text = query_database(1, feel)
            results = dictionary_sql(feel)
            output=""
            if type(results)==str:
                output=results
            else:
                for result in results:
                    output = output+result[0]+"\n"+"\n"

            self.ids.quote.text = output

class ForgotPasswordScreen(Screen):
    """
    Screen will allow user to change password if provided the correct username
    """

    def change_password(self, uname, pword, confirm):
        if pword == confirm:
            with open("users.json") as file:
                users=json.load(file)

            if uname in users:
                users[uname]['password']=pword
                print(users[uname]['password'])
                self.ids.uname_error.text = "Password Changed"
                self.manager.current="forgot_password_success_screen"

            else:
                self.ids.uname_error.text = "Username is not in database"

            with open("users.json", 'w') as file:
                json.dump(users, file)
        else:
            self.ids.uname_error.text="Password and confirmed did not match"

class ForgotPasswordSuccessScreen(Screen):
        """
        Redirects user to login screen after successfully changing password
        """

        def back_to_login(self):
            self.manager.transition.direction ="right"
            self.manager.current="login_screen"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
