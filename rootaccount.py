#! /usr/bin/python

from print_pkg.account import account
import sys


def main():
    args = len(sys.argv)
    if args < 2:
        filename = 'printer_account.csv'
    else:
        filename = sys.argv[1]

    month = None

    if args > 2:
        try:
            month = int(sys.argv[2])
        except ValueError:
            raise ValueError("2nd argument should be an integer which represents month")

    account(custom_acc_file=filename, verbose=True, month=month)


if __name__ == '__main__':
    main()
