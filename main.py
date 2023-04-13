import re
from time import localtime, strftime
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, NumericProperty
import urllib
import urllib.request
import json
import ssl
from kivy.core.window import Window
from kivy.uix.image import AsyncImage

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()    
        
class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()   

class Time(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    font_size = 20

class MyImage(AsyncImage):
    pass
                
class MainApp(MDApp) :
    global screen_manager , pass_screen
    current_id = ""
    current_type = ""
    ssl._create_default_https_context = ssl._create_unverified_context  
    Window.softinput_mode = "below_target"
    screen_manager = ScreenManager()
        
    def build(self):
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("image.kv"))
        screen_manager.add_widget(Builder.load_file("signin.kv"))
        screen_manager.add_widget(Builder.load_file("history.kv"))
        return screen_manager

    def to_img(self):
        screen_manager.transition.direction = "up"
        screen_manager.current = "img"
           
    def to_hist(self):
        global pass_screen
        screen_manager.transition.direction = "left"
        pass_screen = screen_manager.current
        screen_manager.current = "hist"
        
    def to_sign(self):
        screen_manager.transition.direction = "left"
        screen_manager.current = "signin"
    
    def clear(self, screen):
        screen_manager.get_screen(screen).chat_list.clear_widgets()
            
    def to_login(self):
        screen_manager.transition.direction = "right"
        MainApp.current_id = ""
        screen_manager.current = "login"
        
    def to_main(self):
        if screen_manager.current == "login":
            screen_manager.transition.direction = "left"
        elif screen_manager.current == "img":
            screen_manager.transition.direction = "down"
        else:
            screen_manager.transition.direction = "right"
        if screen_manager.current == "hist":
            screen_manager.current = pass_screen
        else:
            screen_manager.current = "main"
       
    
    def check_internet():
        try:
            page = urllib.request.urlopen("https://www.google.com/")
        except urllib.error.URLError:
            toast ("Connection lost !!! Please check your internet !")
            return False
        return True
           
    def get_his(query ,clt):        
            headers = {
                'apiKey': '<YOUR API KEY>',
                'Content-Type': 'application/json',
            }

            json_data = {
                "dataSource": "<YOUR DATASOUR>",
                "database": "<YOUR DATABASE>",
                "collection": clt,
                "filter": query,
                "sort": {"time": -1}  
            }
            
            params = json.dumps(json_data).encode('utf8')
            url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/<YOUR DATA KEY>/endpoint/data/v1/action/find"                   
            req = urllib.request.Request(url,  data=params, headers=headers)
            response = json.loads(urllib.request.urlopen(req).read().decode('utf8'))
            return response 
    
    def get_mongo(query ,clt):
        headers = {
            'apiKey': '<YOUR API KEY>',
            'Content-Type': 'application/json',
        }

        json_data = {
            "dataSource": "<YOUR DATASOUR>",
            "database": "<YOUR DATABASE>",
            "collection": clt,
            "filter": query  
        }
        
        params = json.dumps(json_data).encode('utf8')
        url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/<YOUR DATA KEY>/endpoint/data/v1/action/findOne"
                
        req = urllib.request.Request(url,  data=params, headers=headers)
        response = json.loads(urllib.request.urlopen(req).read().decode('utf8'))
        return response   
        
    def send_mongo(data, clt):
        headers = {
            'apiKey': '<YOUR API KEY>',
            'Content-Type': 'application/json',
        }

        json_data = {
            "dataSource": "<YOUR DATASOUR>",
            "database": "<YOUR DATABASE>",
            "collection": clt,
            "document": data   
        }
        
        params = json.dumps(json_data).encode('utf8')
        url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/<YOUR DATA KEY>/endpoint/data/v1/action/insertOne"               
        req = urllib.request.Request(url,  data=params, headers=headers)
        response = json.loads(urllib.request.urlopen(req).read().decode('utf8'))
        return response
    
    def signin(self, mail, passw, repassw):
        if MainApp.check_internet():
            myquery = {"mail": mail}
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if re.fullmatch(regex, mail):
                if len(passw) < 8:
                    toast("Password length must be greater than 8 !!!")
                else:
                    if repassw != passw:
                        toast("Different re-enter password !!!")
                    else:
                        if MainApp.get_mongo(myquery, "user")["document"] != None :
                            toast("This email is already registered !!!")
                        else:
                            user = {
                                "mail": mail,
                                "password": passw,
                            }
                            MainApp.send_mongo(user, "user")
                            toast("Sign Up Success !!!")
                            MainApp.to_login(self)
            else:
                toast("Invalid email !!!")
            
    def check_login(self, mail, passw):
        if MainApp.check_internet():
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if re.fullmatch(regex, mail):
                if len(passw) < 8:
                    toast("Password length must be greater than 8 !!!")
                else:
                    myquery = {"mail": mail}
                    get_mail = MainApp.get_mongo(myquery, "user")["document"]
                    if get_mail != None:
                        if passw == get_mail["password"]:
                            MainApp.current_id = get_mail["_id"]
                            MainApp.to_main(self)
                        else:    
                            toast("Incorrect Password !!!")
                    else:
                        toast("Unregistered email !!!")
            else:
                toast("Invalid email !!!")
            
    def message(self, text):
        toast(text)
        
    def as_res(screen ,text):
        global size, halign
        if len(text) in range(0,11):
            size =.22
            halign="center"
        elif len(text) in range(11,21):
            size =.32
            halign="center"
        elif len(text) in range(21,31):
            size =.45
            halign="center"
        elif len(text) in range(31,41):
            size =.58
            halign="center"
        elif len(text) in range(41,51):
            size =.71
            halign="center"
        else:
            size = .9
            halign="justify" 
        screen_manager.get_screen(screen).chat_list.add_widget(Response(text=text, size_hint_x=size, halign=halign))
                      
    def as_res_img(screen, text):
        screen_manager.get_screen(screen).chat_list.add_widget(MyImage(source=text))
         
    def us_ques(screen, text):
        if len(text) in range(0,11):
            size =.22
            halign="center"
        elif len(text) in range(11,21):
            size =.32
            halign="center"
        elif len(text) in range(21,31):
            size =.45
            halign="center"
        elif len(text) in range(31,41):
            size =.58
            halign="center"
        elif len(text) in range(41,51):
            size =.71
            halign="center"
        else:
            size = .9
            halign="justify" 
        screen_manager.get_screen(screen).chat_list.add_widget(Command(text=text, size_hint_x=size, halign=halign))
        if screen == ("main"):
            screen_manager.get_screen(screen).scroll.scroll_y = 0.1
            
    def time_his(text):
        size = 1
        halign = "center"
        screen_manager.get_screen("hist").chat_list.add_widget(Time(text=text, size_hint_x=size, halign=halign))
            
    def load_his(self):
        if MainApp.check_internet():
            myquery = {"id": MainApp.current_id}
            data = MainApp.get_his(myquery, "history")["documents"]
            for doc in data:
                MainApp.time_his(doc["time"])
                MainApp.us_ques("hist", doc["question"])
                if doc["type"] == "text":
                    MainApp.as_res("hist", doc["response"])           
                else:
                    MainApp.as_res_img("hist", doc["response"])
        else:
            MainApp.to_main(self)
            
    def send_AI(params, headers):
        url = "https://api.pawan.krd/v1/chat/completions"              
        req = urllib.request.Request(url,  data=params, headers=headers)
        response = json.loads(urllib.request.urlopen(req).read().decode('utf8'))
        return response
    
    def send_IMG(params, headers):    
        url =  "https://api.pawan.krd/v1/images/generations"
        req = urllib.request.Request(url,  data=params, headers=headers)
        response = json.loads(urllib.request.urlopen(req).read().decode('utf8'))
        return response
    
    def img_bot(self, question):
        if MainApp.check_internet():   
            headers = {
            'Authorization': 'Bearer pk-<YOUR API KEY>',
            'Content-Type': 'application/json',
            }
            
            json_data = {
                "n": 1,
                "prompt":question,
                "size":"1024x1024"
            }
            MainApp.us_ques("img", question)
              
            params = json.dumps(json_data).encode('utf8')            
            response = MainApp.send_IMG(params, headers)
            print(response)          
            try:
                data = response["data"][0]["url"]
                if data == "":
                    MainApp.as_res("img", "I do not understand what you say! Can you be more specific again?")
                else:    
                    MainApp.as_res_img("img", data)
                
                    #push data to DB
                    now = strftime("%H:%M:%S   %d/%m/%Y", localtime())
                    history = {
                        "id": MainApp.current_id,
                        "type": "img",
                        "question": question,
                        "response": data,
                        "time": now,
                    }
                    MainApp.send_mongo(history, "history")
            except:
                MainApp.as_res("img", "I do not understand what you say! Can you be more specific again?")
    
    def chat_bot(self, question):
        if MainApp.check_internet():   
            headers = {
            'Authorization': 'Bearer pk-<YOUR API KEY>',
            'Content-Type': 'application/json',
            }
            
            json_data = {
                "model": "gpt-3.5-turbo",
                "max_tokens": 3800,
                "messages": [
                    {
                        "role": "user",
                        "content": question,
                    },
                ],
            }
            MainApp.us_ques("main", question)
              
            params = json.dumps(json_data).encode('utf8')            
            response = MainApp.send_AI(params, headers)
                       
            try:
                data = response["choices"][0]["message"]
                if data["content"] == "":
                    MainApp.as_res("main", "I do not understand what you say! Can you be more specific again?")
                else:    
                    MainApp.as_res("main", data["content"])
                
                    #push data to DB
                    now = strftime("%H:%M:%S   %d/%m/%Y", localtime())
                    history = {
                        "id": MainApp.current_id,
                        "type": "text",
                        "question": question,
                        "response": data["content"],
                        "time": now,
                    }
                    MainApp.send_mongo(history, "history")
            except:
                MainApp.as_res("main", "I do not understand what you say! Can you be more specific again?")
 
if __name__ == "__main__":
    MainApp().run()
