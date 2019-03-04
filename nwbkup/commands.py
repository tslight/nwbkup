"""
Define commands to be run on different devices
"""


def get_backup_cmd(connection, server, path):
    """
    Return a backup command that corresponds to the connection objects
    device_type.
    """
    backup_commands = {
        'cisco_ios': ("copy running tftp://{}{}{}.cfg".format(
            server, path, connection.base_prompt.strip())),
        'fortinet': ("execute backup full-config tftp {}{}.cfg {}".format(
            path, connection.base_prompt.strip(), server)),
        'hp_procurve': ("copy running tftp {} {}{}.cfg".format(
            server, path, connection.base_prompt.strip())),
    }

    return backup_commands[connection.device_type]
