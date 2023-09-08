import flask
from flask import Flask, request
from flask import render_template, redirect
import os
import ast
from gevent.pywsgi import WSGIServer
import time
import datetime
from multiprocessing import Process

latest_v = '8'

all_cmds = '`/getup` - получить последнее сообщение от автора\n\n`/getlv` - нужна для компов: вам не понадобится\n\n`/delacc/вашник/пароль` - удаление аккаунта\n\n`/edp/вашник/вашпароль/вашновыйпароль` - поменять пароль\n\n`/gb/вашник` - узнать баланс\n\n`/pb/вашник/пароль/количествоамогусов/никцели` - переслать амогусы\n\n`/minus/вашник/пароль/никцели/количествоамогусов` - выдать штраф (для админов)\n\n`/plus/вашник/пароль/никцели/количествоамогусов` - выдать зарплату (для админов)\n\n`/isadmin/вашник` - узнать, админ ли этот человек\n\n`/l/вашник/вашпароль` - узнать, есть ли такой аккаунт\n\n`/reg/вашник/вашпароль` - зарегистрироваться в системе\n\n`/getmb` - узнать топ мистуров бистов\n\n`/answer/вашник/ответ` - ответить на вопрос дня\n\n`/gettask` - получить задание дня\n\n/buy/admin/логин/пароль - купить админку (15К амогусов)'

class task:
  with open('task.tx', 'r') as f:
    db = ast.literal_eval(f.read())
  task = db['task']
  answer = db['answer']
  amount = db['amount']
  def reg():
    with open('task.tx', 'r') as f:
      e = ast.literal_eval(f.read())
    task.task = e['task']
    task.answer = e['answer']
    task.amount = e['amount']
  def reset():
    with open('task.tx', 'r') as f:
      e = ast.literal_eval(f.read())
    e['task'] = 'Ответ уже получен!'
    e['answer'] = '253OHQ5NCMECIP[ROkl338t90834ytkq39xryn9y'
    e['amount'] = 0
    os.remove('task.tx')
    with open('task.tx', 'w') as f:
      f.write(str(e))
    task.task = e['task']
    task.answer = e['answer']
    task.amount = e['amount']

def f():
  while True:
    time.sleep(1)
    task.reg()

Process(target=f).start()

update_info = """Обновление v8

- Добавлены товары банка
- Исправлен баг BUG-23 с длиной никнейма
Ответ на вопрос дня: пупсик

"""

def get_accounts():
  with open('accounts.tx') as f:
    return ast.literal_eval(f.read()).keys()

def edit_password(login, newpass):
  with open('accounts.tx', 'r') as f:
    e = ast.literal_eval(f.read())
  e[login]['password'] = newpass
  os.remove('accounts.tx')
  with open('accounts.tx', 'w') as f:
    f.write(str(e))

def is_admin(user):
  with open('accounts.tx') as f:
    f = ast.literal_eval(f.read())
    return f[user]['admin'] == True

def check_password(user, passw):
  with open('accounts.tx') as f:
    f = ast.literal_eval(f.read())
    return f[user]['password'] == passw

def set_admin(login, adm):
  with open('accounts.tx', 'r') as f:
    e = ast.literal_eval(f.read())
  e[login]['admin'] = adm
  os.remove('accounts.tx')
  with open('accounts.tx', 'w') as f:
    f.write(str(e))

def set_bal(login, a):
  with open('accounts.tx', 'r') as f:
    e = ast.literal_eval(f.read())
  e[login]['balance'] = a
  os.remove('accounts.tx')
  with open('accounts.tx', 'w') as f:
    f.write(str(e))

def check_for_ip(ip):
  with open('accounts.tx') as f:
    f = ast.literal_eval(f.read())
    for i in f.values():
      print(i)
      print(ip, type(ip))
      print(str(i['ip']), type(str(i['ip'])))
      if i['ip'] == ip:
        return True
    return False

def task_is(answer):
  if answer == task.answer:
    return True
  else:
    return False
    
def get_all_balances():
  with open('accounts.tx') as f:
    f = ast.literal_eval(f.read())
    ret = {}
    for r in f:
      ret.update({r: f[r]['balance']})
    return ret

def get_bal(login):
  with open('accounts.tx') as f:
    f = ast.literal_eval(f.read())
    return str(f[login]['balance'])

def del_acc(login):
  with open('accounts.tx', 'r') as f:
    e = ast.literal_eval(f.read())
  e.pop(login)
  os.remove('accounts.tx')
  with open('accounts.tx', 'w') as f:
    f.write(str(e))

def get_all_accounts():
  with open('accounts.tx', 'r') as f:
    e = ast.literal_eval(f.read())
    return e.keys()

def register_acc(login, passw, isadmin, ip):
  with open('accounts.tx', 'r') as f:
    e = ast.literal_eval(f.read())
  if login in get_accounts():
    return False
  e.update({login: {'password': passw, 'balance': 0, 'admin': isadmin, 'ip': ip}})
  os.remove('accounts.tx')
  with open('accounts.tx', 'w') as f:
    f.write(str(e))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

app = Flask(__name__)

#log = logging.getLogger('werkzeug')
#log.disabled = True

debug = True

@app.route('/allcmds')
def allcmds():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение всех команд: вывод {all_cmds}{bcolors.ENDC}')
  return all_cmds

@app.route('/getlv')
def getlv():
  #print(f'{bcolors.OKGREEN}{time.time()} > Получение последней версии: вывод {latest_v}{bcolors.ENDC}')
  return latest_v

@app.route('/answer/<string:login>/<string:answer>')
def checkansw(login, answer):
  if login not in get_accounts():
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение задания: вывод False{bcolors.ENDC}')
    return 'False'
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Правилен ли ответ {answer}?: вывод {str(task_is(answer))}{bcolors.ENDC}')
  if task_is(answer):
    set_bal(login, int(get_bal(login))+task.amount)
    f = str(task_is(answer))
    task.reset()
  else:
    f = str(task_is(answer))
  return f

@app.route('/getsells')
def getsells():
  global sells
  # sell template: [name, urltemp, closewindow?, isadminsell, isselling]
  sells = [['Админка в банке - 15К амогусов', 'https://amogbank.hey555444.repl.co/buy/admin', 'True', 'True', 'True'], ['Нет товара - 0 амогусов', 'https://amogbank.hey555444.repl.co/buy/', 'False', 'False', 'False'], ['Нет товара - 0 амогусов', 'https://amogbank.hey555444.repl.co/buy/', 'False', 'False', 'False']]
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение магазина: вывод {sells}{bcolors.ENDC}')
  return sells

@app.route('/buy/admin/<string:login>/<string:password>')
def buy(login, password):
  if login in get_accounts():
    if check_password(login, password):
      if int(get_bal(login)) >= 15000:
        set_bal(login, int(get_bal(login))-15000)
        set_admin(login, True)
        print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > ПОКУПКА АДМИНКИ АККАУНТОМ {login}: вывод True{bcolors.ENDC}')
        return 'True'
      else:
        print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > ПОКУПКА АДМИНКИ АККАУНТОМ {login}: вывод False{bcolors.ENDC}')
        return 'False'
    else:
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > ПОКУПКА АДМИНКИ АККАУНТОМ {login}: вывод False{bcolors.ENDC}')
      return 'False'
  else:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > ПОКУПКА АДМИНКИ АККАУНТОМ {login}: вывод False{bcolors.ENDC}')
    return 'False'
  

@app.route('/getamount')
def getamount():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение цены задания: вывод {task.amount}{bcolors.ENDC}')
  return str(task.amount)

@app.route('/gettask')
def gettask():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение задания: вывод {task.task}{bcolors.ENDC}')
  return task.task

@app.route('/getup')
def getup():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение новости дня: вывод {update_info}{bcolors.ENDC}')
  return update_info

@app.route('/delacc/<string:login>/<string:passw>')
def delacc(login, passw):
  if int(get_bal(login)) < 0:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Удаление аккаунта {login}: вывод False {bcolors.ENDC}')
    return 'False'
  if login in get_accounts():
    if check_password(login, passw):
      del_acc(login)
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Удаление аккаунта {login}: вывод True {bcolors.ENDC}')
      return 'True'
    else:
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Удаление аккаунта {login}: вывод False {bcolors.ENDC}')
      return 'False'
  else:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Удаление аккаунта {login}: вывод False {bcolors.ENDC}')
    return 'False'

@app.route('/edp/<string:login>/<string:passw>/<string:newpass>')
def edp(login, passw, newpass):
  if login in get_accounts():
    if check_password(login, passw):
      edit_password(login, newpass)
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Изменение пароля аккаунта {login}: вывод True {bcolors.ENDC}')
      return 'True'
    else:
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Изменение пароля аккаунта {login}: вывод True {bcolors.ENDC}')
      return 'False'
  else:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Изменение пароля аккаунта {login}: вывод True {bcolors.ENDC}')
    return 'True'

@app.route('/gb/<string:login>')
def gb(login):
  if login not in get_accounts():
    return 'False'
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение баланса аккаунта {login}: вывод {get_bal(login)} {bcolors.ENDC}')
  return get_bal(login)

@app.route('/code')
def code():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение исходного кода {bcolors.ENDC}')
  return render_template('code.html')


@app.route('/')
def main():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение главной страницы {bcolors.ENDC}')
  return redirect('https://pon.hey555444.repl.co/index.html')
  #return render_template('index.html')

@app.route('/getmb')
def getmb():
  text = """"""
  n = 0
  dict1 = get_all_balances()
  sorted_tuples = sorted(dict1.items(), key=lambda item: item[1])
  sorted_dict = {k: v for k, v in sorted_tuples}
  ready = dict(reversed(list(sorted_dict.items())))
  for user in ready:
    if not user.startswith('promo_'):
      n += 1
      if n > 5:
        break
      text = text + f'{n} место: {user}: {ready[user]} амогусов.\n\n'
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение топа: вывод {text} {bcolors.ENDC}')
  return text

@app.route('/docs')
def docs():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение документации {bcolors.ENDC}')
  return render_template('amogusdocs.html')

@app.route('/download/code/main')
def dnwmp():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение исходного Кода Банка Амогусов{bcolors.ENDC}')
  return flask.send_file('downloads/main.py', download_name='main.py')
  return 'Начало скачивания...'

@app.route('/downloadp')
def dnwp():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение Банка Амогусов на Android{bcolors.ENDC}')
  return flask.send_file('downloads/amogusbank_android.apk', download_name='amogusbank_android.apk')
  return 'Начало скачивания...'

@app.route('/download')
def dnw():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение Банка Амогусов на ПК{bcolors.ENDC}')
  return flask.send_file('downloads/amogbank_setup.exe', download_name='amogusbank.exe')
  return 'Начало скачивания...'

@app.route('/pb/<string:login>/<string:passw>/<string:amount>/<string:to>')
def pb(login, passw, amount, to):
  if not amount.isdigit():
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Пересылка {amount} амогусов от {login} до {to}: вывод False 4 {bcolors.ENDC}')
    return 'False'
  if to in get_accounts():
    pass
  else:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Пересылка {amount} амогусов от {login} до {to}: вывод False 3 {bcolors.ENDC}')
    return 'False'
  if int(amount) > int(get_bal(login)):
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Пересылка {amount} амогусов от {login} до {to}: вывод False 2 {bcolors.ENDC}')
    return 'False'
  if int(amount) > 0:
    pass
  else:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Пересылка {amount} амогусов от {login} до {to}: вывод False 1 {bcolors.ENDC}')
    return 'False'
  if login in get_accounts():
    if check_password(login, passw):
      if debug == False:
        try:
          set_bal(login, int(get_bal(login))-int(amount))
          set_bal(to, int(get_bal(to))+int(to))
          print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Пересылка {amount} амогусов от {login} до {to}: вывод True {bcolors.ENDC}')
          return 'True'
        except Exception as e:
          print(e)
          print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Пересылка {amount} амогусов от {login} до {to}: вывод False 5 {bcolors.ENDC}')
          return 'False'
      else:
        set_bal(login, int(get_bal(login))-int(amount))
        set_bal(to, int(get_bal(to))+int(amount))
        print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Пересылка {amount} амогусов от {login} до {to}: вывод True {bcolors.ENDC}')
        return 'True'
    else:
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Пересылка {amount} амогусов от {login} до {to}: вывод False 6 {bcolors.ENDC}')
      return 'False'
  else:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Пересылка {amount} амогусов от {login} до {to}: вывод False 7 {bcolors.ENDC}')
    return 'False'
      
@app.route('/minus/<string:login>/<string:passw>/<string:tlogin>/<string:amount>')
def minus(login, passw, tlogin, amount):
  if int(amount) < 1:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Штраф на {amount} амогусов от {login} нарушителю {tlogin}: вывод False {bcolors.ENDC}')
    return 'False'
  if login in get_accounts():
    if check_password(login, passw):
      if is_admin(login):
        set_bal(tlogin, int(get_bal(tlogin))-int(amount))
        print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Штраф на {amount} амогусов от {login} нарушителю {tlogin}: вывод True {bcolors.ENDC}')
        return 'True'
      else: 
        print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Штраф на {amount} амогусов от {login} нарушителю {tlogin}: вывод False {bcolors.ENDC}')
        return 'False'
    else:
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Штраф на {amount} амогусов от {login} нарушителю {tlogin}: вывод False {bcolors.ENDC}')
      return 'False'
  else: 
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Штраф на {amount} амогусов от {login} нарушителю {tlogin}: вывод False {bcolors.ENDC}')
    return 'False'

@app.route('/plus/<string:login>/<string:passw>/<string:tlogin>/<string:amount>')
def plus(login, passw, tlogin, amount):
  if int(amount) < 1:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Зарплата размером {amount} амогусов от {login} для {tlogin}: вывод False {bcolors.ENDC}')
    return 'False'
  if login in get_accounts():
    if check_password(login, passw):
      if is_admin(login):
        set_bal(tlogin, int(get_bal(tlogin))+int(amount))
        print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Зарплата размером {amount} амогусов от {login} для {tlogin}: вывод True {bcolors.ENDC}')
        return 'True'
      else: 
        print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Зарплата размером {amount} амогусов от {login} для {tlogin}: вывод False {bcolors.ENDC}')
        return 'False'
    else: 
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Зарплата размером {amount} амогусов от {login} для {tlogin}: вывод False {bcolors.ENDC}')
      return 'False'
  else: 
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Зарплата размером {amount} амогусов от {login} для {tlogin}: вывод False {bcolors.ENDC}')
    return 'False'

@app.route('/download/page')
def dpage():
  print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Получение страницы загрузок {bcolors.ENDC}')
  return render_template('download.html')

@app.route('/isadmin/<string:login>')
def isadminn(login):
  if login in get_accounts():
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Админ ли аккаунт {login}?: вывод {str(is_admin(login))} {bcolors.ENDC}')
    return str(is_admin(login))
  else:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Админ ли аккаунт {login}?: вывод False {bcolors.ENDC}')
    return 'False'

@app.route('/l/<string:login>/<string:passw>')
def l(login, passw):
  if login in get_accounts():
    if check_password(login, passw):
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Сущеcтвует ли аккаунт {login}?: вывод True {bcolors.ENDC}')
      return 'True'
    else:
      return 'False'
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Сущеcтвует ли аккаунт {login}?: вывод False {bcolors.ENDC}')
  else:
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Сущеcтвует ли аккаунт {login}?: вывод False {bcolors.ENDC}')
    return 'False'

@app.route('/reg/<string:login>/<string:passw>')
def reg(login, passw):
  #if check_for_ip(request.remote_addr):
  #  return 'False'
  if debug == False:
    try:
      register_acc(login, passw, False, request.remote_addr)
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Регистрация аккаунта {login}: вывод True {bcolors.ENDC}')
      return 'True'
    except:
      print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Регистрация аккаунта {login}: вывод False {bcolors.ENDC}')
      return 'False'
  else:
    register_acc(login, passw, False, request.remote_addr)
    print(f'{bcolors.OKGREEN}{datetime.datetime.now()} > Регистрация аккаунта {login}: вывод True {bcolors.ENDC}')
    return 'True'
  
production = False

if production:
  http_server = WSGIServer(('0.0.0.0', 8080), app)
  http_server.serve_forever()
else:
  app.run('0.0.0.0', 8080)
