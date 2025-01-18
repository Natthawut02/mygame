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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from random import randint, shuffle
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
            self.item_labels[item] = item_label
            self.item_widgets[item] = item_box

        layout.add_widget(self.items_layout_with_images)

        # เพิ่ม Layout แสดงเหรียญทอง
        self.gold_layout = AnchorLayout(anchor_x="right", anchor_y="bottom", padding=10)
        self.gold_image = Image(
            source="gold.jpeg",
            size_hint=(None, None),
            size=(230, 40),
        )
        self.gold_label = Label(
            text="Gold: 10",  # เริ่มต้นที่ 10 ทอง
            font_size=20,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(130, 40),
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
            font_size=20,
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def buy_item(self, instance):
        item_name = instance.text.split()[0]  # แยกชื่อไอเท็มจากข้อความปุ่ม
        item_price = self.item_prices[item_name]
        current_gold = int(self.manager.get_screen("game").gold_label.text.split()[1])

        if current_gold >= item_price:
            # หักเหรียญทองและอัปเดตจำนวนสินค้า
            current_gold -= item_price
            self.manager.get_screen("game").gold_label.text = f"Gold: {current_gold}"

            # เพิ่มจำนวนสินค้าใน GameScreen
            self.manager.get_screen("game").items_count[item_name] += 1
            self.manager.get_screen("game").item_labels[
                item_name
            ].text = (
                f"{item_name}: {self.manager.get_screen('game').items_count[item_name]}"
            )

    def go_back(self, instance):
        self.manager.current = "start"


# สร้างหน้าจอ Mini Game
class CollectGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # สร้าง FloatLayout เป็น layout หลัก
        main_layout = FloatLayout()

        # เพิ่มรูปพื้นหลัง
        background = Image(source="bk2.jpeg", allow_stretch=True, keep_ratio=False)
        main_layout.add_widget(background)

        # สร้างตัวแปรสำหรับเกมจับคู่
        self.cards = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6]
        shuffle(self.cards)
        self.selected = []
        self.buttons = []
        self.matches_found = 0
        self.gold = 0

        # สร้าง GridLayout สำหรับการ์ด
        self.game_layout = GridLayout(
            cols=4,
            spacing=5,
            padding=10,
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # สร้างปุ่มการ์ด
        for i in range(12):
            button = Button(
                text="",
                font_size=24,
                background_normal="",
                background_color=(0.7, 0.7, 0.7, 1),
            )
            button.card_value = self.cards[i]
            button.bind(on_press=self.reveal_card)
            self.buttons.append(button)
            self.game_layout.add_widget(button)

        # สร้าง layout สำหรับแสดงทอง
        gold_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={"top": 0.95, "right": 0.95},
        )

        self.gold_image = Image(
            source="gold.jpeg", size_hint=(None, None), size=(50, 50)
        )
        self.gold_label = Label(text=f": {self.gold}", font_size=24, color=(1, 1, 1, 1))
        gold_layout.add_widget(self.gold_image)
        gold_layout.add_widget(self.gold_label)

        # ปุ่มกลับ
        back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={"top": 0.95, "x": 0.05},
        )
        back_button.bind(on_press=self.go_back)

        # เพิ่ม widgets ทั้งหมดลงใน main_layout
        main_layout.add_widget(self.game_layout)
        main_layout.add_widget(gold_layout)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def reveal_card(self, button):
        if button.text == "" and len(self.selected) < 2:
            button.text = str(button.card_value)
            button.background_color = (1, 1, 1, 1)
            self.selected.append(button)

            if len(self.selected) == 2:
                Clock.schedule_once(self.check_match, 0.5)

    def check_match(self, dt):
        button1, button2 = self.selected

        if button1.card_value == button2.card_value:
            self.matches_found += 1
            self.gold += 10
            self.gold_label.text = f": {self.gold}"
            self.selected = []

            if self.matches_found == 6:
                # เมื่อชนะเกม ให้อัพเดทจำนวนทองในหน้า GameScreen
                game_screen = self.manager.get_screen("game")
                current_gold = int(game_screen.gold_label.text.split()[1])
                game_screen.gold_label.text = f"Gold: {current_gold + self.gold}"
                self.show_winner_popup()
        else:
            Clock.schedule_once(self.reset_cards, 0.5)

    def reset_cards(self, dt):
        for button in self.selected:
            button.text = ""
            button.background_color = (0.7, 0.7, 0.7, 1)
        self.selected = []

    def show_winner_popup(self):
        popup = Popup(
            title="Congratulations!",
            content=Label(text=f"You won!\nYou got {self.gold} gold!"),
            size_hint=(0.6, 0.4),
        )
        popup.bind(on_dismiss=self.reset_game)
        popup.open()

    def reset_game(self, instance=None):
        # รีเซ็ตเกมเมื่อเล่นจบ
        self.matches_found = 0
        self.gold = 0
        self.gold_label.text = f": {self.gold}"
        self.selected = []
        shuffle(self.cards)

        for i, button in enumerate(self.buttons):
            button.text = ""
            button.card_value = self.cards[i]
            button.background_color = (0.7, 0.7, 0.7, 1)

    def go_back(self, instance):
        self.reset_game()
        self.manager.current = "start"


# สร้าง ScreenManager
class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(ShopScreen(name="shop"))
        sm.add_widget(CollectGameScreen(name="collect"))
        return sm


if __name__ == "__main__":
    GameApp().run()
