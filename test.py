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

    def common_test(self, function, filename):
        orgianl_stdout = sys.stdout
        function()
        with open(filename) as log_file:
            self.assertEqual(
                log_file.read(),
                'Today is a good day.\nTomorrow is another good day.\n')

        assert orgianl_stdout is sys.stdout

    def test_f_without_argument(self):
        @f  # default log file is temp.log in current directory
        def inner():
            print('Today is a good day.')
            print('Tomorrow is another good day.')

        self.common_test(inner, 'tmp.log')

    def test_f_with_one_argument(self):
        @f('t.log')  # default log file is temp.log in current directory
        def inner():
            print('Today is a good day.')
            print('Tomorrow is another good day.')

        self.common_test(inner, 't.log')

    def test_f_with_two_positional_arguments(self):
        @f('t.log', 'a')
        def inner():
            print('Today is a good day.')
            print('Tomorrow is another good day.')

        self.common_test(inner, 't.log')

    def test_f_with_two_mixed_arguments(self):
        @f('t.log', mode='a')
        def inner():
            print('Today is a good day.')
            print('Tomorrow is another good day.')

        self.common_test(inner, 't.log')

    def test_f_with_two_keyword_arguments(self):
        @f(filename='t.log', mode='a')
        def inner():
            print('Today is a good day.')
            print('Tomorrow is another good day.')

        self.common_test(inner, 't.log')


if __name__ == '__main__':
    unittest.main()
