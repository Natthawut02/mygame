from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
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


# สร้างหน้าจอเล่นเกม
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # Layout สำหรับป้ายข้อความแสดงค่าอุณหภูมิ
        anchor_layout_temp = AnchorLayout(anchor_x="left", anchor_y="top", padding=10)
        self.temp_label = Label(
            text="Temperature: -- °C",
            font_size=15,
            size_hint=(None, None),
            size=(200, 50),
            halign="left",  # จัดให้อยู่ซ้าย
            valign="middle",
        )
        anchor_layout_temp.add_widget(self.temp_label)

        # Layout สำหรับปุ่ม "Back to Start"
        anchor_layout = AnchorLayout(anchor_x="right", anchor_y="top", padding=10)
        back_button = Button(
            text="Back",
            font_size=14,
            size_hint=(0.05, 0.03),
        )
        back_button.bind(on_press=self.go_back)
        anchor_layout.add_widget(back_button)

        # เพิ่ม Layout ทั้งหมดในหน้า
        self.add_widget(main_layout)
        self.add_widget(anchor_layout_temp)
        self.add_widget(anchor_layout)

        # เรียกใช้งานฟังก์ชันอัปเดตค่าอุณหภูมิ
        self.update_temperature(0)  # เรียกใช้เพื่อสุ่มอุณหภูมิเมื่อเริ่มต้น
        Clock.schedule_interval(self.update_temperature, 60)

    def update_temperature(self, dt):
        # สุ่มค่าอุณหภูมิ
        if random.random() < 0.1:  # โอกาส 10% สำหรับค่าต่ำกว่า 25 หรือมากกว่า 35
            new_temp = (
                random.choice(range(15, 25))
                if random.random() < 0.5
                else random.choice(range(36, 45))
            )
        else:
            new_temp = random.randint(25, 35)  # ค่าในช่วงปกติ

        # อัปเดตข้อความอุณหภูมิ
        self.temp_label.text = f"{new_temp} °C"

    def go_back(self, instance):
        # เปลี่ยนกลับไปยังหน้าเริ่มต้น
        self.manager.current = "start"


# สร้างแอปพลิเคชัน
class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))  # เพิ่มหน้าจอเริ่มต้น
        sm.add_widget(GameScreen(name="game"))  # เพิ่มหน้าจอเกม
        return sm


if __name__ == "__main__":
    GameApp().run()
