"""
Connect to and backup devices
"""
import datetime
import netmiko
import re
from .commands import get_backup_cmd
from .success import get_backup_success


def chkout(output, success):
    """
    Check output of command for success string and for a regex match with
    failed or error. Return a string indicating success or failure.
    """
    regex = ".*error.*|.*failed.*"
    failed = re.match(regex, output, re.IGNORECASE)
    if success not in output or failed:
        return ["Failed", output]
    return ["Success", ""]


def backup(server, path, target):
    """
    Takes device name and ip address as arguments and transforms them into a
    tuple containing the connection object, the command one wants to run on the
    device, and a string to gauge the success of the command by.
    """
    result = [target['device_type'], target['ip']]
    path = datetime.datetime.now().strftime(path + "/%Y/%b/")

    try:
        connection = netmiko.ConnectHandler(**target)
        cmd = get_backup_cmd(connection, server, path)
        success = get_backup_success(connection)
        connection.enable()
        output = connection.send_command(cmd)
        result += chkout(output, success)
    except ValueError:
        error = "{} not supported.".format(target['device_type'])
        result += ["Failed", error]
    except KeyError:
        error = "Cannot find {}.".format(target['device_type'])
        result += ["Failed", error]
    except Exception as error:
        result += ["Failed", error]

    return result
