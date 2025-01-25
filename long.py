from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from random import shuffle
from kivy.clock import Clock


class MemoryMatchApp(App):
    def build(self):
        self.cards = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6]
        shuffle(self.cards)  # สุ่มตัวเลข
        self.selected = []
        self.buttons = []
        self.matches_found = 0
        self.gold = 0  # ตัวแปรเก็บทอง

        layout = GridLayout(cols=4)  # สร้างกริดที่มี 4 คอลัมน์

        # สร้างปุ่มให้เป็นการ์ด
        for i in range(12):
            button = Button(text="", font_size=24, on_press=self.reveal_card)
            button.card_value = self.cards[i]
            self.buttons.append(button)
            layout.add_widget(button)

        # สร้าง GridLayout ใหม่สำหรับวางรูปทองและป้ายทอง
        gold_layout = GridLayout(
            cols=2, size_hint=(None, None), size=(60, 60)
        )  # ใช้ 2 คอลัมน์
        self.gold_label = Label(text=f": {self.gold}", font_size=24)
        self.gold_image = Image(
            source="gold.jpeg", size_hint=(None, None), size=(70, 70)
        )

        # เพิ่มทั้งรูปทองและป้ายทองใน GridLayout ใหม่
        gold_layout.add_widget(self.gold_image)
        gold_layout.add_widget(self.gold_label)

        # วาง GridLayout ของทองในตำแหน่งที่ต้องการใน GridLayout หลัก
        layout.add_widget(gold_layout)

        self.layout = layout
        return layout

    def reveal_card(self, button):
        if button.text == "":  # เฉพาะปุ่มที่ยังไม่ได้เปิด
            button.text = str(button.card_value)
            self.selected.append(button)

            # เช็คการจับคู่
            if len(self.selected) == 2:
                self.check_match()

    def check_match(self):
        button1, button2 = self.selected

        if button1.card_value == button2.card_value:
            self.matches_found += 1
            self.gold += 10  # เพิ่มทองเมื่อจับคู่ถูกต้อง
            self.gold_label.text = f": {self.gold}"  # อัปเดตทองบนหน้าจอ
            self.selected = []

            if self.matches_found == 6:
                self.show_winner_popup()
        else:
            # เมื่อจับคู่ผิด ให้ปิดการ์ดทั้งสองใบหลังจาก 1 วินาที
            Clock.schedule_once(self.reset_cards, 0.5)

    def reset_cards(self, dt):
        # ปิดการ์ดที่ไม่ตรงกัน
        for button in self.selected:
            button.text = ""
        self.selected = []  # รีเซ็ตการเลือก

    def show_winner_popup(self):
        popup = Popup(
            title="You Win!",
            content=Label(text=f"you get gold: {self.gold}"),
            size_hint=(0.6, 0.4),
        )
        popup.open()


if __name__ == "__main__":
    MemoryMatchApp().run()
