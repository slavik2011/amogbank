import ast
import tkinter
import requests
from formation import AppBuilder
import ctypes
import os
import sys
import webbrowser
import time
import threading
import traceback

version = '8'

t = tkinter.Tk()

def chk_updates():
    if requests.get(f'''https://amogbank.hey555444.repl.co/getlv''').text != version:
        ctypes.windll.user32.MessageBoxW(0, f"""Вышло обновление! Обновитесь, и пользуйтесь банком дальше.""", 'Обновление!', 0)
        webbrowser.open_new_tab('https://amogbank.hey555444.repl.co/')
        sys.exit()

chk_updates()

def taskofdaye():
    f = requests.get(f'''https://amogbank.hey555444.repl.co/answer/{tt}/{tod.answer.get()}''').text
    if f == 'True':
        tod._app.destroy()
        chk_bal()

def buy1():
    f = requests.get(sells[0][1]+f'/{tt}/{ww}').text
    if f == 'True':
        shop._app.destroy()
        chk_bal()
        if sells[0][2] == 'True':
            restart()

def buy2():
    f = requests.get(sells[1][1]+f'/{tt}/{ww}').text
    if f == 'True':
        shop._app.destroy()
        chk_bal()
        if sells[1][2] == 'True':
            restart()

def buy3():
    f = requests.get(sells[2][1]+f'/{tt}/{ww}').text
    if f == 'True':
        shop._app.destroy()
        chk_bal()
        if sells[2][2] == 'True':
            restart()

def shop():
    global sells
    print('> Обнаружена проблема (shop.xml). Попытка изменить кодировку на ANSI')
    replace_first_line('templates/shop.xml', 'templates/shop.xml',
                       '''<?xml version='1.0' encoding='ANSI'?>''')
    globals()['shop'] = AppBuilder(path="templates/shop.xml")
    globals()['shop'].connect_callbacks(globals())
    print('> Окно shop.xml определено успешно.')
    sells = ast.literal_eval(requests.get(f'''https://amogbank.hey555444.repl.co/getsells''').text)
    globals()['shop'].sell1['text'] = sells[0][0]
    globals()['shop'].sell2['text'] = sells[1][0]
    globals()['shop'].sell3['text'] = sells[2][0]
    if sells[0][4] == 'False':
        globals()['shop'].sell1['state'] = 'disabled'
    if sells[1][4] == 'False':
        globals()['shop'].sell2['state'] = 'disabled'
    if sells[2][4] == 'False':
        globals()['shop'].sell3['state'] = 'disabled'
    if sells[0][3] == 'True':
        if requests.get(f'''https://amogbank.hey555444.repl.co/isadmin/{tt}''').text == 'True':
            globals()['shop'].sell1['state'] = 'disabled'
    if sells[1][3] == 'True':
        if requests.get(f'''https://amogbank.hey555444.repl.co/isadmin/{tt}''').text == 'True':
            globals()['shop'].sell2['state'] = 'disabled'
    if sells[2][3] == 'True':
        if requests.get(f'''https://amogbank.hey555444.repl.co/isadmin/{tt}''').text == 'True':
            globals()['shop'].sell3['state'] = 'disabled'

def taskofday():
    print('> Обнаружена проблема (tod.xml). Попытка изменить кодировку на ANSI')
    replace_first_line('templates/tod.xml', 'templates/tod.xml',
                       '''<?xml version='1.0' encoding='ANSI'?>''')
    globals()['tod'] = AppBuilder(path="templates/tod.xml")
    globals()['tod'].connect_callbacks(globals())
    print('> Окно tod.xml определено успешно.')
    globals()['tod'].title['text'] = requests.get(f'''https://amogbank.hey555444.repl.co/gettask''').text
    globals()['tod'].amount['text'] = f'''Цена: {requests.get(f'https://amogbank.hey555444.repl.co/getamount').text} амогусов.'''

def save_acc(login, passw):
  with open('config/config.tx', 'r', encoding='utf-8') as f:
    e = ast.literal_eval(f.read())
  e.update({'saved': {'name': login, 'passw': passw}})
  os.remove('config/config.tx')
  with open('config/config.tx', 'w', encoding='utf-8') as f:
    f.write(str(e))


def load_acc():
    try:
        with open('config/config.tx', 'r', encoding='utf-8') as f:
            e = ast.literal_eval(f.read())
            return e['saved']
    except Exception as e:
        print(e)
        return None

def mistwin():
    print('> Обнаружена проблема (topplayers.xml). Попытка изменить кодировку на ANSI')
    replace_first_line('templates/topplayers.xml', 'templates/topplayers.xml',
                       '''<?xml version='1.0' encoding='ANSI'?>''')
    globals()['topplayers'] = AppBuilder(path="templates/topplayers.xml")
    globals()['topplayers'].connect_callbacks(globals())
    print('> Окно topplayers.xml определено успешно.')
    globals()['topplayers'].text['text'] = requests.get(f'''https://amogbank.hey555444.repl.co/getmb''').text

def plusbalwin():
    print('> Обнаружена проблема (plusbal.xml). Попытка изменить кодировку на ANSI')
    replace_first_line('templates/plusbal.xml', 'templates/plusbal.xml',
                       '''<?xml version='1.0' encoding='ANSI'?>''')
    globals()['plusbalwin'] = AppBuilder(path="templates/plusbal.xml")
    globals()['plusbalwin'].connect_callbacks(globals())
    print('> Окно plusbal.xml определено успешно.')

def plusbal():
    rep = requests.get(
        f'''https://amogbank.hey555444.repl.co/plus/{tt}/{ww}/{globals()['plusbalwin'].l.get()}/{globals()['plusbalwin'].amo.get()}''').text
    if rep == 'True':
        globals()['plusbalwin']._app.destroy()
        chk_bal()

def minusbalwin():
    print('> Обнаружена проблема (minusbal.xml). Попытка изменить кодировку на ANSI')
    replace_first_line('templates/minusbal.xml', 'templates/minusbal.xml',
                       '''<?xml version='1.0' encoding='ANSI'?>''')
    globals()['minbalwin'] = AppBuilder(path="templates/minusbal.xml")
    globals()['minbalwin'].connect_callbacks(globals())
    print('> Окно minusbal.xml определено успешно.')

def minusbal():
    rep = requests.get(
        f'''https://amogbank.hey555444.repl.co/minus/{tt}/{ww}/{globals()['minbalwin'].l.get()}/{globals()['minbalwin'].amo.get()}''').text
    if rep == 'True':
        globals()['minbalwin']._app.destroy()
        chk_bal()

def delaccyes():
    rep = requests.get(
        f'''https://amogbank.hey555444.repl.co/delacc/{globals()['tt']}/{ww}''').text
    if rep == 'True':
        globals()['minbalwin']._app.destroy()
        restart()

def delaccno():
    globals()['delaccw']._app.destroy()

def delacc():
    print('> Обнаружена проблема (delacc.xml). Попытка изменить кодировку на ANSI')
    replace_first_line('templates/delacc.xml', 'templates/delacc.xml',
                       '''<?xml version='1.0' encoding='ANSI'?>''')
    globals()['delaccw'] = AppBuilder(path="templates/delacc.xml")
    globals()['delaccw'].connect_callbacks(globals())
    print('> Окно delacc.xml определено успешно.')


def editpassacc():
    rep = requests.get(f'''https://amogbank.hey555444.repl.co/edp/{globals()['tt']}/{globals()['edpaswin'].oldpass.get()}/{globals()['edpaswin'].newpass.get()}''').text
    if rep == 'True':
        globals()['edpaswin']._app.destroy()
        restart()

def epwin():
    print('> Обнаружена проблема (editpass.xml). Попытка изменить кодировку на ANSI')
    replace_first_line('templates/editpass.xml', 'templates/editpass.xml',
                       '''<?xml version='1.0' encoding='ANSI'?>''')
    globals()['edpaswin'] = AppBuilder(path="templates/editpass.xml")
    globals()['edpaswin'].connect_callbacks(globals())
    print('> Окно editpass.xml определено успешно.')

def replace_first_line(src_filename, target_filename, replacement_line):
    f = open(src_filename)
    first_line, remainder = f.readline(), f.read()
    t = open(target_filename, "w")
    t.write(replacement_line + "\n")
    t.write(remainder)
    t.close()

def perec():
    а = globals()['pww'].money.get()
    ggg = requests.get(f'''https://amogbank.hey555444.repl.co/pb/{globals()['tt']}/{ww}/{а}/{globals()['pww'].nk.get()}''').text
    if ggg == 'True':
        globals()['pww']._app.destroy()
        chk_bal()

def chk_bal():
    globals()['bal'] = ast.literal_eval(requests.get(f'''https://amogbank.hey555444.repl.co/gb/{globals()['tt']}''').text)
    globals()['mp'].bl['text'] = globals()['bal']
    if bal < 0:
        mp.delacc['state'] = 'disabled'
    else:
        mp.delacc['state'] = 'normal'

def opere():
    print('> Обнаружена проблема (perc.xml). Попытка изменить кодировку на ANSI')
    replace_first_line('templates/perc.xml', 'templates/perc.xml',
                       '''<?xml version='1.0' encoding='ANSI'?>''')
    globals()['pww'] = AppBuilder(path="templates/perc.xml")
    globals()['pww'].connect_callbacks(globals())
    print('> Окно perc.xml определено успешно.')
    globals()['pww'].money['to'] = globals()['bal']
    if globals()['bal'] < 1:
        globals()['pww'].per['state'] = 'disabled'


def edxit():
    os.system('taskkill /F /IM app.exe')
    exit('df')
    lf._app.destroy()
    mp._app.destroy()


def l():
    global ww
    globals()['tt'] = globals()['lw'].l.get()
    ww = globals()['lw'].p.get()
    g = requests.get(f'''https://amogbank.hey555444.repl.co/l/{globals()['tt']}/{ww}''')
    if g.text == 'True':
        print('> Обнаружена проблема (mainpage.xml). Попытка изменить кодировку на ANSI')
        replace_first_line('templates/mainpage.xml', 'templates/mainpage.xml',
                           '''<?xml version='1.0' encoding='ANSI'?>''')
        globals()['mp'] = AppBuilder(path="templates/mainpage.xml")
        globals()['mp'].connect_callbacks(globals())
        print('> Окно mainpage.xml определено успешно.')
        save_acc(lw.l.get(), lw.p.get())
        globals()['lw']._app.destroy()
        globals()['mp'].nk['text'] = globals()['tt']
        globals()['bal'] = ast.literal_eval(requests.get(f'''https://amogbank.hey555444.repl.co/gb/{globals()['tt']}''').text)
        globals()['mp'].bl['text'] = globals()['bal']
        if requests.get(f'''https://amogbank.hey555444.repl.co/isadmin/{tt}''').text == 'False':
            mp.adminminus['state'] = 'disabled'
            mp.adminplus['state'] = 'disabled'
        if bal < 0:
            mp.delacc['state'] = 'disabled'
        mp.news['text'] = requests.get(f'''https://amogbank.hey555444.repl.co/getup''').text
        mp._app.protocol("WM_DELETE_WINDOW", edxit)



def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def reg():
    g = requests.get(f'''https://amogbank.hey555444.repl.co/reg/{globals()['lw'].l.get()}/{globals()['lw'].p.get()}''')
    if g.text == 'True':
        l()



print('> Обнаружена проблема (loginreg.xml). Попытка изменить кодировку на ANSI')
replace_first_line('templates/loginreg.xml', 'templates/loginreg.xml', '''<?xml version='1.0' encoding='ANSI'?>''')
globals()['lw'] = AppBuilder(path="templates/loginreg.xml")
globals()['lw'].connect_callbacks(globals())
print('> Окно loginreg.xml определено успешно.')
lw._app.protocol("WM_DELETE_WINDOW", edxit)
if load_acc() != None:
    acc = load_acc()
    lw.l.insert(tkinter.END, acc['name'])
    lw.p.insert(tkinter.END, acc['passw'])

def background_task():
    def stop():
        exit()
    while True:
        time.sleep(5)
        if requests.get(f'''https://amogbank.hey555444.repl.co/getlv''').text != version:
            webbrowser.open_new_tab('https://amogbank.hey555444.repl.co/download')
            edxit()


b = threading.Thread(target=background_task)
b.start()
t.destroy()
t.mainloop()
