# Материалы модуля 5 ***Практика***

## Запуск и контроль программ Linux (linux_process)

* перенаправление потоков в файлы
```html
python simple_app.py >>stdout.txt 2>>stderr.txt &
```

* Проверить запущенные процессы
```html
jobs
```

* Убить процесс
```html
kill -9 %ID_process || №_process
```

* test проверка существования файлов или директорий [документация](https://linux.die.net/man/1/test)

```html
test -d test; echo $?

// output # - Означает, что папка test существует
0

// или

test -d my_script.py; echo $?

// output # Такой файл отсутствует
1
```

## Команда ***lsof***

***краткая информация***

* **lsof** - команда, которая используется во многих Unix-подобных системах 
  для составления списка всех открытых файлов и процессов.

* На пример: отфильтровать порты связанный с "java" с помощью ***grep***
```html
lsof -i -n -P | grep java

java      12621 user   43u  IPv6 283382      0t0  TCP 127.0.0.1:63342 (LISTEN)
java      12621 user  302u  IPv6 288517      0t0  TCP 127.0.0.1:63342->127.0.0.1:55580 (ESTABLISHED)
```
В выше приведенном примере:
  * **-i** - вывод списка открытых сетевых сокетов
  * **-n** - скрывает имена DNS
  * **-P** - преобразование номеров портов в имена портов

### Аргументы

* -p - Она позволяет вывести все файлы, открытые процессом с указанным PID (с помощью **sudo**).
```html
 lsof -p 1

systemd   1 root  cwd   unknown                      /proc/1/cwd (readlink: Permission denied)
systemd   1 root  rtd   unknown                      /proc/1/root (readlink: Permission denied)
systemd   1 root  txt   unknown                      /proc/1/exe (readlink: Permission denied)
systemd   1 root NOFD                                /proc/1/fd (opendir: Permission denied)
```
* -iUDP - позволяет просматривать сведения об UDP-соединениях
```html
lsof -iUDP

yandex_br 13136 user  215u  IPv4 387333      0t0  UDP mdns.mcast.net:mdns 
yandex_br 13188 user   78u  IPv4 420068      0t0  UDP mdns.mcast.net:mdns 
```
* -t подавляет вывод всей информации за исключением ID процессов.
```html
lsof -t

2081
2082
2086
2087
...
```
