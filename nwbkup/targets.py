import datetime
import signal
import netmiko
from .backup import backup
signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


def get_success(device, connection, cmd):
    string = ("Success!"
              "\nDEVICE TYPE: {}".format(device['device_type']),
              "\nIP ADDRESS: {}".format(device['ip']),
              "\nHOSTNAME: {}".format(connection.base_prompt),
              "\nCOMMAND: {}\n".format(cmd))
    return ''.join(string)


def get_target_details(target):
    """
    Takes device name and ip address as arguments and transforms them into a
    tuple containing the connection object, the command one wants to run on the
    device, and a string to gauge the success of the command by.
    """
    device, ip = target
    msg = ("Testing connection to {} at {}...".format(device, ip))
    path = datetime.datetime.now().strftime('/Network/'"%Y/%b/")
    server = '10.1.0.6'
    if device == "cisco":
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': 'netseract',
            'password': 'C0mpl77xyeKK',
            'timeout': 5,
        }
        try:
            connection = netmiko.ConnectHandler(**device)
            cmd = ("copy running tftp://{}{}{}.cfg".format(
                server, path, connection.base_prompt.strip()))
            success = " bytes copied in "
            msg += get_success(device, connection, cmd)
        except Exception as error:
            msg += error
            return msg
    elif device == "fortigate":
        device = {
            'device_type': 'fortinet',
            'ip': ip,
            'username': 'netseract',
            'password': 'C0mpl77xyeKK',
            'timeout': 5,
        }
        try:
            connection = netmiko.ConnectHandler(**device)
            cmd = "execute backup full-config tftp %s%s.cfg %s" % (
                path, connection.base_prompt.strip(), server)
            success = "Send config file to tftp server OK."
            msg += get_success(device, connection, cmd)
        except Exception as error:
            msg += error
            return msg
    elif device == "hp":
        device = {
            'device_type': 'hp_procurve',
            'ip': ip,
            'username': 'netseract',
            'password': 'C0mpl77xyeKK',
            'timeout': 5,
        }
        try:
            connection = netmiko.ConnectHandler(**device)
            cmd = "copy running tftp %s %s%s.cfg" % (
                server, path, connection.base_prompt.strip())
            success = "TFTP download in progress."
            msg += get_success(device, connection, cmd)
        except Exception as error:
            msg += error
            return msg
    else:
        return "{} device at {} not supported".format(device, ip)

    msg += backup(connection, cmd, success)
    return msg
