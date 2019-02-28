#!/usr/bin/env python
import argparse
import os
# import multiprocessing
from .parse_csv import parse_csv
from .nwbkup import backup_device
from .write_log import write_log


def chkfile(path):
    """
    Checks for valid file path.
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            return path
        else:
            msg = "{0} is not a file.".format(path)
    else:
        msg = "{0} does not exist.".format(path)

    raise argparse.ArgumentTypeError(msg)


def chkdir(path):
    """
    Checks for valid directory path.
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            msg = "{0} is not a directory.".format(path)
    else:
        msg = "{0} does not exist.".format(path)

    raise argparse.ArgumentTypeError(msg)


def getargs():
    """
    Return a list of valid arguments. If no argument is given, default to $PWD.
    """
    parser = argparse.ArgumentParser(
        description='Remove invalid characters from a given path.')
    parser.add_argument("csv", type=chkfile, default="./list.csv",
                        help="a valid path to a csv file.")
    parser.add_argument("log", type=chkdir, default=".",
                        help="a valid path to store the log csv in.")
    return parser.parse_args()


def main():
    # log = []
    args = getargs()
    targets = parse_csv(args.csv)
    if targets:
        print("Attempting to backup devices...\n")
        # processes = []
        for t in targets:
            backup_device(t)
            #     p = multiprocessing.Process(target=backup_device, args=(t,))
            #     processes.append(p)
            #     p.start()
            # for p in processes:
            #     p.join()
    # if log:
    #     write_log(args.log, log)


if __name__ == '__main__':
    main()
