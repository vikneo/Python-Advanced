import shlex
import subprocess
import time


def check_count_cmd(command: str) -> str:
    cmd_list = [shlex.split(_cmd) for _cmd in command.split('&&')]
    new_list_cmd = ""
    for index in range(len(cmd_list)):
        new_list_cmd += f"{' '.join(cmd_list[index])}; " if index != len(cmd_list) - 1 else f"{' '.join(cmd_list[index])}"

    return new_list_cmd


def get_total_proces_cmd_ps():
    cmd = 'ps -A'
    # cmd = 'ps -A && ls -l && ls -a'
    # cmd_list = shlex.split(cmd)
    # response = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    response = subprocess.Popen(check_count_cmd(cmd),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                close_fds=True)
    answer = response.stdout
    print(f"\nCommand: {cmd}\nTotal running process - {len(answer.read().decode().split('\n'))}\n")


def start_sleeping(command: str):
    procs_list = []
    for res_num in range(1, 10):
        res = subprocess.Popen(check_count_cmd(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True,
                               close_fds=True
                               )
        print("Process number {} started. PID: {}".format(res_num, res.pid))
        procs_list.append(res)

    return procs_list


def finished_sleeping(procs_list: list, timeout: int = None):
    start = time.time()
    for proc in procs_list:
        try:
            proc.wait(timeout=timeout)
            if proc.returncode == 0:
                print('Process with PID {} ended successfully'.format(proc.pid))
        except subprocess.TimeoutExpired as err:
            print('Process with PID {} ended unsuccessfully\n{}'.format(proc.pid, err))

    print(f"\nAll processes finished - {time.time() - start} sec\n{'-' * 10}")


def exemple_1():
    """
    Пример первый - Запуск параллельных 10 процессов с командой
    sleep 15 && echo "My mission is done here!"
    Вывод десять таких объектов так, чтобы всё вместе это заняло примерно 15 секунд, но не более 20.
    """
    procs_list = start_sleeping(command='sleep 15 && echo "My mission is done here!"')
    finished_sleeping(procs_list)


def exemple_2():
    """
    Пример второй - Запуск параллельных 10 процессов с командой
    sleep 10 && exit 1
    с таймером Popen.wait(9)
    """
    procs_list = start_sleeping(command='sleep 10 && exit 1')
    finished_sleeping(procs_list, timeout=9)


def exemple_3(timeout: int = None):
    res = subprocess.Popen(check_count_cmd(command="sleep 10 && exit 1"),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=True,
                           close_fds=True
                           )
    print("\nPID: {} - started".format(res.pid))

    try:
        res.wait(timeout=timeout)
        if res.returncode == 0:
            print('Process with PID {} ended successfully\n'.format(res.pid))
        else:
            print(f"PID {res.pid} ended. Status code - {res.returncode}\n")
    except subprocess.TimeoutExpired as err:
        print('Process with PID {} ended unsuccessfully.\n{}\n'.format(res.pid, err))


if __name__ == '__main__':
    while True:
        try:
            user_input = input("1 - get_total_proces_cmd_ps (Подсчитать кол-во процессов)\n"
                               "2 - sleeping (Пример первый - параллельный запуск 10 процессов)\n"
                               "3 - sleeping (Пример второй - параллельный запуск 10 процессов с Popen.wait(9))\n"
                               "4 - sleeping (Пример третий - запуск процесса с командой exit 1 и с timeout 9\n"
                               "5 - sleeping (Пример четвертый - запуск процесса с командой exit 1 и без timeout\n"
                               "Enter a number: ")

            if user_input == '1':
                get_total_proces_cmd_ps()
                continue
            elif user_input == '2':
                exemple_1()
            elif user_input == '3':
                exemple_2()
            elif user_input == '4':
                exemple_3(timeout=9)
            elif user_input == '5':
                exemple_3()
            else:
                break
        except KeyboardInterrupt:
            break

    print("Thank you!")
