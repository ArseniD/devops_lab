import unittest2 as unittest
from py_extra.py_versions import PythonVersion


class TestPythonVersion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._connection = PythonVersion()

    def test_get_data(self):
        self.assertIsNotNone(self._connection)
        self.assertIsInstance(self._connection.get_data() , dict)
        self.assertIn('py_ver', self._connection.get_data())
        self.assertIn('py_name', self._connection.get_data())
        self.assertIn('py_venv', self._connection.get_data())
        self.assertIn('py_loc', self._connection.get_data())
        self.assertIn('pip_loc', self._connection.get_data())
        self.assertIn('py_path', self._connection.get_data())
        self.assertIn('packages', self._connection.get_data())
        self.assertIn('site_loc', self._connection.get_data())


    def test_format_json(self):
        self.assertIsNotNone(self._connection.__format__('json'))
        self.assertIsInstance(self._connection.__format__('json') , str)

    def test_format_yaml(self):
        self.assertIsNotNone(self._connection.__format__('yaml'))
        self.assertIsInstance(self._connection.__format__('yaml'), str)

    def test_format_all(self):
        self.assertIsNotNone(self._connection.__format__())
        self.assertIsInstance(self._connection.__format__(), str)

    def test_pip_location(self):
        self.assertIsNotNone(self._connection.pip_location())
        self.assertIsInstance(self._connection.pip_location(), list)

    def test_pip_packages(self):
        self.assertIsNotNone(self._connection.pip_packages())
        self.assertIsInstance(self._connection.pip_packages(), dict)

    def test_py_location(self):
        self.assertIsNotNone(self._connection.py_location())
        self.assertIsInstance(self._connection.py_location(), list)

    def test_py_names(self):
        self.assertIsNotNone(self._connection.py_names())
        self.assertIsInstance(self._connection.py_names(), list)


if __name__ == '__main__':
    unittest.main()

