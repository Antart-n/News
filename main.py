from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import config

class NewsApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.button_layout = BoxLayout(orientation=config.ORIENTATION_BUTTONS, size_hint=(1, 1), pos_hint={"y": 0})

        self.backgroud = Image(source=config.BACKGROUD_PATH, fit_mode="cover", size_hint=(1, 1))
        self.logo = Image(source=config.LOGO_PATH, size_hint=(None, None), pos_hint=config.LOGO_POSITION)
        self.logo.size = self.logo.texture_size
        self.button_left = Button(text="", background_normal="", background_color=(1, 1, 1, 0))
        self.button_right = Button(text="", background_normal="", background_color=(1, 1, 1, 0))

        self.music = SoundLoader.load(config.BACKGROUND_MUSIC_PATH)
        self.music.volume = 0.05
        self.sound_page = SoundLoader.load(config.PAGE_SOUND_PATH)
        self.fullscreen = False

    def build(self):

        Window.bind(on_key_down=self.toggle_fullscreen)
        Window.set_icon(config.ICO_PATH)

        self.layout.add_widget(self.backgroud)
        self.set_newspaper()
        self.layout.add_widget(self.logo)

        self.button_left.bind(on_press=lambda x:self.toggle_page_left())
        self.button_right.bind(on_press=lambda x:self.toggle_page_right())

        self.button_layout.add_widget(self.button_left)
        self.button_layout.add_widget(self.button_right)

        self.music.play()

        self.layout.add_widget(self.button_layout)

        return self.layout

    def toggle_fullscreen(self, window, key, scancode, codepoint, modifiers):
        if key == 292:
            if self.fullscreen == False:
                self.fullscreen = "auto"
            elif self.fullscreen == "auto":
                self.fullscreen = False
            Window.fullscreen = self.fullscreen
            print(self.backgroud.size)
            print(Window.size)

    def atualizar_fundo(self):
        self.backgroud.texture = None
        self.backgroud.reload()
            
    def set_newspaper(self):
        self.pages_newpaper = list()
        self.show_page = 0
        for path in config.NEWSPAPER_PATHS:
            img = Image(source=path, pos_hint=config.NEWSPAPER_POSITION, size_hint=(0.75, 0.75), fit_mode="contain")
            self.pages_newpaper.append(img)
        self.layout.add_widget(self.pages_newpaper[self.show_page])

    def toggle_page_left(self):
        self.layout.remove_widget(self.pages_newpaper[self.show_page])
        if self.show_page > 0:
            self.show_page -= 1
            self.sound_page.play()
        self.layout.add_widget(self.pages_newpaper[self.show_page])

    def toggle_page_right(self):

        self.layout.remove_widget(self.pages_newpaper[self.show_page])
        if self.show_page < (len(config.NEWSPAPER_PATHS) - 1):
            self.show_page += 1
            self.sound_page.play()
        self.layout.add_widget(self.pages_newpaper[self.show_page])
    
NewsApp().run()
