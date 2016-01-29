#! /usr/bin/python

from print_pkg.account import account,get_abs_path
import sys

def main():
    args = len(sys.argv)
    if args < 2:
        filename = get_abs_path('../data/printer_account.csv')
    else:
        filename = sys.argv[1]
    account(custom_acc_file=filename)


if __name__ == '__main__':
    main()
