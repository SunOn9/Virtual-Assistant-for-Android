import requests
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

with open("app/api_file.bin", mode='rb') as file:
    API = file.read()

Window.size = (350,500)

class MainApp(MDApp):
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signin.kv"))
        screen_manager.add_widget(Builder.load_file("main.kv"))
        return screen_manager
    
    def check_login(self, mail, passw):
        if mail == "tai":
            if passw == "123":
                screen_manager.current = "main"
            else:    
                toast("Incorrect Password !!!")
        else:
            toast("Invalid email !!!")
            
    def chat_bot(self, question):
        url = 'https://api.pawan.krd/v1/chat/completions'
        question = input()        
        headers = {
            'Authorization': API,
            'Content-Type': 'application/json',
        }

        json_data = {
            'model': 'gpt-3.5-turbo',
            'max_tokens': 100,
            'messages': [
                {
                    'role': 'user',
                    'content': question,
                },
            ],
        }
        response = requests.post(url, headers=headers, json=json_data).json()
        data = response["choices"][0]["message"]
        return (data["role"] +": "+ data["content"])
 
if __name__ == "__main__":
    MainApp().run()