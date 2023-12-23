import string

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

        # Creating the buttons.
        self.create_buttons()

    def create_buttons(self):
        # Creating buttons for all the alphabets.
        for alphabet in string.ascii_uppercase:
            # Creating button.
            button = Button(text=alphabet)

            self.add_widget(button)

            self.buttons[alphabet] = button

class MyRoot(BoxLayout):
    pass

class Hangman(App):
    def build(self):
        return ButtonsLayout()

if __name__ == "__main__":
    Hangman().run()