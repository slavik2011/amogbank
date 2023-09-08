# amogbank
Простая банковская система.

# Установка

```
git clone https://github.com/slavik2011/amogbank.git
cd amogbank
```

## Версия для Android (/and_bank)

Перейдите в папку Android версии:

```
cd and_bank
```

### Зависимости

#### Для KivyMD версии

```
pip install kivy>=2.2.0, kivymd>=1.1.1, requests
```

#### Для Kivy версии

```
pip install kivy>=2.2.0, requests
```

### Запуск

#### Для KivyMD версии
```
python main.py
```
#### Для Kivy Версии
```
python mainl.py
```

## Версия для ПК (/pc_bank)

Перейдите в папку ПК версии:

```
cd and_bank
```

### Зависимости

```
pip install tkinter, formation, requests, ctypes, threading
```
### Запуск
```
python app.py
```

## Сервер (/flask)

Перейдите в папку Flask сервера:

```
cd server
```
### Зависимости
```
pip install flask gevent multiprocessing
```

### Запуск

```
python main.py
```

#### ! Важно !

В flask сервере добавьте ваши amogbank_setup.exe и amogusbank_android.apk для работы скачивания

## Сайт (/site)

### Зависимости
Их нет.

### Запуск

Запустите файл ```index.html```
