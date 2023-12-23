import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class ButtonsLayout(GridLayout):
    pass

class MyRoot(BoxLayout):
    pass

class Hangman(App):
    pass

if __name__ == "__main__":
    Hangman().run()