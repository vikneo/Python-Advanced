import os
import random

from utils.slugify import slugify
from config import PATH_TO_FILE


full_name = ["Григорьев Андрей",
             "Березин Михаил",
             "Иванова Александра",
             "Хохлов Герман",
             "Волкова Ева",
             "Яковлев Георгий",
             "Орлова Ольга",
             "Елисеева Мирослава",
             "Соловьева Алисия",
             "Иванова Дарья",
             "Островский Всеволод",
             "Старикова Алина",
             "Макарова Кристина",
             "Овсянников Артём",
             "Соколова Мария",
             "Кузьмина Диана",
             "Гришина Фатима",
             "Тимофеева София",
             "Семин Давид",
             "Зайцева Елизавета",
             "Соловьев Кирилл",
             "Соловьева Мирослава",
             "Николаева Екатерина",
             "Воронин Даниил",
             "Князева Кира",
             "Жарова Кристина",
             "Максимова Кира",
             "Жукова Ольга",
             "Горелова Арина",
             "Лазарева Анна",
             "Давыдова Варвара",
             "Трифонова Лидия",
             "Одинцова Мария",
             "Иванов Демьян",
             "Максимов Давид",
             "Александров Лев",
             "Серова Варвара",
             "Николаева Елизавета",
             "Тарасов Алексей",
             "Щукин Ярослав"
             ]

email_list = ['inbox', 'mail', 'rambler', 'yandex', slugify(random.choice(full_name).split(' ')[0].lower())]


class GenerateCSVFile:
    """
    Класс генерирует файлы с расширением .csv для таблиц Author, Book, Student, ReceivingBooks
    """

    def __init__(self, path: str):
        self.name_file = None
        self.path = path

    def __generate_number_phone(self) -> str:
        """
        функция для генерации номера телефона
        """
        phone = [str(random.randint(0, 9)) for _ in range(9)]
        return ''.join(phone)

    def __generate_email(self, ful_name: str) -> str:
        """
        Функция генерации email адреса
        """
        surname, name = ful_name.split(' ')
        _email = f"{slugify(surname)}.{slugify(name[0].lower())}@{random.choice(email_list)}.ru"
        return _email
    
    def __generate_hesh_password(self):
        """
        Функция генерации заминированного пароля
        """
        import hashlib

        pswd = ''.join([chr(random.randint(77, 128)) for _ in range(10)])
        salt = os.urandom(32)
        hash_pswd = hashlib.pbkdf2_hmac(
            'sha256',
            pswd.encode('utf-8'),
            salt,
            10000
        )
        return hash_pswd

    def profiles(self):
        """
        функция создает файл profiles.csv для таблицы Profile
        """
        self.name_file = os.path.join(PATH_TO_FILE, f"{self.profiles.__name__}.csv")
        with open(self.name_file, 'w') as profile:
            for user_id in range(len(full_name)):
                _name = (f"{full_name[user_id].replace(' ', ';')};+79{self.__generate_number_phone()};"
                         f"{True if random.randint(0, 1) else ''};{user_id + 1}\n")
                profile.write(_name)

    def users(self):
        """
        функция создает файл users.csv для таблицы User
        """
        self.name_file = os.path.join(PATH_TO_FILE, f"{self.users.__name__}.csv")
        with open(self.name_file, 'w') as user:
            for name in full_name:
                _name = f"{self.__generate_email(name)};{self.__generate_hesh_password()}\n"
                user.write(_name)

    def run(self):
        """
        Запуск для создания файлов и рандомно с ошибкой
        """
        if random.randint(1, 9) == 2:
            raise ValueError('В качестве безопасности, процесс был прерван! Попробуйте еще раз.')
        
        self.profiles()
        self.users()


create_csv = GenerateCSVFile(path = PATH_TO_FILE)


if __name__ == "__main__":
    create_csv.run()
