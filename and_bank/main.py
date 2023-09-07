from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard


# additional imports

import requests


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = MDTextField(
            hint_text="Логин",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        self.password = MDTextField(
            hint_text="Пароль",
            password=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.login_button = MDRaisedButton(
            text="Вход",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.check_login,
        )
        self.reg_button = MDRaisedButton(
            text="Регистрация",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            on_release=self.register,
        )
        self.add_widget(self.username)
        self.add_widget(self.password)
        self.add_widget(self.login_button)
        self.add_widget(self.reg_button)

    def check_login(self, instance):
        username = self.username.text
        password = self.password.text

        # Здесь вы можете добавить код для проверки имени пользователя и пароля
        # Например, вы можете сравнивать их с предварительно сохраненными данными
        if requests.get(f'https://amogbank.hey555444.repl.co/l/{username}/{password}').text == 'True':
            app = MDApp.get_running_app()
            app.username = username
            app.password = password # Устанавливаем никнейм в приложении
            self.manager.current = "second_screen"  # Перейти на второй экран
        else:
            self.username.text = ""
            self.password.text = ""
    def register(self, instance):
        username = self.username.text
        password = self.password.text

        # Здесь вы можете добавить код для проверки имени пользователя и пароля
        # Например, вы можете сравнивать их с предварительно сохраненными данными
        if requests.get(f'https://amogbank.hey555444.repl.co/reg/{username}/{password}').text == 'True':
            app = MDApp.get_running_app()
            app.username = username
            app.password = password # Устанавливаем никнейм в приложении
            self.manager.current = "second_screen"  # Перейти на второй экран
        else:
            self.username.text = "Произошла ошибка"
            self.password.text = ""

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username_label = MDLabel(
            text="",  # Отображаем никнейм из приложения
            pos_hint={"x": 0, "y": 1},
            font_style="H4",
        )

        self.balance_label = MDLabel(
            text="Баланс: 999",
            font_size=14,
            pos_hint={"x": 0, "y": 1},
            font_style="H5",
        )

    def chk_bal(self, e):
        self.balance_label.text = 'Баланс: ' + requests.get(f'https://amogbank.hey555444.repl.co/gb/{self.app.username}').text + ' амогусов'

    def on_pre_enter(self, *args):
        self.app = MDApp.get_running_app()
        self.username_label.text = self.app.username  # Отображаем никнейм из приложения
        self.balance_label.text = 'Баланс: ' + requests.get(f'https://amogbank.hey555444.repl.co/gb/{self.app.username}').text + ' амогусов'  # Отображаем никнейм из приложения

        layout = BoxLayout(orientation="vertical", spacing=5)

        user_info = BoxLayout(orientation="vertical", padding=15)
        user_info.add_widget(self.username_label)
        user_info.add_widget(self.balance_label)

        update_info = BoxLayout(orientation="vertical", padding=15)
        crd = MDLabel(
            text=requests.get('https://amogbank.hey555444.repl.co/getup').text,
            color="grey",
            pos=("12dp", "12dp"),
        )
        update_info.add_widget(crd)

        button_layout = BoxLayout(orientation="horizontal", spacing=5, padding=5)

        button2 = MDRaisedButton(
            text="Топ мистуров\nбистов",
            on_release=self.render_top,
            size_hint=(0.5, None),  # Занимать половину ширины экрана
            height=250  # Высота кнопки
        )
        button3 = MDRaisedButton(
            text="Задание\nдня",
            on_release=self.task_of_day,
            size_hint=(0.5, None),  # Занимать половину ширины экрана
            height=250  # Высота кнопки
        )

        button_layout.add_widget(button2)
        button_layout.add_widget(button3)

        button = MDRaisedButton(
            text="Переслать",
            on_release=self.send_data,
            size_hint=(1, None),
            height=250  # Высота кнопки
        )

        layout.add_widget(user_info)
        layout.add_widget(update_info)
        layout.add_widget(button_layout)
        layout.add_widget(button)
        self.add_widget(layout)

    def render_top(self, e):
        self.dialog = MDDialog(
            title="Топ мистуров бистов",
            text=requests.get('https://amogbank.hey555444.repl.co/getmb').text,
            buttons=[
                MDFlatButton(
                    text="Закрыть",
                    on_release= lambda e: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def transfer(self, e):
        f = requests.get(f'https://amogbank.hey555444.repl.co/pb/{self.app.username}/{self.app.password}/{self.g.text}/{self.f.text}').text
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

        l = MDLabel(text=f"Стоимость вопроса: {requests.get(f'https://amogbank.hey555444.repl.co/getamount').text} амогусов")

        self.ans = MDTextField(hint_text='Ответ на вопрос')

        pon.add_widget(l)
        pon.add_widget(self.ans)

        self.dialog = MDDialog(
                title=requests.get(f'https://amogbank.hey555444.repl.co/gettask').text,
                type="custom",
                content_cls=pon,
                buttons=[
                    MDFlatButton(
                        text="Ответить",
                        on_release=self.answer
                    ),
                ],
            )
        self.dialog.open()

    def send_data(self, instance):
        self.pon = BoxLayout(orientation='vertical', spacing=12, height=120, size_hint_y=None)

        self.f = MDTextField(hint_text='Получатель')
        self.g = MDTextField(hint_text='Количество амогусов')

        self.pon.add_widget(self.f)
        self.pon.add_widget(self.g)

        self.dialog = MDDialog(
                title="Переслать",
                type="custom",
                content_cls=self.pon,
                buttons=[
                    MDFlatButton(
                        text="Переслать!",
                        on_release=self.transfer
                    ),
                ],
            )
        self.dialog.open()


class LoginApp(MDApp):
    username = ""

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "A700"

        self.screen_manager = ScreenManager()

        self.login_screen = LoginScreen(name="login_screen")
        self.second_screen = SecondScreen(name="second_screen")

        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.second_screen)

        return self.screen_manager

if __name__ == "__main__":
    LoginApp().run()
