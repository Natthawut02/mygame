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
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.behaviors import DragBehavior
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from random import randint, shuffle
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
import random
import json
import os


class SettingsPopup(Popup):
    def __init__(self, start_screen, **kwargs):
        super().__init__(**kwargs)
        self.start_screen = start_screen
        self.title = "Settings"
        self.size_hint = (0.6, 0.6)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        # Section: Sound Controls
        sound_controls = BoxLayout(orientation="vertical", spacing=10)

        self.mute_button = Button(
            text="Mute" if start_screen.background_music.volume > 0 else "Unmute",
            size_hint=(1, 0.3),
        )
        self.mute_button.bind(on_press=self.toggle_mute)

        volume_controls = BoxLayout(orientation="horizontal", spacing=10)
        volume_down = Button(text="Volume -", size_hint=(0.5, 1))
        volume_down.bind(on_press=self.volume_down)
        volume_up = Button(text="Volume +", size_hint=(0.5, 1))
        volume_up.bind(on_press=self.volume_up)

        volume_controls.add_widget(volume_down)
        volume_controls.add_widget(volume_up)

        sound_controls.add_widget(Label(text="Sound Settings", size_hint=(1, 0.3)))
        sound_controls.add_widget(self.mute_button)
        sound_controls.add_widget(volume_controls)

        layout.add_widget(sound_controls)

        # Section: Brightness Controls
        brightness_controls = BoxLayout(orientation="vertical", spacing=10)

        brightness_controls.add_widget(
            Label(text="Brightness Settings", size_hint=(1, 0.3))
        )

        self.brightness_slider = Slider(
            min=0, max=100, value=Window.clearcolor[0] * 100
        )
        self.brightness_slider.bind(value=self.on_brightness_change)
        brightness_controls.add_widget(self.brightness_slider)

        layout.add_widget(brightness_controls)

        # Close Button
        close_button = Button(text="Close", size_hint=(1, 0.3))
        close_button.bind(on_press=self.dismiss)
        layout.add_widget(close_button)

        self.content = layout

    # Toggle Mute
    def toggle_mute(self, instance):
        if self.start_screen.background_music:
            if self.start_screen.background_music.volume > 0:
                self.start_screen.background_music.volume = 0
                self.mute_button.text = "Unmute"
            else:
                self.start_screen.background_music.volume = 0.5
                self.mute_button.text = "Mute"

    # Volume Up
    def volume_up(self, instance):
        if (
            self.start_screen.background_music
            and self.start_screen.background_music.volume < 1.0
        ):
            self.start_screen.background_music.volume = min(
                1.0, self.start_screen.background_music.volume + 0.1
            )

    # Volume Down
    def volume_down(self, instance):
        if (
            self.start_screen.background_music
            and self.start_screen.background_music.volume > 0
        ):
            self.start_screen.background_music.volume = max(
                0, self.start_screen.background_music.volume - 0.1
            )

    # Brightness Change
    def on_brightness_change(self, instance, value):
        brightness = value / 100
        Window.clearcolor = [brightness] * 3 + [1]  # Update brightness
        print(f"Brightness: {int(value)}%")


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_music = SoundLoader.load("saw.mp3")
        if self.background_music:
            self.background_music.loop = True
            self.background_music.volume = 0.5
            self.background_music.play()

        background = Image(source="bk1.jpeg", allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        settings_layout = AnchorLayout(anchor_x="right", anchor_y="top", padding=10)
        settings_button = Button(
            background_normal="setting.jpeg",
            size_hint=(None, None),
            size=(80, 80),
        )
        settings_button.bind(on_press=self.open_settings)
        settings_layout.add_widget(settings_button)
        self.add_widget(settings_layout)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)

        welcome_label = Label(
            text="",
            font_size=60,
            color=(0, 0, 0, 1),
        )
        layout.add_widget(welcome_label)
        layout = BoxLayout(orientation="vertical")

        img = Image(
            source="wk.jpeg",
            size_hint=(0.3, 0.3),
            pos_hint={"center_x": 0.5, "center_y": 10},
        )

        layout.add_widget(img)
        start_button = Button(
            text="Start Game",
            font_size=20,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5},
        )
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        load_button = Button(
            text="Load Game",
            font_size=20,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5},
        )
        load_button.bind(on_press=self.load_game)
        layout.add_widget(load_button)

        shop_button = Button(
            text="shop",
            font_size=20,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5},
        )
        shop_button.bind(on_press=self.open_shop)
        layout.add_widget(shop_button)

        collect_button = Button(
            text="MiNi Game",
            font_size=20,
            size_hint=(0.5, 0.05),
            pos_hint={"center_x": 0.5},
        )
        collect_button.bind(on_press=self.open_collect_game)
        layout.add_widget(collect_button)

        self.add_widget(layout)

    def open_settings(self, instance):
        settings_popup = SettingsPopup(self)
        settings_popup.open()

    def start_game(self, instance):
        self.manager.current = "game"
        self.stop_music()

    def load_game(self, instance):
        self.manager.current = "load"
        self.stop_music()

    def open_shop(self, instance):
        self.manager.current = "shop"
        self.stop_music()

    def open_collect_game(self, instance):
        self.manager.current = "collect"
        self.stop_music()

    def stop_music(self):
        if self.background_music:
            self.background_music.stop()

    def on_leave(self):
        self.stop_music()

    def on_enter(self):
        if self.background_music and not self.background_music.state == "play":
            self.background_music.play()


class DraggableItem(DragBehavior, Image):
    def __init__(self, main_screen, item_type, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.item_type = item_type
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.drag_rectangle = [0, 0, Window.width, Window.height]
        self.drag_timeout = 10000000
        self.drag_distance = 0
        self.original_pos = self.pos

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            monster_widget = self.main_screen.monster_image
            monster_x = monster_widget.x
            monster_y = monster_widget.y
            monster_right = monster_x + monster_widget.width
            monster_top = monster_y + monster_widget.height

            if (
                monster_x <= self.x <= monster_right
                and monster_y <= self.y <= monster_top
            ):
                if (
                    self.item_type == "Food"
                    and self.main_screen.items_count["Food"] > 0
                ):
                    self.main_screen.food_bar.value = min(
                        100, self.main_screen.food_bar.value + 20
                    )
                    self.main_screen.items_count["Food"] -= 1
                elif (
                    self.item_type == "Water"
                    and self.main_screen.items_count["Water"] > 0
                ):
                    self.main_screen.water_bar.value = min(
                        100, self.main_screen.water_bar.value + 20
                    )
                    self.main_screen.items_count["Water"] -= 1

                self.main_screen.item_labels[self.item_type].text = (
                    f"{self.item_type}: {self.main_screen.items_count[self.item_type]}"
                )

            Animation(pos=self.original_pos, duration=0.1).start(self)
        return super().on_touch_up(touch)


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = RelativeLayout()

        background = Image(source="bk2.jpeg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        anchor_layout_temp = AnchorLayout(anchor_x="left", anchor_y="top", padding=10)
        self.temp_label = Label(
            text="°C",
            font_size=15,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 50),
            halign="left",
            valign="middle",
        )
        anchor_layout_temp.add_widget(self.temp_label)

        anchor_layout_left = AnchorLayout(anchor_x="left", anchor_y="top", padding=10)
        settings_button = Button(
            background_normal="setting.jpeg",
            size_hint=(None, None),
            size=(80, 80),
        )
        settings_button.bind(on_press=self.toggle_music)
        anchor_layout_left.add_widget(settings_button)

        anchor_layout_right = AnchorLayout(anchor_x="right", anchor_y="top", padding=10)
        back_button = Button(
            text="Back",
            font_size=14,
            size_hint=(0.05, 0.05),
        )
        back_button.bind(on_press=self.go_back)
        anchor_layout_right.add_widget(back_button)

        save_button = Button(
            text="Save Game",
            font_size=14,
            size_hint=(0.1, 0.05),
            pos_hint={"x": 0.9, "y": 0.85},
        )
        save_button.bind(on_press=self.save_game)
        layout.add_widget(save_button)

        shop_button = Button(
            text="Shop",
            font_size=14,
            size_hint=(0.1, 0.05),
            pos_hint={"x": 0.9, "y": 0.65},
        )
        shop_button.bind(on_press=self.open_shop)
        layout.add_widget(shop_button)

        mini_game_button = Button(
            text="Mini Game",
            font_size=14,
            size_hint=(0.1, 0.05),
            pos_hint={"x": 0.9, "y": 0.75},
        )
        mini_game_button.bind(on_press=self.open_mini_game)
        layout.add_widget(mini_game_button)

        sell_button = Button(
            text="Sell Monster",
            font_size=14,
            size_hint=(0.1, 0.05),
            pos_hint={"x": 0.9, "y": 0.55},
        )
        sell_button.bind(on_press=self.sell_monster)
        layout.add_widget(sell_button)

        self.monster_image = Image(
            source="diji.jpeg",
            size_hint=(0.2, 0.3),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        layout.add_widget(self.monster_image)

        self.items_layout_with_images = BoxLayout(
            orientation="horizontal",
            spacing=5,
            size_hint=(0.4, 0.12),
            pos_hint={"x": 0.02, "y": 0.02},
        )

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

            if item in ["Food", "Water"]:
                item_image = Image(source=image_path, size_hint=(1, 0.8))
            else:
                item_image = Image(source=image_path, size_hint=(1, 0.8))

            item_label = Label(
                text=f"{item}: {self.items_count[item]}",
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

        self.gold_layout = AnchorLayout(anchor_x="right", anchor_y="bottom", padding=10)
        self.gold_image = Image(
            source="gold.jpeg",
            size_hint=(None, None),
            size=(230, 40),
        )
        self.gold_label = Label(
            text="Gold: 10",
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

        self.health_bar = ProgressBar(
            max=100,
            value=100,
            size_hint=(0.5, 0.05),
            pos_hint={"x": 0.300, "y": 0.800},
        )
        layout.add_widget(
            Label(
                text="Health:", size_hint=(0.2, 0.05), pos_hint={"x": 0.165, "y": 0.8}
            )
        )
        layout.add_widget(self.health_bar)

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

        self.water_bar = ProgressBar(
            max=100,
            value=70,
            size_hint=(0.5, 0.05),
            pos_hint={"x": 0.3, "y": 0.3},
        )
        layout.add_widget(
            Label(
                text="Water:", size_hint=(0.2, 0.05), pos_hint={"x": 0.165, "y": 0.305}
            )
        )
        layout.add_widget(self.water_bar)
        self.bar_color = Color(1, 0, 0, 1)
        self.care_bar = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.5, 0.05),
            pos_hint={"x": 0.3, "y": 0.9},
        )
        layout.add_widget(
            Label(text="Care:", size_hint=(0.2, 0.05), pos_hint={"x": 0.165, "y": 0.9})
        )
        layout.add_widget(self.care_bar)

        layout.add_widget(anchor_layout_temp)
        layout.add_widget(anchor_layout_left)
        layout.add_widget(anchor_layout_right)

        self.add_widget(layout)

        Clock.schedule_interval(self.decrease_values, 2)
        Clock.schedule_interval(self.check_health, 1)

        self.update_temperature(0)
        self.update_monster()
        Clock.schedule_interval(
            self.update_temperature, 120
        )  # Update temperature every 2 minutes
        Clock.schedule_interval(self.update_monster, 30)

        self.animate_monster()

        # Add touch event bindings for food, water, and heater images
        self.item_widgets["Food"].children[1].bind(
            on_touch_down=self.on_touch_down_food
        )
        self.item_widgets["Water"].children[1].bind(
            on_touch_down=self.on_touch_down_water
        )
        self.item_widgets["heater"].children[1].bind(
            on_touch_down=self.on_touch_down_heater
        )

        self.alert_sound = None

        # Load and play background music
        self.background_music = SoundLoader.load("game_music.mp3")
        if self.background_music:
            self.background_music.loop = True
            self.background_music.volume = 0.5

    def save_game(self, instance):
        content = BoxLayout(orientation="vertical", padding=10)

        # Add image to the popup
        save_image = Image(source="save_icon.png", size_hint=(1, 0.5))
        content.add_widget(save_image)

        save_name_input = TextInput(hint_text="Enter save name", multiline=False)
        content.add_widget(save_name_input)

        save_button = Button(text="Save", size_hint=(1, 0.3))
        save_button.bind(on_press=lambda x: self.save_game_state(save_name_input.text))
        content.add_widget(save_button)

        popup = Popup(
            title="Save Game", content=content, size_hint=(0.6, 0.6), auto_dismiss=True
        )
        popup.open()

    def save_game_state(self, save_name):
        game_state = {
            "health": self.health_bar.value,
            "food": self.food_bar.value,
            "water": self.water_bar.value,
            "gold": self.gold_label.text.split()[1],
            "items_count": self.items_count,
            "care": self.care_bar.value,
        }
        save_path = os.path.join(os.getcwd(), f"{save_name}.json")
        with open(save_path, "w") as save_file:
            json.dump(game_state, save_file)

    def load_game_state(self, save_name):
        save_path = os.path.join(os.getcwd(), f"{save_name}.json")
        try:
            with open(save_path, "r") as save_file:
                game_state = json.load(save_file)
                self.health_bar.value = game_state["health"]
                self.food_bar.value = game_state["food"]
                self.water_bar.value = game_state["water"]
                self.gold_label.text = f"Gold: {game_state['gold']}"
                self.items_count = game_state["items_count"]
                self.care_bar.value = game_state["care"]
                for item, count in self.items_count.items():
                    self.item_labels[item].text = f"{item}: {count}"
        except FileNotFoundError:
            print(f"Error: Save file {save_name}.json not found.")

    def sell_monster(self, instance):
        if self.care_bar.value < 100:
            popup = Popup(
                title="Cannot Sell",
                content=Label(
                    text="Care bar must be full to sell the monster.",
                    color=(0.8, 0.2, 0.2, 1),
                ),
                size_hint=(0.6, 0.2),
                background_color=(0.9, 0.9, 0.9, 1),
            )
            popup.open()
            return

        sell_price = 50  # Define the price for selling the monster
        current_gold = int(self.gold_label.text.split()[1])
        self.gold_label.text = f"Gold: {current_gold + sell_price}"
        self.monster_image.source = (
            "default_monster.jpeg"  # Reset to default monster image
        )
        self.monster_image.reload()

    def on_touch_down_food(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.increase_food()

    def on_touch_down_water(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.increase_water()

    def on_touch_down_heater(self, instance, touch):
        if instance.collide_point(*touch.pos) and self.items_count["heater"] > 0:
            if self.alert_sound:
                self.alert_sound.stop()
                self.alert_sound = None

    def increase_food(self):
        if self.food_bar.value < 100 and self.items_count["Food"] > 0:
            self.food_bar.value = min(100, self.food_bar.value + 10)
            self.items_count["Food"] -= 1
            self.item_labels["Food"].text = f"Food: {self.items_count['Food']}"
            self.care_bar.value = min(100, self.care_bar.value + 5)

    def increase_water(self):
        if self.water_bar.value < 100 and self.items_count["Water"] > 0:
            self.water_bar.value = min(100, self.water_bar.value + 10)
            self.items_count["Water"] -= 1
            self.item_labels["Water"].text = f"Water: {self.items_count['Water']}"
            self.care_bar.value = min(100, self.care_bar.value + 5)

    def check_health(self, dt):
        if self.food_bar.value <= 0 or self.water_bar.value <= 0:
            if self.health_bar.value > 0:
                self.health_bar.value = max(0, self.health_bar.value - 0.5)
                self.monster_image.opacity = max(0.3, self.health_bar.value / 100)

                if self.health_bar.value <= 0:
                    self.show_game_over()
        elif self.health_bar.value < 100:
            self.health_bar.value = min(100, self.health_bar.value + 0.2)
            self.monster_image.opacity = max(0.3, self.health_bar.value / 100)

    def show_game_over(self):
        content = BoxLayout(orientation="vertical", padding=10)
        content.add_widget(Label(text="Game Over!\nYour monster has died."))

        restart_button = Button(text="Restart", size_hint=(1, 0.3))
        restart_button.bind(on_press=self.restart_game)
        content.add_widget(restart_button)

        popup = Popup(
            title="Game Over", content=content, size_hint=(0.6, 0.4), auto_dismiss=False
        )
        popup.open()

    def restart_game(self, instance):
        self.health_bar.value = 100
        self.food_bar.value = 80
        self.water_bar.value = 70
        self.monster_image.opacity = 1
        self.items_count = {"Food": 0, "Water": 0, "heater": 0, "Toy": 0}
        self.care_bar.value = 0

        for item, count in self.items_count.items():
            self.item_labels[item].text = f"{item}: {count}"

        for child in Window.children[:]:
            if isinstance(child, Popup):
                child.dismiss()

    def animate_monster(self):
        animation = Animation(
            pos_hint={"center_x": 0.5, "center_y": 0.55}, duration=1
        ) + Animation(pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=1)
        animation.repeat = True
        animation.start(self.monster_image)

    def update_temperature(self, dt):
        temp = random.choices(
            population=[
                random.randint(20, 24),
                random.randint(25, 35),
                random.randint(36, 40),
            ],
            weights=[1, 8, 1],
            k=1,
        )[0]
        self.temp_label.text = f" {temp} °C"

        if temp < 25 or temp > 35:
            if not self.alert_sound:
                self.alert_sound = SoundLoader.load("alert.mp3")
                if self.alert_sound:
                    self.alert_sound.play()
            self.health_bar.value = max(0, self.health_bar.value - 1)

    def update_monster(self, dt=None):
        monsters = ["diji"]
        monster = random.choice(monsters)
        image_path = f"{monster.lower()}.jpeg"
        try:
            with open(image_path, "rb"):
                self.monster_image.source = image_path
        except FileNotFoundError:
            print(f"Error: The image file for {monster} does not exist.")
            self.monster_image.source = "default_monster.jpeg"
        self.monster_image.reload()

    def decrease_values(self, dt):
        if self.food_bar.value > 0:
            self.food_bar.value -= 1
        if self.water_bar.value > 0:
            self.water_bar.value -= 1

    def go_back(self, instance):
        self.manager.current = "start"
        self.stop_music()

    def open_mini_game(self, instance):
        self.manager.current = "collect"
        self.stop_music()

    def open_shop(self, instance):
        self.manager.current = "shop"
        self.stop_music()

    def toggle_music(self, instance):
        if self.background_music:
            if self.background_music.volume > 0:
                self.background_music.volume = 0
            else:
                self.background_music.volume = 0.5

    def stop_music(self):
        if self.background_music:
            self.background_music.stop()

    def on_enter(self):
        if self.background_music and not self.background_music.state == "play":
            self.background_music.play()


class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # เพิ่มการตรวจสอบไฟล์เสียงร้านค้า
        try:
            self.shop_music = SoundLoader.load("shop.mp3")
            if self.shop_music:
                self.shop_music.loop = True
                self.shop_music.volume = 0.5
        except:
            print("Warning: Could not load shop music")
            self.shop_music = None

        main_layout = FloatLayout()

        background = Image(
            source="shop_background.jpeg", allow_stretch=True, keep_ratio=False
        )
        main_layout.add_widget(background)

        overlay = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        with overlay.canvas.before:
            Color(0, 0, 0, 0.7)
            Rectangle(pos=overlay.pos, size=overlay.size)
        main_layout.add_widget(overlay)

        content_layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=30,
            size_hint=(0.9, 0.9),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        header_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, 0.15), padding=[10, 5]
        )
        with header_layout.canvas.before:
            Color(0, 0, 0, 0.8)
            Rectangle(pos=header_layout.pos, size=header_layout.size)

        shop_label = Label(
            text="JY HET BY DIE WINKEL AANGEKOM",
            font_size=40,
            color=(1, 0.8, 0.2, 1),
            bold=True,
            size_hint=(0.8, 1),
            outline_width=2,
            outline_color=(0, 0, 0, 1),
        )

        self.gold_display = BoxLayout(
            orientation="horizontal",
            size_hint=(0.2, 1),
            padding=(5, 0),
            spacing=5,
        )

        with self.gold_display.canvas.before:
            Color(0, 0, 0, 0.6)
            Rectangle(pos=self.gold_display.pos, size=self.gold_display.size)

        gold_icon = Image(
            source="gold.jpeg",
            size_hint=(None, None),
            size=(30, 30),
            pos_hint={"center_y": 0.5},
        )

        self.gold_amount = Label(
            text="0",
            font_size=28,
            color=(1, 0.8, 0.2, 1),
            bold=True,
            size_hint=(1, 1),
            pos_hint={"center_y": 0.5},
        )

        self.gold_display.add_widget(gold_icon)
        self.gold_display.add_widget(self.gold_amount)

        header_layout.add_widget(shop_label)
        header_layout.add_widget(self.gold_display)
        content_layout.add_widget(header_layout)

        self.item_prices = {
            "Food": {"price": 25, "description": "Restores 20% hunger"},
            "Water": {"price": 10, "description": "Restores 20% thirst"},
            "heater": {"price": 60, "description": "Keeps your pet warm"},
            "Toy": {"price": 30, "description": "Makes your pet happy"},
        }

        items_grid = GridLayout(
            cols=2, spacing=15, size_hint=(1, 0.7), padding=[10, 10]
        )

        for item, details in self.item_prices.items():
            item_card = BoxLayout(orientation="vertical", spacing=5, padding=10)

            with item_card.canvas.before:
                Color(0.1, 0.1, 0.1, 0.9)
                Rectangle(pos=item_card.pos, size=item_card.size)

            image_container = BoxLayout(size_hint=(1, 0.6), padding=[2, 2])
            with image_container.canvas.before:
                Color(1, 1, 1, 0.8)
                Rectangle(pos=image_container.pos, size=image_container.size)

            item_image = Image(source=f"{item.lower()}.jpeg", size_hint=(1, 1))
            image_container.add_widget(item_image)

            item_name = Label(
                text=item,
                font_size=24,
                color=(1, 1, 1, 1),
                size_hint=(1, 0.15),
                bold=True,
                outline_width=1,
                outline_color=(0, 0, 0, 1),
            )

            price_label = Label(
                text=f"{details['price']} Gold",
                font_size=20,
                color=(1, 0.8, 0.2, 1),
                size_hint=(1, 0.15),
                bold=True,
                outline_width=1,
                outline_color=(0, 0, 0, 1),
            )

            description_label = Label(
                text=details["description"],
                font_size=16,
                color=(0.9, 0.9, 0.9, 1),
                size_hint=(1, 0.15),
                outline_width=1,
                outline_color=(0, 0, 0, 1),
            )

            buy_button = Button(
                text="BUY",
                font_size=20,
                size_hint=(0.8, 0.2),
                pos_hint={"center_x": 0.5},
                background_normal="",
                background_color=(0.2, 0.6, 0.2, 1),
                bold=True,
            )
            buy_button.item_name = item
            buy_button.bind(on_press=self.buy_item)

            item_card.add_widget(image_container)
            item_card.add_widget(item_name)
            item_card.add_widget(price_label)
            item_card.add_widget(description_label)
            item_card.add_widget(buy_button)

            items_grid.add_widget(item_card)

        content_layout.add_widget(items_grid)

        back_button = Button(
            text="BACK",
            font_size=24,
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_color=(0.8, 0.2, 0.2, 1),
            bold=True,
        )
        back_button.bind(on_press=self.go_back)
        content_layout.add_widget(back_button)

        game_button = Button(
            text="Game",
            font_size=24,
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "y": 0.1},
            background_normal="",
            background_color=(0.2, 0.6, 0.2, 1),
            bold=True,
        )
        game_button.bind(on_press=self.go_to_game)
        content_layout.add_widget(game_button)

        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def on_enter(self):
        if self.shop_music and not self.shop_music.state == "play":
            try:
                self.shop_music.play()
            except:
                print("Warning: Could not play shop music")

        current_gold = int(self.manager.get_screen("game").gold_label.text.split()[1])
        self.gold_amount.text = str(current_gold)

        start_screen = self.manager.get_screen("start")
        if start_screen.background_music:
            start_screen.background_music.stop()

    def on_leave(self):
        if self.shop_music:
            try:
                self.shop_music.stop()
            except:
                print("Warning: Could not stop shop music")

        start_screen = self.manager.get_screen("start")
        if start_screen.background_music:
            start_screen.background_music.play()

    def buy_item(self, instance):
        item_name = instance.item_name
        item_price = self.item_prices[item_name]["price"]
        current_gold = int(self.manager.get_screen("game").gold_label.text.split()[1])

        if current_gold >= item_price:
            current_gold -= item_price
            self.manager.get_screen("game").gold_label.text = f"Gold: {current_gold}"
            self.gold_amount.text = str(current_gold)
            self.manager.get_screen("game").items_count[item_name] += 1
            self.manager.get_screen("game").item_labels[
                item_name
            ].text = (
                f"{item_name}: {self.manager.get_screen('game').items_count[item_name]}"
            )

            # แสดง Popup เมื่อซื้อสำเร็จ
            popup = Popup(
                title="Purchase Successful!",
                content=Label(
                    text=f"You bought 1 {item_name}!", color=(0.2, 0.8, 0.2, 1)
                ),
                size_hint=(0.6, 0.2),
                background_color=(0.9, 0.9, 0.9, 1),
            )
            popup.open()

            # พยายามเล่นเสียงซื้อของ ถ้าไม่มีไฟล์ก็จะข้ามไป
            try:
                # ลองใช้เสียงตัวอื่นที่มีอยู่แล้วในเกม
                purchase_sound = SoundLoader.load("shop.mp3")  # ใช้เสียงร้านค้าแทน
                if purchase_sound:
                    purchase_sound.volume = 0.3  # ลดเสียงลงเพื่อไม่ให้ดังเกินไป
                    purchase_sound.play()
            except:
                print("Warning: Could not play purchase sound")
        else:
            needed_gold = item_price - current_gold
            popup = Popup(
                title="Cannot Purchase",
                content=Label(
                    text=f"Not enough gold!\nYou need {needed_gold} more gold.",
                    color=(0.8, 0.2, 0.2, 1),
                ),
                size_hint=(0.6, 0.2),
                background_color=(0.9, 0.9, 0.9, 1),
            )
            popup.open()

    def go_back(self, instance):
        self.manager.current = "start"

    def go_to_game(self, instance):
        self.manager.current = "game"


class CollectGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = FloatLayout()

        background = Image(source="bk2.jpeg", allow_stretch=True, keep_ratio=False)
        main_layout.add_widget(background)

        self.cards = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6]
        shuffle(self.cards)
        self.selected = []
        self.buttons = []
        self.matches_found = 0
        self.gold = 0

        self.game_layout = GridLayout(
            cols=4,
            spacing=5,
            padding=10,
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

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

        back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={"top": 0.95, "right": 0.05},
        )
        back_button.bind(on_press=self.go_back)

        game_button = Button(
            text="Game",
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={"bottom": 0.05, "right": 0.05},
        )
        game_button.bind(on_press=self.go_to_game)

        main_layout.add_widget(self.game_layout)
        main_layout.add_widget(gold_layout)
        main_layout.add_widget(back_button)
        main_layout.add_widget(game_button)

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
                game_screen = self.manager.get_screen("game")
                current_gold = int(game_screen.gold_label.text.split()[1])
                game_screen.gold_label.text = f"Gold: {current_gold + self.gold}"
                self.show_winner_popup()
        else:
            Clock.schedule_once(self.hide_cards, 0.5)

    def hide_cards(self, dt):
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

    def go_to_game(self, instance):
        self.reset_game()
        self.manager.current = "game"


class LoadGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Add background image
        background = Image(
            source="load_background.jpeg", allow_stretch=True, keep_ratio=False
        )
        self.add_widget(background)

        self.save_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.save_list.bind(minimum_height=self.save_list.setter("height"))

        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(self.save_list)

        layout.add_widget(scroll_view)

        back_button = Button(text="Back", size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        self.load_saves()

    def load_saves(self):
        self.save_list.clear_widgets()
        save_files = [f for f in os.listdir(os.getcwd()) if f.endswith(".json")]
        for save_file in save_files:
            save_layout = BoxLayout(size_hint_y=None, height=40)
            save_button = Button(text=save_file, size_hint_x=0.8)
            save_button.bind(on_press=lambda instance, sf=save_file: self.load_game(sf))
            delete_button = Button(text="Delete", size_hint_x=0.2)
            delete_button.bind(
                on_press=lambda instance, sf=save_file: self.delete_save(sf)
            )
            save_layout.add_widget(save_button)
            save_layout.add_widget(delete_button)
            self.save_list.add_widget(save_layout)

    def load_game(self, save_file):
        game_screen = self.manager.get_screen("game")
        game_screen.load_game_state(save_file.replace(".json", ""))
        self.manager.current = "game"

    def delete_save(self, save_file):
        save_path = os.path.join(os.getcwd(), save_file)
        if os.path.exists(save_path):
            os.remove(save_path)
            self.load_saves()

    def go_back(self, instance):
        self.manager.current = "start"


class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(ShopScreen(name="shop"))
        sm.add_widget(CollectGameScreen(name="collect"))
        sm.add_widget(LoadGameScreen(name="load"))
        return sm


if __name__ == "__main__":
    GameApp().run()
