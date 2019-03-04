"""
Connect to and backup devices
"""
import datetime
import netmiko
from .backup import backup
from .commands import get_backup_cmd
from .success import get_backup_success


def connect_and_backup(server, path, target):
    """
    Takes device name and ip address as arguments and transforms them into a
    tuple containing the connection object, the command one wants to run on the
    device, and a string to gauge the success of the command by.
    """
    msg = ("Connecting to {} at {}... ".format(
        target['device_type'], target['ip']))
    path = datetime.datetime.now().strftime(path + "/%Y/%b/")

    try:
        connection = netmiko.ConnectHandler(**target)
        cmd = get_backup_cmd(connection, server, path)
        success = get_backup_success(connection)
        msg += "Success!\n"
        msg += backup(connection, cmd, success)
    except ValueError:
        msg += "Failed!\n{} not supported.".format(target['device_type'])
    except KeyError:
        msg += "Failed!\nCannot find {}.".format(target['device_type'])
    except Exception as error:
        msg += error

    return msg
