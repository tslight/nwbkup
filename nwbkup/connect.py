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
    result = [target['device_type'], target['ip']]
    path = datetime.datetime.now().strftime(path + "/%Y/%b/")

    try:
        connection = netmiko.ConnectHandler(**target)
        cmd = get_backup_cmd(connection, server, path)
        success = get_backup_success(connection)
        backup_result = backup(connection, cmd, success)
        result = result + backup_result
    except ValueError:
        error = "{} not supported.".format(target['device_type'])
        result = result + ["Failed", error]
    except KeyError:
        error = "Cannot find {}.".format(target['device_type'])
        result = result + ["Failed", error]
    except Exception as error:
        result = result + ["Failed", error]

    return result
