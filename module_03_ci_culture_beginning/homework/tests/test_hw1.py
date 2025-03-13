import re
import unittest

from hw1.hello_word_with_day import \
    app, \
    GREETINGS


class ContextMixin(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-word'
        self.username = 'Alex'

    def get_response(self):
        url = self.base_url + f'/{self.username}'
        response = self.app.get(url)
        return response


class HelloWordTestCase(ContextMixin):
    """

    """

    def test_correct_path_to_template(self) -> None:
        """
        Тест на корректность пути к шаблону.
        :return: None.
        """
        self.assertEqual(self.get_response().status_code, 200)

    def test_template_without_username(self) -> None:
        """
        Тест на путь к шаблону без аргументов.
        :return: None.
        """
        self.username = ''
        self.assertEqual(self.get_response().status_code, 404)

    def test_hello_username(self) -> None:
        """
        Тест на приветствие пользователя.
        :return: None.
        """
        context = self.get_response().data.decode()
        self.assertTrue(f"Привет, {self.username}" in context)

    def test_hello_username_with_day(self) -> None:
        """
        Тест на корректное пожелание хорошего "дня недели".
        :return: None
        """
        context = self.get_response().data.decode().split('.')
        con_text = context[1].replace('!', '').strip()
        self.assertTrue(con_text in GREETINGS)

    def test_incorrect_type_date(self) -> None:
        """
        Тест на проверку ввода имя пользователя в виде числа.
        :return: None
        """
        self.username = 123123
        context = self.get_response().data.decode().split('.')
        self.assertEqual(f"Привет, {self.username}", context[0])
