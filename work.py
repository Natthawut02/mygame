from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
import random


# สร้างหน้าจอเริ่มเกม
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # เพิ่มรูปพื้นหลังสำหรับ StartScreen
        background = Image(source="bk1.jpeg", allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        # Layout สำหรับปุ่มและข้อความ
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # ข้อความต้อนรับ
        welcome_label = Label(
            text="Welcome to the Game!",
            font_size=60,
            color=(0, 0, 0, 1),
        )
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

        # ปุ่มร้านค้า
        shop_button = Button(
            text="Shop",
            font_size=20,
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
        )
        shop_button.bind(on_press=self.open_shop)
        layout.add_widget(shop_button)

        # เพิ่ม Layout ลงในหน้า
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = "game"

    def open_shop(self, instance):
        self.manager.current = "shop"


# สร้างหน้าจอเล่นเกม
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ใช้ RelativeLayout สำหรับการจัดการวางตำแหน่งของวิดเจ็ตต่างๆ
        layout = RelativeLayout()

        # เพิ่มรูปพื้นหลังสำหรับ GameScreen
        background = Image(source="bk2.jpeg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Layout หลัก
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # Layout สำหรับแสดงข้อความ
        anchor_layout_temp = AnchorLayout(anchor_x="left", anchor_y="top", padding=10)
        self.temp_label = Label(
            text="Temperature: -- °C",
            font_size=15,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 50),
            halign="left",
            valign="middle",
        )
        anchor_layout_temp.add_widget(self.temp_label)

        # ปุ่มย้อนกลับ
        anchor_layout = AnchorLayout(anchor_x="right", anchor_y="top", padding=10)
        back_button = Button(
            text="Back",
            font_size=14,
            size_hint=(0.1, 0.1),
        )
        back_button.bind(on_press=self.go_back)
        anchor_layout.add_widget(back_button)

        # มอนิเตอร์แสดงสถานะ
        self.monitor_label = Label(
            text="Game Status: Ready to start!",
            font_size=12,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1),
            halign="center",
            valign="middle",
        )
        main_layout.add_widget(self.monitor_label)

        # Layout สำหรับมอนสเตอร์
        self.monster_layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.monster_image = Image(
            source="diji.jpeg", size_hint=(0.3, 0.5), pos_hint={"center_x": 0.5}
        )
        self.monster_label = Label(
            text="Monster: Unknown",
            font_size=16,
            color=(1, 1, 1, 1),
            size_hint=(1, 1),
            halign="center",
            valign="middle",
        )

        self.monster_layout.add_widget(self.monster_image)
        self.monster_layout.add_widget(self.monster_label)

        main_layout.add_widget(self.monster_layout)

        # Layout สำหรับรายการสิ่งของ
        self.items_layout = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0, "y": 0},
        )
        self.items_count = {"Food": 0, "Water": 0, "Ether": 0, "Toy": 0}
        self.item_labels = {}

        for item in self.items_count:
            item_label = Label(
                text=f"{item}: 0",
                font_size=12,
                color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(80, 40),
                halign="center",
                valign="middle",
            )
            self.items_layout.add_widget(item_label)
            self.item_labels[item] = item_label

        layout.add_widget(self.items_layout)

        # เพิ่ม Layout ต่างๆ ลงในหน้า
        layout.add_widget(main_layout)
        layout.add_widget(anchor_layout_temp)
        layout.add_widget(anchor_layout)

        self.add_widget(layout)

        # อัปเดตข้อมูลเริ่มต้น
        self.update_temperature(0)
        self.update_monster()
        Clock.schedule_interval(self.update_temperature, 120)
        Clock.schedule_interval(self.update_monster, 30)

    def update_temperature(self, dt):
        # สุ่มค่าอุณหภูมิ
        new_temp = random.randint(20, 40)
        self.temp_label.text = f"Temperature: {new_temp} °C"
        self.monitor_label.text = f"Game Status: Temperature updated to {new_temp} °C"

    def update_monster(self, dt=None):
        monsters = ["diji"]
        monster = random.choice(monsters)

        # อัปเดตรูปภาพมอนสเตอร์
        self.monster_image.source = f"{monster.lower()}.jpeg"

        # อัปเดตชื่อมอนสเตอร์
        self.monster_label.text = f"Monster: {monster}"
        self.monitor_label.text = f"Game Status: Monster updated to {monster}"

    def update_items(self, item_name):
        if item_name in self.items_count:
            self.items_count[item_name] += 1
            self.item_labels[item_name].text = (
                f"{item_name}: {self.items_count[item_name]}"
            )

    def go_back(self, instance):
        self.manager.current = "start"


# สร้างหน้าจอร้านค้า
class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout หลัก
        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # ข้อความแสดงชื่อหน้าร้านค้า
        shop_label = Label(
            text="Welcome to the Shop!",
            font_size=40,
            color=(1, 1, 1, 1),
        )
        layout.add_widget(shop_label)

        # รายการสินค้า
        self.items = ["Food", "Water", "Ether", "Toy"]
        for item in self.items:
            item_button = Button(
                text=item,
                font_size=20,
                size_hint=(0.5, 0.2),
                pos_hint={"center_x": 0.5},
            )
            item_button.bind(on_press=self.buy_item)
            layout.add_widget(item_button)

        # ปุ่มย้อนกลับ
        back_button = Button(
            text="Back",
            font_size=20,
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def buy_item(self, instance):
        item_name = instance.text
        print(f"You selected {item_name}")
        game_screen = self.manager.get_screen("game")
        game_screen.update_items(item_name)

    def go_back(self, instance):
        self.manager.current = "start"


# สร้างแอปพลิเคชัน
class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(ShopScreen(name="shop"))
        return sm


if __name__ == "__main__":
    GameApp().run()
