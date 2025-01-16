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

        # Layout สำหรับแสดงข้อความอุณหภูมิ
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
            size_hint=(0.05, 0.05),
        )
        back_button.bind(on_press=self.go_back)
        anchor_layout.add_widget(back_button)

        # เพิ่มมอนสเตอร์
        self.monster_image = Image(
            source="diji.jpeg",  # ค่าเริ่มต้นของมอนสเตอร์
            size_hint=(0.2, 0.3),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        layout.add_widget(self.monster_image)

        # Layout สำหรับรายการไอเท็มพร้อมรูปภาพ
        self.items_layout_with_images = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(0.4, 0.12),
            pos_hint={"x": 0.02, "y": 0.02},
        )

        # เพิ่มรูปภาพและข้อความของไอเท็ม
        self.item_widgets = {}
        self.items_count = {"Food": 0, "Water": 0, "heater": 0, "Toy": 0}
        item_images = {
            "Food": "food.jpeg",
            "Water": "water.jpeg",
            "heater": "heater.jpeg",
            "Toy": "toy.jpeg",
        }

        self.item_labels = {}
        for item, image_path in item_images.items():
            item_box = BoxLayout(orientation="vertical", spacing=5)
            item_image = Image(source=image_path, size_hint=(1, 0.8))
            item_label = Label(
                text=f"{item}: 0",
                font_size=12,
                color=(1, 1, 1, 1),
                size_hint=(1, 0.2),
                halign="center",
                valign="middle",
            )
            item_box.add_widget(item_image)
            item_box.add_widget(item_label)
            self.items_layout_with_images.add_widget(item_box)
            self.item_labels[item] = item_label  # อัปเดต Label
            self.item_widgets[item] = item_box  # เก็บ Widget สำหรับการอัปเดต

        layout.add_widget(self.items_layout_with_images)

        # เพิ่ม Layout แสดงเหรียญทอง
        self.gold_layout = AnchorLayout(anchor_x="right", anchor_y="bottom", padding=10)
        self.gold_image = Image(
            source="gold.jpeg",
            size_hint=(None, None),
            size=(40, 40),
        )
        self.gold_label = Label(
            text="Gold: 0",
            font_size=12,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(100, 40),
            halign="center",
            valign="middle",
        )
        self.gold_layout.add_widget(self.gold_image)
        self.gold_layout.add_widget(self.gold_label)
        layout.add_widget(self.gold_layout)

        # เพิ่ม Layout ต่างๆ ลงในหน้า
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
        self.temp_label.text = f"{new_temp} °C"

    def update_monster(self, dt=None):
        # รายชื่อมอนสเตอร์ที่สามารถสุ่มได้
        monsters = ["diji"]  # เพิ่มมอนสเตอร์ที่นี่

        # สุ่มเลือกมอนสเตอร์
        monster = random.choice(monsters)

        # ตรวจสอบว่าไฟล์รูปภาพมอนสเตอร์มีอยู่หรือไม่
        image_path = f"{monster.lower()}.jpeg"
        try:
            # หากไม่พบไฟล์จะเกิดข้อผิดพลาด
            with open(image_path, "rb"):
                self.monster_image.source = image_path  # อัปเดตรูปภาพมอนสเตอร์
        except FileNotFoundError:
            # ถ้าไม่พบไฟล์จะแสดงข้อผิดพลาด
            print(f"Error: The image file for {monster} does not exist.")
            self.monster_image.source = "default_monster.jpeg"  # แสดงภาพดีฟอลต์แทน

        # อัปเดตภาพมอนสเตอร์
        self.monster_image.reload()  # ใช้ reload() เพื่อให้ภาพอัปเดตทันที

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
        self.items = ["Food", "Water", "heater", "Toy"]
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
        game_screen = self.manager.get_screen("game")
        if game_screen.gold_label.text.split(": ")[1].isdigit():
            current_gold = int(game_screen.gold_label.text.split(": ")[1])
            if current_gold > 0:
                game_screen.items_count[item_name] += 1
                game_screen.item_labels[item_name].text = (
                    f"{item_name}: {game_screen.items_count[item_name]}"
                )
                game_screen.gold_label.text = f"Gold: {current_gold - 1}"

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
