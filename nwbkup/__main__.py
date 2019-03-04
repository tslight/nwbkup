"""
Parse arguments and implement threading
"""
import argparse
import os
import socket
from multiprocessing.pool import ThreadPool
from functools import partial
from .parse import parse_csv
from .connect import connect_and_backup
from .results import print_results
from .results import write_results


def chkfile(path):
    """
    Checks for valid file path.
    """
    if not os.path.isfile(path):
        msg = "{0} is not a file.".format(path)
        raise argparse.ArgumentTypeError(msg)
    return path


def chkdir(path):
    """
    Checks for valid directory path.
    """
    if not os.path.isdir(path):
        msg = "{} is not a directory.".format(path)
        raise argparse.ArgumentTypeError(msg)
    return path


def chkip(server):
    """
    Checks connectivity to an ip or hostname.
    """
    try:
        socket.gethostbyname(server)
        return server
    except socket.gaierror:
        msg = "Cannot connect to {}".format(server)
        raise argparse.ArgumentTypeError(msg)


def getargs():
    """
    Return a list of valid arguments. If no argument is given, default to $PWD.
    """
    parser = argparse.ArgumentParser(description=(
        "Backup network devices listed in [SOURCE] csv.\n"
        "Each device is backed up to [TFTP SERVER/PATH].\n"
        "Output success or failure to [DESTINATION] csv.\n"
    ))
    parser.add_argument("-s", "--source",
                        nargs='?',
                        default="./devices.csv",
                        type=chkfile,
                        help="a valid path to a csv file.")
    parser.add_argument("-d", "--destination",
                        nargs='?',
                        default=".",
                        type=chkdir,
                        help="Path to store the results csv in.")
    parser.add_argument("-t", "--tftp_server",
                        nargs='?',
                        default="10.1.0.6",
                        type=chkip,
                        help="TFTP IP or hostname to send the backups to.")
    parser.add_argument("-p", "--tftp_path",
                        nargs='?',
                        default="/Network",
                        type=str,
                        help="TFTP path to send the backups to.")
    return parser.parse_args()


def main():
    """
    Main function
    """
    args = getargs()
    targets = parse_csv(args.source)
    if targets:
        pool = ThreadPool(8)
        func = partial(connect_and_backup, args.tftp_server, args.tftp_path)
        results = pool.imap(func, targets)
        pool.close()
        pool.join()

    if results:
        results = print_results(results)
        write_results(results, args.destination)


if __name__ == '__main__':
    main()
