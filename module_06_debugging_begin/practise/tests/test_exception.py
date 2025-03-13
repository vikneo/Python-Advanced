import unittest

from module_06_debugging_begin.practise.work_2_3 import app, calculate


class TestExceptions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        cls.app = app.test_client()
        cls.base_url = "/calculate/"

    def test_page(self):
        response = self.app.get(self.base_url + "2 + 2")
        self.assertEqual(response.status_code, 200)

    def test_exception_ZeroDivisionError(self):
        with self.assertRaises(ZeroDivisionError):
            calculate("2 / 0")

    def test_exception_NameError(self):
        with self.assertRaises(NameError):
            calculate("3 + a")

    def test_exception_SyntaxError(self):
        with self.assertRaises(SyntaxError):
            calculate("2 a 2")


if __name__ == '__main__':
    unittest.main()