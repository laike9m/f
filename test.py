import glob
import os
import unittest
import sys

import f

TEXT = 'Today is a good day.\nTomorrow is another good day.\n'
TMP_LOG = 'tmp.log'
T_LOG = 't.log'


class TestF(unittest.TestCase):

    def setUp(self):
        for filename in glob.glob('*.log'):
            if os.path.isfile(filename):
                os.remove(filename)

    @staticmethod
    def inner():
        print('Today is a good day.')
        print('Tomorrow is another good day.')

    def assert_equal(self, filename, original_stdout, text=TEXT):
        with open(filename) as log_file:
            self.assertEqual(log_file.read(), text)

        assert original_stdout is sys.stdout

    def common_test(self, function, filename, text=TEXT):
        original_stdout = sys.stdout
        function()
        self.assert_equal(filename, original_stdout, text)

    def test_f_without_argument(self):
        self.common_test(f(self.inner), TMP_LOG)

    def test_f_with_one_argument(self):
        self.common_test(f(T_LOG)(self.inner), T_LOG)

    def test_f_with_two_positional_arguments(self):
        self.common_test(f(T_LOG, 'a')(self.inner), T_LOG)

    def test_f_with_two_mixed_arguments(self):
        self.common_test(f(T_LOG, mode='a')(self.inner), T_LOG)

    def test_f_with_two_keyword_arguments(self):
        self.common_test(f(filename=T_LOG, mode='a')(self.inner), T_LOG)

    def test_f_with_append_mode(self):
        f(filename=T_LOG)(self.inner)()
        self.common_test(f(filename=T_LOG, mode='a')(self.inner), T_LOG,
                         TEXT * 2)

    def test_f_as_context_manager(self):
        original_stdout = sys.stdout
        with f:
            self.inner()

        self.assert_equal(TMP_LOG, original_stdout)

        with f(filename=T_LOG, mode='a'):
            self.inner()

        self.assert_equal(TMP_LOG, original_stdout)


if __name__ == '__main__':
    unittest.main()
