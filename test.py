import glob
import os
import unittest

import f


class TestF(unittest.TestCase):

    def setUp(self):
        for filename in glob.glob('*.log'):
            if os.path.isfile(filename):
                os.remove(filename)

    def test_f_without_argument(self):
        @f  # default log file is temp.log in current directory
        def inner():
            print('Today is a good day.')
            print('Tomorrow is another good day.')

        inner()
        with open('temp.log') as log_file:
            self.assertEqual(
                log_file.read(),
                'Today is a good day.\nTomorrow is another good day.\n')

    def test_f_with_one_argument(self):
        @f('t.log')  # default log file is temp.log in current directory
        def inner():
            print('Today is a good day.')
            print('Tomorrow is another good day.')

        inner()
        with open('t.log') as log_file:
            self.assertEqual(
                log_file.read(),
                'Today is a good day.\nTomorrow is another good day.\n')

    def test_f_with_two_arguments(self):
        @f('t.log', 'a')
        def inner():
            print('Today is a good day.')
            print('Tomorrow is another good day.')

        inner()
        inner()
        with open('t.log') as log_file:
            self.assertEqual(
                log_file.read(),
                ('Today is a good day.\nTomorrow is another good day.\n'
                 'Today is a good day.\nTomorrow is another good day.\n'))


if __name__ == '__main__':
    unittest.main()
