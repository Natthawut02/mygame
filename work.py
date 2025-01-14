from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        welcome_label = Label(text="Welcome to the Game!", font_size=30)
        layout.add_widget(welcome_label)

        start_button = Button(
            text="Start Game",
            font_size=20,
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
        )
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, instance):

        self.manager.current = "game"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        game_label = Label(text="This is the Game Screen!", font_size=30)
        layout.add_widget(game_label)


class GameApp(App):
    def build(self):

        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))

        return sm


if __name__ == "__main__":
    GameApp().run()
