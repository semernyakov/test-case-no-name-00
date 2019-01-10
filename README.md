# TEST CASE / FOR PERX

Разработал: Иван Семерняков <direct@beatum-group.ru>

## Архитектура

* Ubuntu 14.04 LTS
* Python 3.6.3
* SQLite3
* Django 2.1.5
* Bootstrap 4.0.0-alpha.6 from CDN
* Jquery-3.1.1.slim.min.js jQuery 3.2.1 from CDN
* Tether.min.js 1.4.0 from CDN

## Инструкция

#### Клонируем проект:
```
$ mkdir test_project && cd $_
$ git clone https://github.com/beatum/perxtestcase.git
```

#### Инициализируем виртуальное окружение ```virtualenv```:
```
$ virtualenv -p python3.6 {path}
$ virtualenv -p /usr/bin/python3.6 {path}
$ python3.6 -m venv /path/to/new/virtual/environment
```

#### Активируем виртуальное окружение ```virtualenv```:
```
$ source {virtualenv_path}/bin/activate
```

#### Ставим зависимости:
```
$ cd project
$ pip install -r requirements.txt
```


#### Применяем миграции:
```
$ ./manage.py migrate
```

#### Создаём суперпользователя:
```
$ ./manage.py createsuperuser --username=admin --email=admin@admin.ru
```

#### Создаём приоритетную запись:
```
$ ./manage.py  setcounter - это нужно сделать в первую очередь (создаём запись счётчика со значением 500 ед.)
```


#### Создаём случайных 10 записей
```
$ ./manage.py createkeycode
```

#### Запускаем локальный сервер
```
$ ./manage.py runserver
```

Наслаждаемся работой сервиса по адресу localhost:8000

### Вот и всё! Удачи!

## License

This software is released under the [MIT License](http://opensource.org/licenses/MIT).

