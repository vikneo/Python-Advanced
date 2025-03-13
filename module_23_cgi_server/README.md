# CGI server (module 23)


<p style="font-style: italic; color: yellow">Вступление</p>

Если у вас не получается скачать (установить) плагин **nginx Configurate** для PyCharm<br>
Воспользуйтесь инструкцией по настройке [VPN for Linux (Ubuntu 22.0)](setup_vpn_linux.md)

<p style="font-size: 16px; color: #27ae60">
Документация
</p>

<div style='display: flex; align-items: center;'>
<a href="https://nginx.org/ru/docs/beginners_guide.html">
<img src='https://nginx.org/img/nginx_logo_dark.png' width="100px">
</a>
<span style='padding-left: 10px; font-size: 16px;'>Руководство для начинающих на русском</span>
</div>
<div style='display: flex; align-items: center;'>
<a href="https://nginx.org/ru/docs/beginners_guide.html">
<img src='https://nginx.org/img/nginx_logo_dark.png' width="100px">
</a>
<span style='padding-left: 10px; font-size: 16px;'>NGINX официальная документация</span>
</div>

<hr>

***NGINX** – это высокопроизводительный веб-сервер, потребляющий
очень мало системных ресурсов.*
<hr>

### Содержание

* [Установка](#установка-nginx-for-linux)
* [Иерархия](#иерархия-каталогов-nginx)
* [Управление](#остановка-перезагрузка-конфигурации)
* [Примеры](#пример-конфигурационного-файла)

## Установка **nginx** (for Linux)

* Чтобы установить nginx, откройте терминал и выполните следующие команды:

```html
sudo apt update
sudo apt install nginx
```
После установки сервер **nginx** запустится автоматически, что бы проверить, перейдите по адресу 127.0.0.1 и увидите приветствие

<img src="img/welcom_to_nginx.PNG" width="600px">

## Иерархия каталогов Nginx

* **/var/www/html** — начальная страница;
* **/etc/nginx** — директория с основными файлами настроек;
* **etc/nginx/nginx.conf** — главный конфигурационный файл Nginx;
* **/etc/nginx/sites-available** — каталог с конфигурациями для каждого из сайтов, содержащий информацию о них: имя, IP и другое;
* **/etc/nginx/sites-enabled** — в отличие от предыдущей директории, здесь содержатся конфигурации только активных сайтов, которые обслуживаются Nginx;
* **/etc/nginx/snippets** — сниппеты для подключения к основной конфигурации сервера;
* **/var/log/nginx** — директория с логами событий. 

## Остановка, перезагрузка конфигурации

<p style="font-size: 15px">
Когда <b>nginx</b> запущен, им можно управлять, вызывая исполняемый файл
с параметром <b>-s</b>. Используйте следующий синтаксис:
</p>

```html
nginx -s <сигнал>
```
Где ***сигнал*** может быть одним из нижеследующих:

* **stop** — быстрое завершение
* **quit** — плавное завершение
* **reload** — перезагрузка конфигурационного файла
* **reopen** — переоткрытие лог-файлов

<table border="1">
  <tr>
    <td>Команда должна быть выполнена под тем же пользователем, 
        под которым был запущен nginx.
    </td>
  </tr>
</table>

Например:
* остановить <b>nginx</b> с ожиданием окончания обслуживания запросов рабочими процессами

```html
nginx -s quit
```

* перезапустить <b>nginx</b> после изменений в конфигурационном файле, 
что бы вступили в силу изменения

```html
nginx -s reload
```

## Пример конфигурационного файла 

* **/etc/nginx/nginx.conf** - расположение конфигурационного файла

```html
user nginx;
# авоматическое определение кол-ва подключенных ядер процессора
# можно вручную указать данное кол-во
workeworker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;

    keepalive_timeout  65;

    server {
        listen       80;
        listen  [::]:80;

        location /static/ {
            autoindex on;
            alias /app/static/;
        }

        location / {
            include uwsgi_params;
            uwsgi_read_timeout 70;
            uwsgi_pass unix:/run/uwsgi.sock;
        }
    }
}
daemon off;


```
## Запускаем NGINX с помощью Docker

* Собираем контейнер
```html
docker build . -f Dockerfile -t <name container>
```
* Запускаем контейнер
```html
docker run -ti -p 80:80 <name container>
```

* Посмотреть содержимое контейнера с помощью оболочки **bash**

```html
docker run -ti <name container> bash
```

