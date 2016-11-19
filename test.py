import glob
import os
import unittest
import sys

import f


class TestF(unittest.TestCase):

    def setUp(self):
        for filename in glob.glob('*.log'):
            if os.path.isfile(filename):
                os.remove(filename)

    @staticmethod
    def inner():
        print('Today is a good day.')
        print('Tomorrow is another good day.')

    def assert_equal(self, filename, original_stdout):
        with open(filename) as log_file:
            self.assertEqual(
                log_file.read(),
                'Today is a good day.\nTomorrow is another good day.\n')

        assert original_stdout is sys.stdout

    def common_test(self, function, filename):
        original_stdout = sys.stdout
        function()
        self.assert_equal(filename, original_stdout)

    def test_f_without_argument(self):
        self.common_test(f(self.inner), 'tmp.log')

    def test_f_with_one_argument(self):
        self.common_test(f('t.log')(self.inner), 't.log')

    def test_f_with_two_positional_arguments(self):
        self.common_test(f('t.log', 'a')(self.inner), 't.log')

    def test_f_with_two_mixed_arguments(self):
        self.common_test(f('t.log', mode='a')(self.inner), 't.log')

    def test_f_with_two_keyword_arguments(self):
        self.common_test(f(filename='t.log', mode='a')(self.inner), 't.log')

    def test_f_as_context_manager(self):
        original_stdout = sys.stdout
        with f:
            self.inner()

        self.assert_equal('tmp.log', original_stdout)


if __name__ == '__main__':
    unittest.main()
