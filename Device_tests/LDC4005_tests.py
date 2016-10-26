import sys
sys.path.insert(0, "/home/pawel1/Pulpit/PyLabDevice/Device")

from LDC4005 import LDC4005, BadDeviceException
from mock import patch
import unittest


class TestLDC4005(unittest.TestCase):

    @patch("IODevice.IODevice.getName")
    def test_should_raise_exception_when_name_of_device_is_incorrect(self, mock_for_get_name):
        ldc = LDC4005("/home/pawel1/Pulpit/PyLabDevice/Device_tests/LDC4005_tests.py")
        mock_for_get_name.return_value = "foo"
        with self.assertRaises(BadDeviceException):
            ldc. _check_if_device_is_correct()

if __name__ == '__main__':
    unittest.main()