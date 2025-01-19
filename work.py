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
from random import randint, shuffle
import random


class SettingsPopup(Popup):
    def __init__(self, start_screen, **kwargs):
        super().__init__(**kwargs)
        self.start_screen = start_screen
        self.title = "Settings"
        self.size_hint = (0.6, 0.4)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=20)
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

        close_button = Button(text="Close", size_hint=(1, 0.3))
        close_button.bind(on_press=self.dismiss)
        layout.add_widget(close_button)

        self.content = layout

    def toggle_mute(self, instance):
        if self.start_screen.background_music:
            if self.start_screen.background_music.volume > 0:
                self.start_screen.background_music.volume = 0
                self.mute_button.text = "Unmute"
            else:
                self.start_screen.background_music.volume = 0.5
                self.mute_button.text = "Mute"

    def volume_up(self, instance):
        if (
            self.start_screen.background_music
            and self.start_screen.background_music.volume < 1.0
        ):
            self.start_screen.background_music.volume = min(
                1.0, self.start_screen.background_music.volume + 0.1
            )

    def volume_down(self, instance):
        if (
            self.start_screen.background_music
            and self.start_screen.background_music.volume > 0
        ):
            self.start_screen.background_music.volume = max(
                0, self.start_screen.background_music.volume - 0.1
            )


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
            text="Welcome to the Game!",
            font_size=60,
            color=(0, 0, 0, 1),
        )
        layout.add_widget(welcome_label)

        start_button = Button(
            text="Start Game",
            font_size=20,
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
        )
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        shop_button = Button(
            text="Shop",
            font_size=20,
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
        )
        shop_button.bind(on_press=self.open_shop)
        layout.add_widget(shop_button)

        collect_button = Button(
            text="MiNi Game",
            font_size=20,
            size_hint=(0.5, 0.2),
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

    def open_shop(self, instance):
        self.manager.current = "shop"

    def open_collect_game(self, instance):
        self.manager.current = "collect"

    def on_leave(self):
        if self.background_music:
            self.background_music.stop()

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
            text="Temperature: -- °C",
            font_size=15,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 50),
            halign="left",
            valign="middle",
        )
        anchor_layout_temp.add_widget(self.temp_label)

        anchor_layout = AnchorLayout(anchor_x="right", anchor_y="top", padding=10)
        back_button = Button(
            text="Back",
            font_size=14,
            size_hint=(0.05, 0.05),
        )
        back_button.bind(on_press=self.go_back)
        anchor_layout.add_widget(back_button)

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
        self.items_count = {"Food": 5, "Water": 5, "heater": 0, "Toy": 0}
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
                item_image = DraggableItem(
                    main_screen=self,
                    item_type=item,
                    source=image_path,
                    size_hint=(1, 0.8),
                )
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

        Clock.schedule_interval(self.decrease_values, 2)

        layout.add_widget(anchor_layout_temp)
        layout.add_widget(anchor_layout)

        self.add_widget(layout)

        self.update_temperature(0)
        self.update_monster()
        Clock.schedule_interval(self.update_temperature, 120)
        Clock.schedule_interval(self.update_monster, 30)

        self.animate_monster()

    def animate_monster(self):
        animation = Animation(
            pos_hint={"center_x": 0.5, "center_y": 0.55}, duration=1
        ) + Animation(pos_hint={"center_x": 0.5, "center_y": 0.5}, duration=1)
        animation.repeat = True
        animation.start(self.monster_image)

    def update_temperature(self, dt):
        new_temp = random.randint(20, 40)
        self.temp_label.text = f"Temperature: {new_temp} °C"

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


class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

        for item, price in self.item_prices.items():
            item_button = Button(
                text=f"{item}          -   {price} Gold",
                font_size=20,
                size_hint=(0.5, 0.2),
                pos_hint={"center_x": 0.5},
            )
            item_button.bind(on_press=self.buy_item)
            layout.add_widget(item_button)

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
        item_name = instance.text.split()[0]
        item_price = self.item_prices[item_name]
        current_gold = int(self.manager.get_screen("game").gold_label.text.split()[1])

        if current_gold >= item_price:
            current_gold -= item_price
            self.manager.get_screen("game").gold_label.text = f"Gold: {current_gold}"
            self.manager.get_screen("game").items_count[item_name] += 1
            self.manager.get_screen("game").item_labels[
                item_name
            ].text = (
                f"{item_name}: {self.manager.get_screen('game').items_count[item_name]}"
            )

    def go_back(self, instance):
        self.manager.current = "start"


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
            pos_hint={"top": 0.95, "x": 0.05},
        )
        back_button.bind(on_press=self.go_back)

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
