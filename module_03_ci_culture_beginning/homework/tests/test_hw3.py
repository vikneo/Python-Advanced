import unittest

from hw3.accounting import \
    app, \
    check_corrected_date, \
    storage


class MixinTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        storage.update(
            {
                2005: {
                    5: [550],
                    6: [990],
                    8: [990],
                    10: [1100],
                },
                2008: {
                    1: [300],
                    3: [1200],
                    10: [800],
                },
                2013: {
                    8: [2000],
                    10: [1000],
                    12: [880],
                },
            },
        )


class CalculateTestCase(MixinTestCase):
    """
    Тестирование модуля hw3
    """

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/'

    def test_correct_endpoint_add(self) -> None:
        """
        Тест на проверку endpoint "/add/<date>/<int:number>"
        :return: None
        """
        url = self.base_url + 'add/200705/800'
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def test_check_incorrect_data(self) -> None:
        """
        Тест на ввод не корректной даты
        :return: None.
        """
        with self.assertRaises(ValueError):
            check_corrected_date(date='2100')

    def test_correct_endpoint_calculate_year(self) -> None:
        """
        Тест на проверку endpoint "/calculate/<int:year>"
        :return: None.
        """
        url = self.base_url + 'calculate/2005'
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def test_output_data_for_year(self) -> None:
        """
        Тест на проверку подсчета сбережений за определенный год.
        :return: None.
        """
        year = 2005
        country = 0
        url = self.base_url + f'calculate/{year}'
        response = self.app.get(url)
        for res in storage[year]:
            country += sum(storage[year][res])
        self.assertEqual(response.data.decode(), f"Накопления за {year} год: ({country} руб.)")

    def test_correct_endpoint_calculate_year_mount(self) -> None:
        """
        Тест на проверку endpoint "/calculate/<int:year>/<int:mount>"
        :return: None
        """
        url = self.base_url + 'calculate/2010/05'
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def test_output_data_for_year_mount(self) -> None:
        """
        Тест на проверку подсчета сбережений за определенный год и месяц.
        :return: None.
        """
        year = 2013
        mount = 12
        url = self.base_url + f'calculate/{year}/{mount}'
        response = self.app.get(url)
        summ = sum(storage[year][mount])
        self.assertEqual(response.data.decode(), f"Накопления в 2013 году за 12-й месяц: ({summ} руб.)")
