from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import requests


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10, padding=40)

        self.username = TextInput(
            hint_text="Логин",
            multiline=False,
            font_size=20,
            size_hint_y=None,
            height=50,
        )
        self.password = TextInput(
            hint_text="Пароль",
            password=True,
            multiline=False,
            font_size=20,
            size_hint_y=None,
            height=50,
        )
        blayout = BoxLayout(orientation="horizontal", spacing=10, padding=40,)
        self.login_button = Button(
            text="Вход",
            on_release=self.check_login,
            size_hint=(0.5, None),
            font_size=20,
            background_normal='',
            background_color=(0, 0.7, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        self.reg_button = Button(
            text="Регистрация",
            on_release=self.register,
            size_hint=(0.5, None),
            font_size=20,
            background_normal='',
            background_color=(0, 0.7, 0.5, 1),
            color=(1, 1, 1, 1),
        )

        layout.add_widget(self.username)
        layout.add_widget(self.password)
        blayout.add_widget(self.login_button)
        blayout.add_widget(self.reg_button)
        layout.add_widget(blayout)

        self.add_widget(layout)

    def check_login(self, instance):
        username = self.username.text
        password = self.password.text

        if requests.get(f'https://amogbank.hey555444.repl.co/l/{username}/{password}').text == 'True':
            app = App.get_running_app()
            app.username = username
            app.password = password
            self.manager.current = "second_screen"
        else:
            self.username.text = ""
            self.password.text = ""

    def register(self, instance):
        username = self.username.text
        password = self.password.text

        if requests.get(f'https://amogbank.hey555444.repl.co/reg/{username}/{password}').text == 'True':
            app = App.get_running_app()
            app.username = username
            app.password = password
            self.manager.current = "second_screen"
        else:
            self.username.text = "Произошла ошибка"
            self.password.text = ""


class SecondScreen(Screen):
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.app = app
        self.username_label.text = app.username
        self.balance_label.text = 'Баланс: ' + requests.get(
            f'https://amogbank.hey555444.repl.co/gb/{app.username}').text + ' амогусов'

    def chk_bal(self, i):
        self.balance_label.text = 'Баланс: ' + requests.get(
            f'https://amogbank.hey555444.repl.co/gb/{self.app.username}').text + ' амогусов'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=40)

        self.username_label = Label(
            text="",
            font_size=30,
            size_hint_y=None,
            height=50,
            color=(0.5, 0.5, 0.5, 1),  # Серый цвет текста
        )

        self.balance_label = Label(
            text="Баланс: 999",
            font_size=14,
            size_hint_y=None,
            height=50,
            color=(0.5, 0.5, 0.5, 1),  # Серый цвет текста
        )

        layout.add_widget(self.username_label)
        layout.add_widget(self.balance_label)

        update_info = BoxLayout(orientation="vertical", padding=15)
        crd = Label(
            text=requests.get('https://amogbank.hey555444.repl.co/getup').text,
            color=(0.5, 0.5, 0.5, 1),  # Серый цвет текста
        )
        update_info.add_widget(crd)
        layout.add_widget(update_info)

        button_layout = BoxLayout(orientation="horizontal", spacing=10, padding=10, size_hint_y=None)

        button3 = Button(
            text="Задание\nдня",
            on_release=self.task_of_day,
            font_size=16,
            background_normal='',
            background_color=(0, 0.7, 0.5, 1),
            color=(1, 1, 1, 1),
        )

        button2 = Button(
            text="Топ мистуров\nбистов",
            on_release=self.render_top,
            font_size=16,
            background_normal='',
            background_color=(0, 0.7, 0.5, 1),
            color=(1, 1, 1, 1),
        )

        button_layout.add_widget(button3)
        button_layout.add_widget(button2)

        button = Button(
            text="Переслать",
            on_release=self.send_data,
            font_size=20,
            size_hint=(1, None),
            height=60,
            background_normal='',
            background_color=(0, 0.7, 0.5, 1),
            color=(1, 1, 1, 1),
        )

        layout.add_widget(button_layout)
        layout.add_widget(button)

        self.add_widget(layout)

    def render_top(self, e):
        content = Label(
            text=requests.get('https://amogbank.hey555444.repl.co/getmb').text,
            color=(0, 0, 0, 1),  # Черный цвет текста
        )
        popup = Popup(
            title="Топ мистуров бистов",
            content=content,
            size_hint=(None, None),
            size=(400, 350),
        )
        popup.open()

    def transfer(self, e):
        f = requests.get(
            f'https://amogbank.hey555444.repl.co/pb/{self.app.username}/{self.app.password}/{self.g.text}/{self.f.text}').text
        if f == 'True':
            self.dialog.dismiss()
            self.chk_bal(None)

    def answer(self, e):
        f = requests.get(
            f'https://amogbank.hey555444.repl.co/answer/{self.app.username}/{self.ans.text}').text
        if f == 'True':
            self.dialog.dismiss()
            self.chk_bal(None)

    def task_of_day(self, instance):
        pon = BoxLayout(orientation='vertical', spacing=12, height=120, size_hint_y=None)

        l = Label(text=f"Стоимость вопроса: {requests.get(f'https://amogbank.hey555444.repl.co/getamount').text} амогусов")

        self.ans = TextInput(hint_text='Ответ на вопрос')

        pon.add_widget(l)
        pon.add_widget(self.ans)

        self.dialog = Popup(
            title=requests.get(f'https://amogbank.hey555444.repl.co/gettask').text,
            content=pon,
            size_hint=(None, None),
            size=(400, 250),
        )

        button = Button(
            text="Ответить",
            on_release=self.answer,
            font_size=20,
            background_normal='',
            background_color=(0, 0.7, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        pon.add_widget(button)

        self.dialog.open()

    def send_data(self, instance):
        self.pon = BoxLayout(orientation='vertical', spacing=12, height=120, size_hint_y=None)

        self.f = TextInput(hint_text='Получатель')
        self.g = TextInput(hint_text='Количество амогусов')

        self.pon.add_widget(self.f)
        self.pon.add_widget(self.g)

        self.dialog = Popup(
            title="Переслать",
            content=self.pon,
            size_hint=(None, None),
            size=(400, 250),
        )
        button = Button(
            text="Переслать!",
            on_release=self.transfer,
            font_size=20,
            background_normal='',
            background_color=(0, 0.7, 0.5, 1),
            color=(1, 1, 1, 1),
        )
        self.pon.add_widget(button)

        self.dialog.open()

class LoginApp(App):
    username = ""
    password = ""

    def build(self):
        self.screen_manager = ScreenManager()

        self.login_screen = LoginScreen(name="login_screen")
        self.second_screen = SecondScreen(name="second_screen")

        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.second_screen)

        return self.screen_manager

if __name__ == "__main__":
    LoginApp().run()
