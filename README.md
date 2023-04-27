# Virtual-Assistant-for-Android
Run main files:
```bash
#create app folder
mkdir app
cd app

#clone github repository
git clone https://github.com/SunOn9/Virtual-Assistant-for-Android.git

#install and create virtual enviroment
python -m pip install --upgrade pip setuptools virtualenv
python -m virtualenv kivy_venv
kivy_venv\Scripts\activate

cd Virtual-Assistant-for-Android

pip install kivy==2.1.0
pip install kivymd
python main.py

```
