import string
import random
import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from words import Words

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
    WORD_DISPLAY = StringProperty()

    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(**kwargs)
                
        self.RANDOM_WORD = ""

        self.GUESSES = []

        self.buttons_layout = ButtonsLayout.instance[0]

        self.configure_buttons()

        self.start_game()

    @property
    def won(self):
        return all(alphabet in self.GUESSES for alphabet in self.RANDOM_WORD)
    
    def update_word_display(self):

        WORD_DISPLAY = []
        for alphabet in self.RANDOM_WORD:
            if alphabet in self.GUESSES:
                WORD_DISPLAY.append(alphabet)
            else:
                WORD_DISPLAY.append("_")

        self.WORD_DISPLAY = " ".join(WORD_DISPLAY)

    def btn_press(self, widget):

        self.GUESSES.append(widget.text)

        if widget.text in self.RANDOM_WORD:

            self.update_word_display()

    def configure_buttons(self):

        for button in self.buttons_layout.buttons.values():
            button.on_press = lambda btn=button: self.btn_press(btn)

    def start_game(self):

        self.RANDOM_WORD = random.choice(Words)

        self.WORD_DISPLAY = " ".join(["_" for _ in self.RANDOM_WORD])
class Hangman(App):
    def build(self):
        return MyRoot()

if __name__ == "__main__":
    Hangman().run()
