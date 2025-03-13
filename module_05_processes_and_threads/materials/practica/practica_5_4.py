import re
import subprocess
import shlex


def main() -> str:
    """
    Запускаем команду:
    curl -i -H "Accept: application/json" -X GET https://api.ipify.org?format=json
    ответ рапарсить и вернуть строку - IP-адрес
    """
    url = 'curl -i -H "Accept: application/json" -X GET https://api.ipify.org?format=json'
    command_list = shlex.split(url)
    response = subprocess.run(command_list, capture_output=True)
    # answer = re.findall(r'"ip":"[0-9]*.[0-9]*.[0-9]*.[0-9]*"', response.stdout.decode())
    answer = re.findall(r'"ip":"\d?\d?\d\.\d?\d?\d\.\d?\d?\d\.\d?\d?\d"', response.stdout.decode())
    ip_address = answer[0].split(":")[1].replace('"', '')
    return f"IP-address: {ip_address}"


def get_total_cmd_ps() -> str:
    """
    Запустить команду ps -A
    Подсчитать кол-во запущенных процессов и вывести результат
    """
    cmd = 'ps -A'
    cmd_list = shlex.split(cmd)
    response = subprocess.run(cmd_list, capture_output=True)
    answer = response.stdout.decode().split('\n')
    return f"Total process: {len(answer)}"


if __name__ == '__main__':
    print(main())
    print(get_total_cmd_ps())
