"""
Количество попыток ввода неправильного пароля у нас строго зашито в коде программы, это плохо.
Пусть наша программа будет чуть более вежливой и спросит, сколько раз пользователь хочет ввести пароль.

Минимальное количество раз — два, максимальное — десять.

В случае возникновения ошибок нужно, конечно, правильным образом их залогировать.

В качестве кода программы можете взять то, что у вас получилось в результате
работы над work_3_1.py или нижеследующий код
"""

import getpass
import hashlib
import logging

logger = logging.getLogger("password_checker")


def input_and_check_password():
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()
    logger.debug("Был получен пароль")

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False

    try:
        hasher = hashlib.md5()
        logger.debug(f"Мы создали объект hasher: {hasher!r}")

        hasher.update(password.encode("latin-1"))
        logger.debug(f"Зашифровали пароль: {hasher.hexdigest()!r}")

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            logger.warning("Пароль успешно проверен.")
            return True

        logger.warning("Был введен не верный пароль.")
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


def input_count_number() -> int:
    while True:
        try:
            count_number: int = int(input("Сколько попыток выберите? min: 2, max: 10\n"
                                          "Введите кол-во попыток: "))
            logger.info(f"Пользователь ввел {count_number} попыток")
        except ValueError as err:
            logger.error(f"При вводе кол-во попыток введен не корректный символ\n"
                         f"описание ошибки: - {err}")
            count_number: int = int(input("Попробуйте еще раз! Поле должно содержать только цифры!\n"
                                          "Введите кол-во попыток: "))
            logger.info(f"Пользователь ввел {count_number} попыток")
        if 2 <= count_number <= 10:
            logger.info(f"Установлено {count_number} попыток")
            break

        logger.warning(f"Кол-во попыток вышло за диапазон от 2 до 10. Пользователь ввел: {count_number}")

    return count_number


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox\n")

    counter = input_count_number()

    while counter > 0:
        logger.info(f"У вас есть {counter} попыток")
        if input_and_check_password():
            exit(0)
        counter -= 1

    logger.error(f"Пользователь ввёл не правильный пароль за {counter} попыток!")
    exit(1)
