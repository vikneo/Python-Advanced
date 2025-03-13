"""
В приложении для парольной аутентификации, которое мы рассматривали, недостаточно debug-сообщений. Добавим после каждой
строки с кодом в функции input_and_check_password ещё по debug-сообщению, например:
f"Мы создали объект hasher {hasher!r}"
после строки:
"hasher = hashlib.md5()"
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
