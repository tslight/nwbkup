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
    connection, command, ipaddr, success_string = target_details
    print("Backing up {} at {}...".format(
        connection.device_type, connection.ip))
    try:
        connection.enable()
        output = connection.send_command(command)
        if success_string not in output:
            msg = ("Failed to run {} on {}.\n{}".format(
                command, ipaddr, output))
        else:
            msg = ("Successfully ran {} on {}.\n".format(
                command, ipaddr))
    except Exception as exception:
        msg = ("Exception raised running {} on {}:\n{}\n".format
               (command, ipaddr, exception))

    print(msg)
    return msg
