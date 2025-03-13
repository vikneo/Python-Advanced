"""
Хорошим паролем считается пароль, в котором есть
как минимум восемь символов, большие и маленькие буквы,
а также как минимум одна цифра и один символ из списка

!@#$%^&*()-+=_

Сделайте так, чтобы при вводе пароля проверялось, является ли пароль хорошим.
И если нет — предупредите пользователя (с помощью warning, конечно), что введённый пароль слабый.
В идеале ещё и объясните почему.
"""
import logging
import re

logger = logging.getLogger("password_checker")
logging.basicConfig(level='INFO')

def check_password(psw: str) -> str:
    """
    Проверка на качечство пароля
    """

    if len(psw) < 8:
        logger.error('You have a short password. The password must be at least 8 characters long')
    
    if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()--+=_])[A-Za-z\d!@#$%^&*()--+=_]{8,}$', psw):
        logger.warning('The entered password is weak. The password must contain letters of the Latin alphabet,'
                       'large and small, at least one digit and a special character !@#$%^&*()-+=_')
    else:
        logger.info("You have a good password")
    
    
if __name__ == "__main__":
    psw = '!Acd-casDc'

    check_password(psw=psw)
