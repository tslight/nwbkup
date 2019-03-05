"""
Connect to and backup devices
"""
import netmiko
import re
from datetime import datetime
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
    Construct backup command using dictionary from get_backup_cmd, success
    string from get_backup_success dictionary. Run backup command using netmiko
    and return result list.
    """
    result = [target['device_type'], target['ip']]
    path = datetime.now().strftime(path + "/%Y/%b/")

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
