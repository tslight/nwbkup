def get_backup_success(connection):
    success_strings = {
        'cisco_ios': "bytes copied in",
        'fortinet': "Send config file to tftp server OK.",
        'hp_procurve': "TFTP download in progress.",
    }

    return success_strings[connection.device_type]
