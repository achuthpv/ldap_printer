#! /usr/bin/python
import os

from print_pkg.account import account
import sys

from utils import PROJECT_ROOT


def main():
    args = len(sys.argv)
    if args < 2:
        filename = os.path.join(PROJECT_ROOT, './data/printer_account.csv')
    else:
        filename = os.path.abspath(sys.argv[1])

    dir_, _ = os.path.split(filename)
    if not os.path.exists(dir_):
        os.makedirs(dir_)

    month = None

    if args > 2:
        try:
            month = int(sys.argv[2])
        except ValueError:
            raise ValueError("2nd argument should be an integer which represents month")

    print("Generating accounting information. Please wait...")
    _, compact_file, verbose_file = account(custom_acc_file=filename, verbose=True, month=month)
    print("Accounting information is generated in directory %s" % os.path.dirname(filename))
    print("Generated files are %s and %s" % (compact_file, verbose_file))


if __name__ == '__main__':
    main()
