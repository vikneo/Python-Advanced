import unittest

from module_04_flask.materials.flask_wtform import app


class TestRegistrationForm(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = '/'

    def test_field_mail(self) -> None:
        url = self.base_url + "registration"
        register = self.app.get(url)
        self.assertEqual(register.status_code, 405)
