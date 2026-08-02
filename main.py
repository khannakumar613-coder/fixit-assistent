import os
import requests
import json
import base64
import threading
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from plyer import filechooser, tts

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    # Cream/Off-white Background
    md_bg_color: 0.96, 0.95, 0.92, 1

    # Header / Toolbar with Custom Logo
    MDBoxLayout:
        size_hint_y: None
        height: "65dp"
        padding: "10dp"
        spacing: "10dp"
        md_bg_color: 0.92, 0.90, 0.85, 1

        Image:
            source: 'logo.png'
            size_hint: None, None
            size: "45dp", "45dp"
            allow_stretch: True

        MDLabel:
            text: "FixIt Assistant"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: 0.2, 0.2, 0.2, 1
            bold: True

    # Chat Log Area
    ScrollView:
        MDBoxLayout:
            id: chat_box
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: "15dp"
            spacing: "15dp"

    # Bottom Input Bar
    MDBoxLayout:
        size_hint_y: None
        height: "70dp"
        padding: "10dp"
        spacing: "10dp"
        md_bg_color: 0.92, 0.90, 0.85, 1

        MDIconButton:
            icon: "camera"
            theme_icon_color: "Custom"
            icon_color: 0.2, 0.5, 0.4, 1
            on_release: app.open_camera_or_picker()

        MDIconButton:
            icon: "microphone"
            theme_icon_color: "Custom"
            icon_color: 0.8, 0.3, 0.3, 1
            on_release: app.listen_voice_input()

        MDTextField:
            id: user_input
            hint_text: "Ask FixIt Assistant..."
            mode: "rectangle"
            text_color_focus: 0.1, 0.1, 0.1, 1
            hint_text_color_focus: 0.4, 0.4, 0.4, 1
            active_line_color: 0.3, 0.5, 0.8, 1

        MDIconButton:
            icon: "send"
            theme_icon_color: "Custom"
            icon_color: 0.2, 0.5, 0.9, 1
            on_release: app.send_message()
'''

class FixItAssistant(MDApp):
    API_KEY = "AQ.Ab8RN6JoA-y4WGuQc30ACtgn08-8GwfA6LbvuBjyPAbzuxxKbw"

    def build(self):
        self.title = "FixIt Assistant"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def speak_text(self, text):
        """AI Jawab ko Bolkar sunayega (Text-To-Speech)"""
        try:
            tts.speak(text)
        except Exception:
            pass

    def add_message(self, text, is_user=True):
        """Cream Theme Bubbles"""
        bg_color = (0.2, 0.5, 0.8, 1) if is_user else (0.88, 0.86, 0.80, 1)
        text_color = (1, 1, 1, 1) if is_user else (0.1, 0.1, 0.1, 1)

        card = MDCard(
            size_hint_x=0.85,
            size_hint_y=None,
            padding="12dp",
            md_bg_color=bg_color,
            radius=[14, 14, 14, 14],
            pos_hint={'right': 1} if is_user else {'left': 1}
        )
        
        label = MDLabel(
            text=text,
            size_hint_y=None,
            theme_text_color="Custom",
            text_color=text_color
        )
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        card.bind(children=lambda instance, value: setattr(card, 'height', label.height + 24))
        
        card.add_widget(label)
        self.root.ids.chat_box.add_widget(card)

    def send_message(self):
        user_text = self.root.ids.user_input.text.strip()
        if not user_text:
            return

        self.add_message(user_text, is_user=True)
        self.root.ids.user_input.text = ""
        self.add_message("FixIt AI thinking...", is_user=False)

        threading.Thread(target=self.get_ai_response, args=(user_text,)).start()

    def get_ai_response(self, text, image_path=None):
        """Fast Gemini 1.5 Flash Response + Vision Support"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.API_KEY}"
            headers = {'Content-Type': 'application/json'}
            
            parts = [{"text": f"You are FixIt Assistant. Give clear, polite, and helpful solutions: {text}"}]
            
            # Agar image select ki gayi ho toh Base64 convert karke bhejenge
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    parts.append({
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_data
                        }
                    })

            payload = {"contents": [{"parts": parts}]}
            response = requests.post(url, headers=headers, json=payload, timeout=12)
            
            if response.status_code == 200:
                result = response.json()
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            else:
                ai_reply = "API issue. Please check API Key."

        except Exception as e:
            ai_reply = f"Error: {str(e)}"

        # UI update aur Speak out
        Clock.schedule_once(lambda dt: self.display_and_speak(ai_reply), 0)

    def display_and_speak(self, reply):
        self.add_message(reply, is_user=False)
        threading.Thread(target=self.speak_text, args=(reply,)).start()

    def open_camera_or_picker(self):
        """Camera / Gallery se image picking"""
        try:
            filechooser.open_file(on_selection=self.on_image_selected)
        except Exception:
            self.add_message("Unable to access storage/camera.", is_user=False)

    def on_image_selected(self, selection):
        if selection:
            img_path = selection[0]
            self.add_message("📷 Analyzing selected image...", is_user=True)
            threading.Thread(target=self.get_ai_response, args=("What is in this image and how to fix it?", img_path)).start()

    def listen_voice_input(self):
        """Microphone Voice Command"""
        self.add_message("🎙 Listening... Speak your prompt.", is_user=True)

if __name__ == '__main__':
    FixItAssistant().run()