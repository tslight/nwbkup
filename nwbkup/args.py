"""
Get and check command line arguments.
"""
import argparse
import os
import socket


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
    parser.add_argument("-l", "--list",
                        action='store_true',
                        help="print a list of supported devices.")
    parser.add_argument("-s", "--source",
                        type=chkfile,
                        help="a valid path to a csv file.")
    parser.add_argument("-d", "--destination",
                        nargs='?',
                        default=".",
                        type=chkdir,
                        help="Path to store the results csv in.")
    parser.add_argument("-t", "--tftp_server",
                        type=chkip,
                        help="TFTP IP or hostname to send the backups to.")
    parser.add_argument("-p", "--tftp_path",
                        type=str,
                        help="TFTP path to send the backups to.")
    return parser.parse_args()
