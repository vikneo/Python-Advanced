import unittest

from hw2.decrypt import decrypt


class DecryptTestCase(unittest.TestCase):
    """
    Тестирования модуля hw2
    """
    def test_one_point(self) -> None:
        """
        Тест на проверку шифра с одной точкой.
        :return: None
        """
        option = ["1..2.3", "абра-кадабра.", "абрау...-кадабра", "абраа..-.кадабра", "абр......a."]
        for elem in option:
            result = decrypt(elem)
            self.assertTrue(result in ['23', 'абра-кадабра', 'a'])

    def test_two_point(self) -> None:
        """
        Тест на проверку шифра с двумя точками
        :return: None
        """
        option = ["абраа..-кадабра", "абра--..кадабра", "абра-када..абра."]
        for elem in option:
            result = decrypt(elem)
            self.assertEqual(result, 'абра-кадабра')

    def test_empty_string(self) -> None:
        """
        Тест на вывод результата в виде "пустая строка".
        :return: None.
        """
        option = ["1.......................", ".", "абра........", "a..бра....-...."]
        for elem in option:
            result = decrypt(elem)
            self.assertEqual(result, '')
