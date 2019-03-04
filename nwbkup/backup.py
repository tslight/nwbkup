"""
Backup device
"""
import re


def chkout(output, success):
    """
    Check output of command for success string and for a regex match with
    failed or error. Return a string indicating success or failure.
    """
    regex = ".*error.*|.*failed.*"
    failed = re.match(regex, output, re.IGNORECASE)
    if success not in output or failed:
        msg = ("Failed!\n{}".format(output))
    else:
        msg = ("Success!\n")
    return msg


def backup(connection, cmd, success):
    """
    Takes a tuple or list of device details as an argument. First
    element is the connection object returned from ConnectHandler,
    second element is the backup command to run, and the last is the
    string from the command's output that we are looking for to gauge
    success.

    Runs the command using the connection object and appends success status to
    log based on return string from command and IP address.
    """
    msg = ("Backing up {} at {}... ".format(
        connection.device_type, connection.ip))
    try:
        connection.enable()
        output = connection.send_command(cmd)
        msg += chkout(output, success)
    except Exception as error:
        msg += ("Failed!\n{}".format(error))

    return msg
