from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.progressbar import ProgressBar
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from random import randint
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

        # ปุ่มเกม Collect Item
        collect_button = Button(
            text="MiNi Game",
            font_size=20,
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
        )
        collect_button.bind(on_press=self.open_collect_game)
        layout.add_widget(collect_button)

        # เพิ่ม Layout ลงในหน้า
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = "game"

    def open_shop(self, instance):
        self.manager.current = "shop"

    def open_collect_game(self, instance):
        self.manager.current = "collect"


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
            spacing=5,
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
            text="Gold: 10",  # เริ่มต้นที่ 10 ทอง
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

        # เพิ่ม ProgressBar สำหรับอาหาร
        self.food_bar = ProgressBar(
            max=100,
            value=80,
            size_hint=(0.5, 0.05),
            pos_hint={"x": 0.3, "y": 0.2},
        )
        layout.add_widget(
            Label(
                text="Food:", size_hint=(0.2, 0.05), pos_hint={"x": 0.165, "y": 0.205}
            )
        )
        layout.add_widget(self.food_bar)

        # เพิ่ม ProgressBar สำหรับน้ำ
        self.water_bar = ProgressBar(
            max=100, value=70, size_hint=(0.5, 0.05), pos_hint={"x": 0.3, "y": 0.3}
        )
        layout.add_widget(
            Label(
                text="Water:", size_hint=(0.2, 0.05), pos_hint={"x": 0.165, "y": 0.305}
            )
        )
        layout.add_widget(self.water_bar)

        # ตัวอย่างปุ่มทดสอบการเพิ่มค่าอาหารและน้ำ
        increase_button = Button(
            text="Feed & Water", size_hint=(0.08, 0.08), pos_hint={"x": 1, "y": 1}
        )
        increase_button.bind(on_press=self.increase_values)
        layout.add_widget(increase_button)

        # ลดค่าหลอดอาหารและน้ำเมื่อเวลาผ่านไป
        Clock.schedule_interval(self.decrease_values, 2)

        # เพิ่ม Layout ต่างๆ ลงในหน้า
        layout.add_widget(anchor_layout_temp)
        layout.add_widget(anchor_layout)

        self.add_widget(layout)

        # อัปเดตข้อมูลเริ่มต้น
        self.update_temperature(0)
        self.update_monster()
        Clock.schedule_interval(self.update_temperature, 120)
        Clock.schedule_interval(self.update_monster, 30)

        # เรียกใช้ฟังก์ชันสำหรับการขยับมอนสเตอร์
        self.animate_monster()

    def animate_monster(self):
        # สร้าง Animation สำหรับการขยับมอนสเตอร์
        animation = Animation(
            pos_hint={"center_x": 0.5, "center_y": 0.55}, duration=1
        ) + Animation(pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=1)
        animation.repeat = True
        animation.start(self.monster_image)

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
            print(f"Error: The image file for {monster} does not exist.")
            self.monster_image.source = "default_monster.jpeg"  # แสดงภาพดีฟอลต์แทน

        self.monster_image.reload()  # ใช้ reload() เพื่อให้ภาพอัปเดตทันที

    def decrease_values(self, dt):
        if self.food_bar.value > 0:
            self.food_bar.value -= 1
        if self.water_bar.value > 0:
            self.water_bar.value -= 1

    def increase_values(self, instance):
        if self.food_bar.value < 100:
            self.food_bar.value += 10
        if self.water_bar.value < 100:
            self.water_bar.value += 10

    def go_back(self, instance):
        self.manager.current = "start"


# สร้างหน้าจอร้านค้า
class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # กำหนดราคาสินค้า
        self.item_prices = {
            "Food": 25,
            "Water": 10,
            "heater": 60,
            "Toy": 30,
        }

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        shop_label = Label(
            text="Welcome to the Shop!",
            font_size=40,
            color=(1, 1, 1, 1),
        )
        layout.add_widget(shop_label)

        # สร้างปุ่มสำหรับสินค้าแต่ละรายการ พร้อมแสดงราคา
        for item, price in self.item_prices.items():
            item_button = Button(
                text=f"{item}          -   {price} Gold",
                font_size=20,
                size_hint=(0.5, 0.2),
                pos_hint={"center_x": 0.5},
            )
            item_button.bind(on_press=self.buy_item)
            layout.add_widget(item_button)

        # ปุ่มกลับไปหน้าหลัก
        back_button = Button(
            text="Back",
            font_size=30,
            size_hint=(0.1, 0.095),
            pos_hint={"center_x": 0.95},
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def buy_item(self, instance):
        # ดึงชื่อสินค้าและราคาจากปุ่ม
        item_info = instance.text.split(" - ")
        item_name = item_info[0]
        item_price = int(item_info[1].split(" ")[0])

        # ดึงหน้าจอเกม
        game_screen = self.manager.get_screen("game")

        # ตรวจสอบว่ามีทองคำเพียงพอหรือไม่
        current_gold = int(game_screen.gold_label.text.split(": ")[1])
        if current_gold >= item_price:  # ถ้ามีทองคำเพียงพอ
            # อัปเดตจำนวนสินค้า
            game_screen.items_count[item_name] += 1
            game_screen.item_labels[item_name].text = (
                f"{item_name}: {game_screen.items_count[item_name]}"
            )
            # หักทองคำ
            game_screen.gold_label.text = f"Gold: {current_gold - item_price}"
        else:
            # แสดงข้อความแจ้งเตือน
            self.show_alert(f"Not enough gold! {item_name} costs {item_price} Gold.")

    def show_alert(self, message):
        # ฟังก์ชันสำหรับแสดงข้อความแจ้งเตือน
        alert = Label(
            text=message,
            font_size=20,
            color=(1, 0, 0, 1),  # Red color for alert message
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
        )
        self.add_widget(alert)

        # Remove the alert after a short period
        Clock.schedule_once(lambda dt: self.remove_alert(alert), 2)

    def remove_alert(self, alert):
        # Remove the alert label from the screen
        self.remove_widget(alert)

    def go_back(self, instance):
        self.manager.current = "start"


# สร้างแอปหลัก
class GameApp(App):
    def build(self):
        # สร้างหน้าจอหลัก
        sm = ScreenManager()

        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(ShopScreen(name="shop"))

        return sm


if __name__ == "__main__":
    GameApp().run()
