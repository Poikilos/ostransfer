
import sys
import os

def main():

    import argparse
    parser = argparse.ArgumentParser(
        description='Transfer files from one computer to another.'
    )

    # See <https://stackoverflow.com/a/25320300>:
    sub_parsers = parser.add_subparsers(dest='cmd')

    subcommand_a = sub_parsers.add_parser('include', help='include subs in a directory')
    subcommand_a.add_argument('include_path', help='Specify a path to include.')
    subcommand_a.add_argument('include_as', help='Specify what it is.')
    # subcommand_a.add_argument('--opt1', help='option 1 help')
    subcommand_b = sub_parsers.add_parser('exclude', help='exclude subs a directory')
    subcommand_b.add_argument('exclude_path', help='Specify a path to exclude.')
    subcommand_b.add_argument('exclude_as', help='Specify what the path is.')

    ## parser.add_argument('--include', nargs="+", help='include several directories')
    ## parser.add_argument('--include', help='include a directory to the keep list.')
    # parser.add_argument('include', nargs=2, help='include subs in a directory')
    # parser.add_argument('exclude', nargs=2, help='exclude subs a directory')

    args = parser.parse_args()
    # print(args.accumulate(args.directory_names))
    if hasattr(args, "include_path"):
        print('include={}'.format(args.include_path))
        print('as={}'.format(args.include_as))
        # ^ becomes a list *if* nargs is set even if nargs=1
    if hasattr(args, "exclude_path"):
        print('exclude={}'.format(args.exclude_path))
        print('as={}'.format(args.exclude_as))
        # ^ becomes a list *if* nargs is set even if nargs=1


if __name__ == "__main__":
    sys.exit(main())
