import unittest

from hw4.person import Person


class PersonTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.person = Person(
            name='Alex',
            year_of_birth=1990,
            address='Moscow'
        )

    def test_get_age(self) -> None:
        age = self.person.get_age()
        self.assertEqual(age, 33)

    def test_get_name(self) -> None:
        name = self.person.get_name()
        self.assertEqual(name, 'Alex')

    def test_get_address(self) -> None:
        address = self.person.get_address()
        self.assertEqual(address, 'Moscow')

    def test_set_name(self) -> None:
        self.person.set_name(name='Bob')
        name = self.person.get_name()
        self.assertEqual(name, 'Bob')

    def test_set_address(self) -> None:
        self.person.set_address(address='Omsk')
        address = self.person.get_address()
        self.assertEqual(address, 'Omsk')

    def test_is_homeless(self) -> None:
        self.person.set_address(address='')
        address = self.person.is_homeless()
        self.assertTrue(address)
