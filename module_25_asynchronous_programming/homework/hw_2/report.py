from datetime import datetime

import multiprocessing as mp
from py_markdown_table.markdown_table import markdown_table

from asyncs_cats import main_asyncs
from threadings_cats import main_threads
from processes_cats import main_processes

from config import OUT_PATH

COUNT_REQUEST = [10, 50, 100]


def write_markdown_report(data: str) -> None:
    """
    Запись таблицы markdown в файл report.md
    """
    file_name = "{}/report.md".format(OUT_PATH)
    with open(file_name, 'w') as _report:
        _report.write(
            f"# Report to task #2\n"
            f"* Asynchronous mode\n"
            f"* Threads mode\n"
            f"* Multiprocessing mode\n"
            f"{data}"
        )


def report() -> None:
    """
    Отчет по методам роботы (асинхронный, мультипоток, мультипроцессор)
    при 10, 50, 100 запросах.
    """
    result = []
    print("Запускаем анализ: ", end = '')
    for count_query in COUNT_REQUEST:
        _async = main_asyncs(count_query)
        print('.', end = '')
        _thread = main_threads(count_query)
        print('.', end = '')
        _process = main_processes(count_query)
        print('.', end = '')
        _process_pool = main_processes(count_query, queue = True)
        print('.', end = '')
        result.append(
            {
                "count_query": count_query,
                "date": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                "asyncs": _async['time'],
                "threads": _thread['time'],
                "processes": _process['time'],
                "processes Pool": _process_pool['time']
            }
        )
    print('.', end = '')
    markdown = markdown_table(result) \
        .set_params(row_sep = 'always', padding_width = 10, padding_weight = 'centerright') \
        .get_markdown()
    print(' Done!')
    write_markdown_report(markdown)


if __name__ == '__main__':
    mp.freeze_support()
    report()
    print("Анализ данных завершен! Статистику можно посмотреть в файле `report.md`")