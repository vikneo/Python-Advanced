import sys
import unittest
from redirect import Redirect


class TestRedirect(unittest.TestCase):
    """
    Testing the context manager the Redirect class
    """
    @classmethod
    def setUpClass(cls):
        cls.stdout_text = 'Красивое лучше, чем уродливое.'
        cls.stderr_text = 'Ошибки никогда не должны замалчиваться.'

    def test_intercepting_streams_to_stdout_stderr(self):
        """
        Full flow testing stdout & stderr
        """
        with open('test_stdout.txt', 'w') as stdout_file, open('test_stderr.txt', 'w') as stderr_file:
            with Redirect(stdout_file, stderr_file):
                print(self.stdout_text)
                raise Exception(self.stderr_text)

        with open('test_stdout.txt', 'r') as stdout_file, open('test_stderr.txt', 'r') as stderr_file:
            out_file = stdout_file.read()
            err_file = stderr_file.read()
        self.assertTrue(self.stdout_text in out_file)
        self.assertTrue(self.stderr_text in err_file)

    def test_intercepting_stdout_only(self):
        """
        Testing the stdout flow only
        """
        with open('test_stdout_only.txt', 'w') as stdout_file:
            with Redirect(stdout_file):
                print(self.stdout_text)

        with open('test_stdout_only.txt', 'r') as stdout_file:
            out_file = stdout_file.read()
        self.assertTrue(self.stdout_text in out_file)

    def test_intercepting_stderr_only(self):
        """
        Testing the stderr flow only
        """
        with open('test_stderr_only.txt', 'w') as stderr_file:
            with Redirect(stderr=stderr_file):
                raise Exception(self.stderr_text)

        with open('test_stderr_only.txt', 'r') as stderr_file:
            err_file = stderr_file.read()
        self.assertTrue(self.stderr_text in err_file)

    def test_intercepting_stdout_stderr_tern_off(self):
        """
        Testing stdout and stderr streams without message interception
        """
        with open('test_stdout_tern.txt', 'w'), open('test_stderr_tern.txt', 'w'):
            with Redirect():
                print(self.stdout_text)
                raise Exception(self.stderr_text)

        with open('test_stdout_tern.txt', 'r') as stdout_file, open('test_stderr_tern.txt', 'r') as stderr_file:
            out_file = stdout_file.read()
            err_file = stderr_file.read()
            self.assertFalse(self.stdout_text in out_file)
            self.assertFalse(self.stderr_text in err_file)


if __name__ == '__main__':
    unittest.main()
    # with open('test_results.txt', 'a') as test_file_stream:
    #     runner = unittest.TextTestRunner(stream=test_file_stream)
    #     unittest.main(testRunner=runner)
