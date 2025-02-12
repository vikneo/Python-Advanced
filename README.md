# Learning Python-Advanced

* Documentation to the [Flask](https://flask-russian-docs.readthedocs.io/ru/0.10.1/)
* [API-Flask Documentation (3.1.x)](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.before_request)
* Settings [environment](#settings-project)
* Studied [materials](#studied-materials)
* [Шпаргалки](#cheat-sheets)

<hr>

## Abstract

* Деплой проекта [module_08](./module_08_deploy/DEPLOY.md)
* ...
* Мультипоточность [module_11](./module_11_multitasking/Multitasking.md)
* ...
* MVC, язык шаблонов [module_14](./module_14_mvc/homework/README.md)
* Основы сетевого взаимодействия [module_15](./module_15_networking_basics/homework/README.md)
* База данных часть 3 [module_16](./module_16_db3/homework/README.md)
* REST API [module_17](./module_17_rest_api/homework/README.md)
* Документирование. Стандарты API [module_18](./module_18_documentation/homework/README.md)

## Settings project

* Setup environment for Linux
    ```html
    python3 -m venv name_venv
    ```
* Activated
    ```html
    source venv/bin/activate
    ```
____________________________________________________
* In the project, all dependencies are stored in a file ***poetry.toml***

* Setup ***Poetry***
```html
sudo apt install poetry
```

* Setup Flask
```html
poetry add flask
```

______________________________________________________
* Install all the dependencies
```html
poetry install
```

<hr>

## Cheat sheets

* Шпаргалка
  Setup package ***netstat***
  ```html
    # сканер сети
    sudo apt install net-tools
  
    # просмотр открытых портов
    sudo netstat -ntulp
  ```
  
* Шпаргалка по [иерархии исключений](docs/TREE_EXCEPTION.md) в Python
    * Функция [tree_exception.py](docs/tree_exception.py) для просмотра дерева исключений Python

* Команда **grep** в [Linux](https://www.geeksforgeeks.org/grep-command-in-unixlinux/)
<hr>