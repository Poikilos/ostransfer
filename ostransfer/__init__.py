import sys
import os

# TODO: Implement (put the directories in ~/.config/ on the destination):
# - home-include-as-config.list
# - appdata-include-as-config.list.
# - localappdata-include-as-config.list.

class SetInfo:
    def __init__(self, path, config_dir="."):
        self.config_dir = config_dir
        self.path = path


class FolderInfo:
    def __init__(self, key, path, parent_set, config_dir="."):
        self.key = key
        self.path = path
        self.parent = parent_set
        self.config_dir = config_dir

    def copy_filtered(self, key, source, destination):
        this_i_path = os.path.join(self.config_dir, this_i_name)
        for sub in os.listdir(source):
            srcPath = os.path.join(source, sub)
            dstPath = os.path.join(destination, sub)
            if os.path.islink(subPath):
                continue
            if os.path.isdir(subPath):
                command = 'rsync -rt'
                # The first argument to match the source is used as the
                #   operation:
                '''
                for this_i_name in ["c-exclude.list", "c-exclude.more"]:
                    this_i_path = os.path.join(self.config_dir, this_i_name)
                    if os.path.isfile(this_i_path):
                        command += ' --exclude-from "{}"'.format(this_i_path)
                for this_i_name in ["c-include.list", "c-include.more"]:
                    this_i_path = os.path.join(self.config_dir, this_i_name)
                    if os.path.isfile(this_i_path):
                        command += ' --include-from "{}"'.format(this_i_path)
                '''
                command += ' "{}/"'.format(srcPath)
                command += ' "{}"'.format(dstPath)


class UserInfo:
    def __init__(self, path, config_dir="."):
        SetInfo.__init__(self, path, config_dir=config_dir)

        _appdata_parent = os.path.join(path, "AppData")
        if not os.path.isdir(_appdata_parent):
            raise FileNotFoundError(
                '"{}" was not found so the parent does not seem'
                ' to be a user profile.'.format(_appdata_parent)
            )
        self.infos = [
            FolderInfo("appdata", os.path.join(_appdata_parent, "Roaming"),
                       self, config_dir=config_dir),
            FolderInfo("localappdata", os.path.join(_appdata_parent, "Local"),
                       self, config_dir=config_dir),
            FolderInfo("home", path,
                       self, config_dir=config_dir),
        ]




class ComputerInfo:
    def __init__(self, boot_drive, config_dir="."):
        SetInfo.__init__(self, boot_drive, config_dir=config_dir)
        users_names = ["Users", "home"]
        self.users = None
        for users_name in users_names:
            users = os.path.join(boot_drive, users_name)
            if not os.path.isdir(users):
                continue
            self.users = users
            break
        if self.users is None:
            raise FileNotFoundError(
                'None of "{}" were in "{}" so it does not seem'
                ' to be a boot drive. Create one of them there to force'
                ' the operation to continue on a custom location.'
                ''.format(users_names, boot_drive)
            )
        self.infos = [
            FolderInfo("c", boot_drive,
                       self, config_dir=config_dir),
            FolderInfo("programdata", os.path.join(boot_drive, "ProgramData"),
                       self, config_dir=config_dir),
        ]


    def get_users(self):
        results = []
        for sub in os.listdir(self.users):
            subPath = os.path.join(self.users, sub)
            if os.path.islink(subPath):
                # Such as:
                # 'All Users' -> /media/ostransfer/WIN7/ProgramData
                # 'Default User' -> /media/ostransfer/WIN7/Users/Default
                continue
            if os.path.isdir(subPath):
                results.append(subPath)
        return results

    def copy_c(self, destination):
        raise NotImplementedError("copy_c")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Transfer files from one computer drive to another.'
    )

    # See <https://stackoverflow.com/a/25320300>:
    sub_parsers = parser.add_subparsers(dest='cmd')

    '''
    subcommand_a = sub_parsers.add_parser('include', help='include subs in a directory')
    subcommand_a.add_argument('include_path', help='Specify a path to include.')
    subcommand_a.add_argument('include_as', help='Specify what it is.')
    subcommand_b = sub_parsers.add_parser('exclude', help='exclude subs a directory')
    subcommand_b.add_argument('exclude_path', help='Specify a path to exclude.')
    subcommand_b.add_argument('exclude_as', help='Specify what the path is.')
    '''

    transfer_sc = sub_parsers.add_parser('transfer',
        help=('<source> <destination>         #Copy from one main drive to another,'
              ' adding a number to each user that is not on the destination.'),
    )
    transfer_sc.add_argument('source', help='Specify a source that has either a Users or home directory.')
    transfer_sc.add_argument('destination', help='Specify a destination that has either a Users or home directory.')

    ## parser.add_argument('--include', nargs="+", help='include several directories')
    ## parser.add_argument('--include', help='include a directory to the keep list.')
    # parser.add_argument('include', nargs=2, help='include subs in a directory')
    # parser.add_argument('exclude', nargs=2, help='exclude subs a directory')

    args = parser.parse_args()
    # print(args.accumulate(args.directory_names))
    '''
    if hasattr(args, "include_path"):
        print('include={}'.format(args.include_path))
        print('as={}'.format(args.include_as))
        # ^ becomes a list *if* nargs is set even if nargs=1
    if hasattr(args, "exclude_path"):
        print('exclude={}'.format(args.exclude_path))
        print('as={}'.format(args.exclude_as))
    '''
    if hasattr(args, 'transfer'):
        print('transfer={}'.format(args.transfer))
    if hasattr(args, 'source') and hasattr(args, 'destination'):
        print('source={}'.format(args.source))
        print('destination={}'.format(args.destination))
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
