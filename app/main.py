import requests
import re
import pymongo
import datetime
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

with open("app/api_file.bin", mode='rb') as file:
    API = file.read()
    
with open("app/mongodb_file.bin", mode='rb') as file:
    mongo_id = file.read()
    

myclient = pymongo.MongoClient(mongo_id.decode("utf-8") )
mydb = myclient["vafa"]
myuser = mydb["user"]
myhis = mydb["history"]

Window.size = (350,500)

class MainApp(MDApp):
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signin.kv"))
        screen_manager.add_widget(Builder.load_file("main.kv"))
        return screen_manager
    
    def to_sign(self):
        screen_manager.current = "signin"
    
    def to_login(self):
        screen_manager.current = "login"
        
    def to_main(self):
        screen_manager.current = "main"
        
    def signin(self, mail, passw, repassw):
        myquery = {"mail": mail}
        if re.match(r"^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$", mail):
            if myuser.count_documents(myquery):
                toast("This email is already registered !!!")
            else:
                if len(passw) < 8:
                    toast("Password length must be greater than 8 !!!")
                else:
                    if repassw != passw:
                        toast("Different re-enter password !!!")
                    else:
                        user = {
                            "mail": mail,
                            "password": passw,
                        }
                        myuser.insert_one(user)
        else:
            toast("Invalid email !!!")
            
    def check_login(self, mail, passw):
        myquery = {"mail": mail}
        user = myuser.find(myquery)[0]
        if re.match(r"^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$", mail):
            if myuser.count_documents(myquery):
                if len(passw) < 8:
                    toast("Password length must be greater than 8 !!!")
                else:
                    if passw == user["password"]:
                        MainApp.to_main(self)
                    else:    
                        toast("Incorrect Password !!!")
            else:
                toast("Unregistered email !!!")
        else:
            toast("Invalid email !!!")
              
    def chat_bot(self, question, id):
        url = 'https://api.pawan.krd/v1/chat/completions'
            
        headers = {
        'Authorization': API,
        'Content-Type': 'application/json',
        }

        json_data = {
            'model': 'gpt-3.5-turbo',
            'max_tokens': 4000,
            'stop': 'None',
            'messages': [
                {
                    'role': 'user',
                    'content': question,
                },
            ],
        }
        response = requests.post(url, headers=headers, json=json_data).json()
        try:
            data = response["choices"][0]["message"]
            print("Assistant: "+data["content"])
            
            #push data to DB
            now = datetime.datetime.now()
            history = {
                "id": id,
                "question": question,
                "response": data["content"],
                "time": now,
            }
            myhis.insert_one(history)
        except:
            print("Assistant: I do not understand what you say! Can you be more specific again?")
 
if __name__ == "__main__":
    MainApp().run()