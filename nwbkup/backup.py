import datetime
import signal
import netmiko

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
    print("Backing up {} at {}...".format(
        connection.device_type, connection.ip))
    try:
        connection.enable()
        output = connection.send_command(cmd)
        if success not in output:
            msg = ("Failed to run {}.\n{}".format(cmd, output))
        else:
            msg = ("Successfully ran {}.\n".format(cmd))
    except Exception as e:
        msg = ("Exception raised running {}:\n{}\n".format(cmd, e))

    print(msg)
    return msg
