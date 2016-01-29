from print_pkg.account import account
import sys


def main():
    args = len(sys.argv)
    if args < 2:
        filename = 'printer_account.csv'
    else:
        filename = sys.argv[1]
    account(custom_acc_file=filename)


if __name__ == '__main__':
    main()
