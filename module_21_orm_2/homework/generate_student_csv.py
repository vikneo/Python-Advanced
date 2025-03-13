import random
import os
from datetime import datetime

from utils import slugify, PATH_TO_FORLDER_FILE

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
author_name = [
    "Фёдор Достоевский",
    "Иван Тургенев",
    "Иван Гончаров",
    "Лев Толстой",
    "Михаил Лермонтов",
    "Антон Чехов",
    "Михаил Салтыков-Щедрин",
    "Александр Пушкин",
    "Николай Гоголь",
    "Александр Грибоедов",
]
book_title = [
    "Горе от ума 10",
    "Евгений Онегин 8",
    "Подросток 1",
    "Белые ночи 1",
    "Первая любовь 2",
    "Ася 2",
    "Руди 2",
    "Обыкновенная история 3",
    "Униженные и оскорбленные 1",
    "Ревизор 9",
    "Женитьба 9",
    "Записки сумасшедшего 9",
    "Повести 9",
    "Капитанская дочка 8",
    "История одного города 7",
    "Братья Карамазовы 1",
    "Дама с собачкой 6",
    "Герой нашего времени 5",
    "Война и мир. Книга 1 4",
    "Война и мир. Книга 2 4",
    "Обломов 3",
    "Отцы и дети 2",
    "Преступление и наказание 1",
    "Мертвые души 9",
    "Тарас Бульба 9",
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

    def __random_num_int_float(self) -> float:
        num_float = str(round(random.uniform(3, 6), 2))
        return num_float

    def __generate_email(self, ful_name: str) -> str:
        """
        Функция генерации email адреса
        """
        surname, name = ful_name.split(' ')
        _email = f"{slugify(surname)}.{slugify(name[0].lower())}@{random.choice(email_list)}.ru"
        return _email

    def __random_date_and_number(self):
        """
        функция генерирует случайную дату и число из диапазона 5 - 25
        """
        date_format = '%Y'
        date = datetime.strptime(f'{random.randint(1983, 2005)}', date_format).date()
        number = random.randint(5, 25)
        return date.year, number

    def students(self):
        """
        функция создает файл student.csv для таблицы Student
        """
        self.name_file = os.path.join(PATH_TO_FORLDER_FILE, f"{self.students.__name__}.csv")
        with open(self.name_file, 'w') as students:
            for name in full_name:
                _name = f"{name.replace(' ', ';')};+79{self.__generate_number_phone()};{self.__generate_email(name)};{self.__random_num_int_float()};{True if random.randint(0, 1) else ''}\n"
                students.write(_name)

    def authors(self):
        """
        функция создает файл authors.csv для таблицы Author
        """
        self.name_file = os.path.join(PATH_TO_FORLDER_FILE, f"{self.authors.__name__}.csv")
        with open(self.name_file, 'w') as authors:
            for name in author_name:
                data = f"{name.replace(' ', ';')}\n"
                authors.write(data)

    def books(self):
        """
        функция создает файл books.csv для таблицы Book
        """
        self.name_file = os.path.join(PATH_TO_FORLDER_FILE, f"{self.books.__name__}.csv")
        with open(self.name_file, 'w') as books:
            for title in book_title:
                data = title.split()
                book = f"{' '.join(data[:-1])};{self.__random_date_and_number()[1]};{self.__random_date_and_number()[0]};{data[-1]}\n"
                books.write(book)

    def run(self):
        """
        Запуск для создания файлов
        """
        self.students()
        self.authors()
        self.books()


if __name__ == "__main__":
    create_csv = GenerateCSVFile(path = PATH_TO_FORLDER_FILE)
    create_csv.run()
