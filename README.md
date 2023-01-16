# Домашнее задание к лекции «Flask»

## Задание 1

* Реализовано  REST API (backend) для сайта объявлений на Flask. 
* Реализованы методы создания/удаления/редактирования объявления.

## Задание 2

* Добавлена система прав доступа

### Установка

``` bash
pip install -r requirements.txt
```

### Инициализация базы данных

``` bash
flask db init
```

### Миграции

``` bash
flask db migrate -m "migration-1"
flask db upgrade
```

Примеры http-запросов в файле [requests-examples.http](/requests-examples.http)