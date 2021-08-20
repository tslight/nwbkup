"""
Define success string to look for in output from commands
"""


def get_backup_success(connection):
    """
    Returns a success string that corresponds to the connection objects
    device_type.
    """
    success_strings = {
        'cisco_ios': "bytes copied in",
        'fortinet': "Send config file to tftp server OK.",
        'hp_procurve': "TFTP download in progress.",
    }

    return success_strings[connection.device_type]
