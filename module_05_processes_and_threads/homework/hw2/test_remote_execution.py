import unittest
from remote_execution import app
from validators import TimeLimit

import tracemalloc


class TestRemoteExecution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tracemalloc.start()
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        cls.app = app.test_client()
        cls.base_url = "/run_code"

    def setUp(self):
        self.code = 'print(2**2**10)'
        self.timeout = 1

    def _data(self, code, timeout):
        return self.app.post(
            self.base_url,
            data=dict(code=code, timeout=timeout)
        )

    def test_not_work_specified_timeout(self):
        """
        Checking that the code will not work within the specified time
        """
        self.timeout = 0
        result = self._data(self.code, self.timeout)
        self.assertEqual(result.data.decode(), f"Код не уложился в данное время - {self.timeout}s")

    def test_form_valid(self):
        """
        Checking form fields for data validity
        """
        result = self._data(self.code, self.timeout)
        self.assertEqual(result.status_code, 200)

    def test_form_field_code(self):
        """
        Checking the "code" field for missing data
        """
        result = self._data(None, self.timeout)
        self.assertEqual(result.status_code, 400)

    def test_form_field_timeout(self):
        """
        Checking the "timeout" field for missing data
        """
        result = self._data(self.code, None)
        self.assertEqual(result.status_code, 400)

    def test_form_field_timeout_max(self):
        """
        Setting the "timeout" field to more than the maximum value
        """
        self.timeout = 31
        result = self._data(self.code, self.timeout)
        self.assertTrue(f"The time must not exceed 30" in result.data.decode())

    def test_form_field_timeout_negative(self):
        """
        Setting the "timeout" field to a negative value
        """
        self.timeout = -1
        result = self._data(self.code, self.timeout)
        self.assertTrue("The time must be a positive number" in result.data.decode())

    def test_sell_true_in_command(self):
        """
        Checking for "shell=True" in the command
        """
        self.code += '; shell=True'
        result = self._data(self.code, self.timeout)
        self.assertEqual(result.data.decode(), "The shell=True expression cannot be used")


if __name__ == '__main__':
    unittest.main()
