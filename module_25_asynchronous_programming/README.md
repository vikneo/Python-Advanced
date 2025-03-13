# Многозадачность: asyncio (module 25)

* [asyncio](https://docs.python.org/3/library/asyncio.html) - официальная документация
    * [asyncio.gather()](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)
    * [asyncio.to_thread()](https://docs.python.org/3/library/asyncio-task.html#running-in-threads)

Дополнительные материалы

* Полное руководство по модулю [asyncio](https://habr.com/ru/companies/wunderfund/articles/700474/) в Python (русския язык)
* [Асинхронный](https://habr.com/ru/articles/667630/) python без головной боли (русский язык)

## Конкурентный запуск нескольких корутин

* Сила **asyncio** в том, что этот модуль позволяет запускать множество корутин в конкурентном режиме.
* Эти корутины могут быть созданы в виде группы и сохранены, а потом их можно, все вместе, в одно и то же время, запустить

<table border="1">
  <tr>
    <td>Реализовать такой сценарий работы можно, воспользовавшись функцией <b>asyncio.gather()<b>.
    </td>
  </tr>
</table>

<hr>

**Корутина** - это функция которя может приостанавливать задачи в определенной точке, а потом продолжить их выполнение с того же места, **без блокировки** их выполнения.

<hr>

## Функция [asyncio.gather()](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)

Функция **gather()** не является блокирующей и позволяет вызывающей стороне группировать объекты, допускающие ожидание.Эти объекты, после группировки, можно запустить в конкурентном режиме. Кроме того — можно организовать ожидание их выполнения. Их выполнение можно и отменить.

```html
# синтаксис

awaitable asyncio.gather(*aws, return_exceptions=False)
```
**Пример**
```html
async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        print(f'Ответ сервера - {response.status}')
        result = await response.read()
        return result


async def get_all_cats() -> aiohttp.client.ClientSession:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(TIME_OUT)) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        # Выполнение коллекции объектов, допускающих ожидание
        return await asyncio.gather(*tasks)
```

Применение функции **gather()** даёт больше возможностей, чем обычное ожидание завершения работы задач.

Она позволяет рассматривать группу объектов, допускающих ожидание, как один такой объект.

### Резюме

* В результате — вызывать функцию **gather()** можно, передавая ей следующие сущности:
    * Множество задач;
    * Множество корутин;
    * Смешанный набор объектов, некоторые из которых являются задачами, а некоторые — корутинами;
* Примеры:

```html
выполнение нескольких корутин
asyncio.gather(coro1(), coro2())
```

Нельзя создать список или коллекцию таких объектов и передать их этой функции, так как это приведёт к ошибке

```html
функции нельзя передать напрямую список объектов, допускающих ожидание
asyncio.gather([coro1(), coro2()])
```

Можно передать этой функции распакованный и представленный в виде набора его элементов с использованием оператора **«звёздочка»** — *

```html
вызов функции с передачей ей распакованного списка объектов, допускающих ожидание
asyncio.gather(*[coro1(), coro2()])
```

<hr>

Создаем таблицы [markdown](https://github.com/hvalev/py-markdown-table)

<hr>