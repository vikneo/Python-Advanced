import unittest
from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    """
    Testing exception the class BlockErrors
    """
    @staticmethod
    def _exemple_zero_division():
        return 1 / 0

    @staticmethod
    def _exemple_divergent_type():
        return 1 / '0'

    @staticmethod
    def _exemple_list(index: int = None):
        _new_list = [1, 2, 3]
        if index is None:
            return _new_list[3]

        return _new_list.index(index)

    def test_check_ZeroDivisionError(self):
        """ testing exception the ZeroDivisionError """

        with self.assertRaises(ZeroDivisionError):
            err_type = {TypeError}
            with BlockErrors(err_type):
                self._exemple_zero_division()

    def test_check_TypeError(self):
        """ testing exception the TypeError var.1 """

        with self.assertRaises(TypeError):
            err_type = {ZeroDivisionError}
            with BlockErrors(err_type):
                self._exemple_divergent_type()

    def test_check_nested_TypeError(self):
        """ testing exception the TypeError var.2 """

        with self.assertRaises(TypeError):
            put_err_type = {}
            with BlockErrors(put_err_type):
                in_err_type = {ZeroDivisionError}
                with BlockErrors(in_err_type):
                    self._exemple_divergent_type()

    def test_check_Exception(self):
        """ testing exception the Exception """

        with self.assertRaises(Exception):
            with BlockErrors({}):
                self._exemple_divergent_type()

    def test_check_IndexError(self):
        """ testing exception the IndexError """

        with self.assertRaises(IndexError):
            err_type = {ValueError}
            with BlockErrors(err_type):
                self._exemple_list()

    def test_check_ValueError(self):
        """ testing exception the ValueError """

        with self.assertRaises(ValueError):
            err_type = {IndexError}
            with BlockErrors(err_type):
                self._exemple_list(index=5)

    def test_check_ImportError(self):
        """ testing exception the ImportError """

        with self.assertRaises(ImportError):
            with BlockErrors({}):
                import discoteka


if __name__ == '__main__':
    unittest.main()
