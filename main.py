import string
import random
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from words import Words

class ButtonsLayout(GridLayout):
    instance = []
    background_music = SoundLoader.load('sound/game_music1.mp3')
    button_sound = SoundLoader.load('sound/button_sound.mp3')

    @classmethod
    def play_background_music(cls):
        if cls.background_music:
            cls.background_music.volume = 0.125
            cls.background_music.play()

    @classmethod
    def stop_background_music(cls):
        if cls.background_music:
            cls.background_music.stop()

    @classmethod
    def set_background_music_volume(cls, volume):
        if cls.background_music:
            cls.background_music.volume = volume

    def __init__(self, **kwargs):
        super(ButtonsLayout, self).__init__(**kwargs)

        ButtonsLayout.instance.append(self)

        self.rows = 2
        self.cols = 14
        self.buttons = {}
        self.create_buttons()

    def create_buttons(self):
        for alphabet in string.ascii_uppercase:
            button = Button(
                text=alphabet,
                font_name="fonts/Productive_Day.otf",
                font_size=24,
                background_color=(0, 0, 0, 0),
                color=(0, 0, 0, 1)
            )
            button.bind(on_press=self.on_button_press)
            self.add_widget(button)
            self.buttons[alphabet] = button

        hint_button = Button(
            text='Hint',
            font_name="fonts/Productive_Day.otf",
            font_size=24,
            background_color=(0, 0, 0, 0),
            color=(0, 0, 0, 1)
        )
        hint_button.bind(on_press=self.on_hint_button_press)
        self.add_widget(hint_button)
        self.buttons['Hint'] = hint_button

    def on_setting_button_press(self, instance):
        print("Setting button pressed")

    def show_settings_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        change_song_button1 = Button(text='Change Song 1', font_size=24, on_press=self.change_song1)
        change_song_button2 = Button(text='Change Song 2', font_size=24, on_press=self.change_song2)
        change_song_button3 = Button(text='Change Song 3', font_size=24, on_press=self.change_song3)
        content.add_widget(change_song_button1)
        content.add_widget(change_song_button2)
        content.add_widget(change_song_button3)
        exit_button = Button(text='Exit', font_size=24, on_press=self.on_exit_button_press)
        content.add_widget(exit_button)
        popup = Popup(title='Settings', content=content, size_hint=(None, None), size=(400, 300))
        popup.open()

    def change_song1(self, instance=None):
        print("Changing to Song 1")
        if self.background_music:
            self.background_music.stop()
        self.background_music = SoundLoader.load('sound/game_music1.mp3')
        if self.background_music:
            self.background_music.volume = 0.125
            self.background_music.play()

    def change_song2(self, instance=None):

        print("Changing to Song 2")
        if self.background_music:
            self.background_music.stop()
        self.background_music = SoundLoader.load('sound/game_music2.mp3')
        if self.background_music:
            self.background_music.volume = 0.125
            self.background_music.play()

    def change_song3(self, instance=None):
        print("Changing to Song 3")
        if self.background_music:
            self.background_music.stop()
        self.background_music = SoundLoader.load('sound/game_music3.mp3')
        if self.background_music:
            self.background_music.volume = 0.125
            self.background_music.play()

    def on_exit_button_press(self, instance):
        print("Exit button pressed")
        App.get_running_app().stop()

    def on_button_press(self, instance):
        self.button_sound.play()

    def on_hint_button_press(self, instance):
        self.show_hint()

class MyRoot(BoxLayout):
    ERRORS = StringProperty()
    HANGMAN_IMG = StringProperty()
    WORD_DISPLAY = StringProperty()
    GAME_MSG = StringProperty()

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
        widget.disabled = True
        self.GUESSES.append(widget.text)

        if widget.text in self.RANDOM_WORD:
            self.update_word_display()
            if self.won:
                for button in self.buttons_layout.buttons.values():
                    button.disabled = True
                self.HANGMAN_IMG = "images/vic.jpg"
                self.GAME_MSG = "You Won!!!!"
        else:
            self.ERRORS = str(int(self.ERRORS) + 1)
            self.HANGMAN_IMG = "images/hangman" + self.ERRORS + ".png"
            if int(self.ERRORS) == 7:
                for button in self.buttons_layout.buttons.values():
                    button.disabled = True
                self.GAME_MSG = "GAME OVER!!!"
                self.WORD_DISPLAY = self.RANDOM_WORD
                ButtonsLayout.stop_background_music()

    def configure_buttons(self):
        for button in self.buttons_layout.buttons.values():
            button.on_press = lambda btn=button: self.btn_press(btn)
        setting_button = self.buttons_layout.buttons.get("Settings")
        if setting_button:
            setting_button.bind(on_press=lambda btn=setting_button: self.on_setting_button_press())

    def show_hint(self):
        if self.RANDOM_WORD and not self.won:
            unrevealed_letters = [letter for letter in self.RANDOM_WORD if letter not in self.GUESSES]
            if unrevealed_letters:
                hint_letter = unrevealed_letters[0]
                self.GUESSES.append(hint_letter)
                self.update_word_display()

    def start_game(self):
        self.RANDOM_WORD = random.choice(Words)
        self.GUESSES.clear()
        self.ERRORS = "0"
        self.HANGMAN_IMG = "images/hangman0.png"
        self.GAME_MSG = "Guess the word"
        self.WORD_DISPLAY = " ".join(["_" for _ in self.RANDOM_WORD])
        for button in self.buttons_layout.buttons.values():
            button.disabled = False
        ButtonsLayout.play_background_music()

    def on_setting_button_press(self):
        print("Setting button pressed")
        self.buttons_layout.show_settings_popup(None)

class Hangman(App):
    def build(self):
        return MyRoot()

if __name__ == "__main__":
    Hangman().run()
