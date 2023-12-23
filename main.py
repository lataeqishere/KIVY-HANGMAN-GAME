import string
import random
import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class ButtonsLayout(GridLayout):
    instance = []

    def __init__(self, **kwargs):
        super(ButtonsLayout, self).__init__(**kwargs)

        ButtonsLayout.instance.append(self)

        self.rows = 2
        self.cols = 13

        self.buttons = {}

        self.create_buttons()

    def create_buttons(self):
        
        for alphabet in string.ascii_uppercase:

            button = Button(
                text=alphabet,
                font_name="fonts/GeistMonoNerdFontMono-Bold.otf",
                font_size=24)

            self.add_widget(button) #26widget

            self.buttons[alphabet] = button
class MyRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
        self.buttons_layout = ButtonsLayout
class Hangman(App):
    def build(self):
        return MyRoot()

if __name__ == "__main__":
    Hangman().run()
