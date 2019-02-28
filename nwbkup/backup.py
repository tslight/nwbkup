import datetime
import signal
import netmiko
import re

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


def backup_device(target_details):
    """
    Takes a tuple or list of device details as an argument. First element is the
    connection object returned from ConnectHandler, second element is the backup
    command to run, third is the IP address of the device and the last is the
    string from the command's output that we are looking for to gauge success.

    Runs the command using the connection object and appends success status to
    log based on return string from command and IP address.
    """
    connection, cmd, success = target_details
    regex = ".*error.*|.*failed.*"
    print("Backing up {} at {}...".format(
        connection.device_type, connection.ip), end=" ")
    try:
        connection.enable()
        output = connection.send_command(cmd)
        failed = re.match(regex, output, re.IGNORECASE)
        if success not in output or failed:
            msg = ("Failed!\nCOMMAND: {}\nERROR: {}".format(cmd, output))
        else:
            msg = ("Success!\nCOMMAND: {}\n".format(cmd))
    except Exception as e:
        msg = ("Failed!\nCOMMAND: {}\nERROR: {}\n".format(cmd, e))

    print(msg)
