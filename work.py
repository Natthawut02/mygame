from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import random


# สร้างหน้าจอเริ่มเกม
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # ข้อความต้อนรับ
        welcome_label = Label(text="Welcome to the Game!", font_size=30)
        layout.add_widget(welcome_label)

        # ปุ่มเริ่มเกม
        start_button = Button(
            text="Start Game",
            font_size=20,
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
        )
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        # เพิ่ม Layout ลงในหน้า
        self.add_widget(layout)

    def start_game(self, instance):
        # เปลี่ยนไปยังหน้าหลักของเกม
        self.manager.current = "game"


# สร้างแอปพลิเคชัน
class GameApp(App):
    def build(self):
        sm = ScreenManager()


if __name__ == "__main__":
    GameApp().run()
