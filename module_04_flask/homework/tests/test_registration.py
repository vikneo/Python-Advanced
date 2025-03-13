"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""
import unittest
from hw1_3.hw1_registration import app


class RegistrationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        app.config["WTF_CSRF_ENABLED"] = False
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/registration'

    def _register(self, email, phone, name, address, index, comment):
        return self.app.post(
            self.base_url,
            data=dict(email=email,
                      phone=phone,
                      name=name,
                      address=address,
                      index=index,
                      comment=comment,
                      )
        )

    def test_form_register(self):
        response = self._register(
            'qwe@qwe.com',
            1234567899,
            'Ivanov A.A.',
            'Novosibirsk',
            '630000',
            'comment')
        self.assertEqual(response.status_code, 200)

    def test_required_email(self):
        response = self._register(
            None,
            1234567899,
            'Ivanov A.A.',
            'Novosibirsk',
            '630000',
            ''
        )
        self.assertEqual(response.status_code, 400)

    def test_incorrect_email(self):
        response = self._register(
            'qwe.com',
            1234567899,
            'Ivanov A.A.',
            'Novosibirsk',
            '630000',
            ''
        )
        self.assertEqual(response.status_code, 400)

    def test_required_phone(self):
        response = self._register(
            'qwe@qwe.com',
            None,
            'Ivanov A.A.',
            'Novosibirsk',
            '630000',
            ''
        )
        self.assertEqual(response.status_code, 400)

    def test_incorrect_phone(self):
        response = self._register(
            'qwe@qwe.com',
            '0A12345678',
            'Ivanov A.A.',
            'Novosibirsk',
            '630000',
            ''
        )
        self.assertEqual(response.status_code, 400)

    def test_required_name(self):
        response = self._register(
            'qwe@qwe.com',
            1234567899,
            None,
            'Novosibirsk',
            '630000',
            'comment')

        self.assertEqual(response.status_code, 400)

    def test_incorrect_name(self):
        response = self._register(
            'qwe@qwe.com',
            1234567899,
            'Ivanov AA',
            'Novosibirsk',
            '630000',
            'comment')

        self.assertEqual(response.status_code, 400)

    def test_required_address(self):
        response = self._register(
            'qwe@qwe.com',
            1234567899,
            'Ivanov A.A.',
            None,
            '630000',
            'comment')

        self.assertEqual(response.status_code, 400)

    def test_required_index(self):
        response = self._register(
            'qwe@qwe.com',
            1234567899,
            'Ivanov A.A.',
            'Novosibirsk',
            None,
            'comment')

        self.assertEqual(response.status_code, 400)

    def test_incorrect_index(self):
        response = self._register(
            'qwe@qwe.com',
            1234567899,
            'Ivanov A.A.',
            'Novosibirsk',
            'AA6300',
            'comment')

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
