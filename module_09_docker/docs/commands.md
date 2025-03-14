# Список команд

* [<< Назад к Docker](../Docker.md)
* [<< Назад к Launch](Launch%20Docker.md)

Синтаксис:
```html
docker [OPTIONS] COMMAND [args...]
```

* Основные ОПЦИИ утилиты:
    ```html
    -D - включить режим отладки;
    -H - подключиться к серверу, запущенному на другом компьютере;
    -l - изменить уровень ведения логов, доступно: debug,info,warn,error,fatal;
    -v - показать версию;
    --help вывести справку по команде или утилите в целом;
    ```
<hr>

* Список всех команд:
  - **attach** - подключиться к запущенному контейнеру;
  - **build** - собрать образ из инструкций dockerfile;
  - **commit** - создать новый образ из изменений контейнера;
  - **cp** - копировать файлы между контейнером и файловой системой;
  - **create** - создать новый контейнер;
  - **diff** - проверить файловую систему контейнера;
  - **events** - посмотреть события от контейнера;
  - **exec** - выполнить команду в контейнере;
  - **export** - извлечь содержимое контейнера в архив;
  - **history** - посмотреть историю изменений образа;
  - **images** - список установленных образов;
  - **import** - создать контейнер из архива tar;
  - **info** - посмотреть информацию о системе;
  - **inspect** - посмотреть информацию о контейнере;
  - **kill** - остановить запущенный контейнер;
  - **load** - загрузить образ из архива;
  - **login** - авторизация в официальном репозитории Docker;
  - **logout** - выйти из репозитория Docker;
  - **logs** - посмотреть логи контейнера;
  - **pause** - приостановить все процессы контейнера;
  - **port** - подброс портов для контейнера;
  - **ps** - список запущенных контейнеров;
  - **pull** - скачать образ контейнера из репозитория;
  - **push** - отправить образ в репозиторий;
  - **restart** - перезапустить контейнер;
  - **rm** - удалить контейнер;
  - **run** - выполнить команду в контейнере;
  - **save** - сохранить образ в архив tar;
  - **search** - поиск образов в репозитории по заданному шаблону;
  - **start** - запустить контейнер;
  - **stats** - статистика использования ресурсов контейнером;
  - **stop** - остановить контейнер;
  - **top** - посмотреть запущенные процессы в контейнере;
  - **unpause** - проложить выполнение процессов в контейнере.

<hr>

* Дополнительно: опции команды **run**
  - **-e** - переменные окружения для команды;
  - **-h** - имя хоста контейнера;
  - **-i** - интерактивный режим, связывающий stdin терминала с командой;
  - **-m** - ограничение памяти для команды;
  - **-u** - пользователь, от имени которого будет выполнена команда;
  - **-t** - связать tty с контейнером для работы ввода и вывода;
  - **-v** - примонтировать директорию основной системы в контейнер;
