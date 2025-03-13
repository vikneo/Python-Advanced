from datetime import datetime


def avg_time_measure():
    """
    Функция считывает лог, обрабатывает время начало работы функции и ее конец, а так же,
    высчитывает и выводит среднее время работы в мили секундах
    """
    start_data = []
    end_data = []
    total_time_list = []

    with open('measure_me.log', 'r') as file:
        read_log = file.readlines()

    for _time in range(len(read_log)):
        if _time % 2 == 0:
            start_data.append(datetime.strptime(read_log[_time].split()[0], '%M:%S.%f'))
        else:
            end_data.append(datetime.strptime(read_log[_time].split()[0], '%M:%S.%f'))

    zipped = zip(start_data, end_data)

    for val in zipped:
        start, end = val[0], val[1]
        result = end - start
        total_time_list.append(result.microseconds / 1000)

    avg_time = sum(total_time_list) / len(total_time_list)

    return avg_time
