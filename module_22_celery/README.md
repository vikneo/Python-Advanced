# Очереди задач (module 22)

* Module [collections](https://docs.python.org/3/library/collections.html) официальная документация

## Очереди задач
* Класс **[deque()](https://docs-python.ru/standart-library/modul-collections-python/klass-deque-modulja-collections/)** модуля *collections* на русском языке
  * #### Коротко:
  * Класс **deque()** модуля *collections* возвращает новый объект deque(), 
  инициализированный слева направо данными из итерируемой последовательности *iterable*.
  При создании объекта очереди класс использует метод **dq.append()** для добавления элементов из итерации *iterable*. 
  Если итерация не указана, новая очередь **deque()** будет пуста.
  * #### Синтаксис:
  ```html
    from collections import deque
    dq = deque([iterable[, maxlen]])
  ```
  * #### Параметры:
    * **iterable** - итерируемая последовательность,
    * **maxlen (int)** - максимальное кол-во хранимых записей.
  * #### Возвращаемое значение:
    * новый объект Deque.

### To be continue >>>