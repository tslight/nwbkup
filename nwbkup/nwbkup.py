import csv
import datetime
import signal
import netmiko

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

CONFIGPATH = datetime.datetime.now().strftime('/Network/'"%Y/%b/")
BACKUPSRV = '10.1.0.6'
LOG = []


def backup_device(target_details):
    netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                          netmiko.ssh_exception.NetMikoAuthenticationException)
    connection = target_details[0]
    command = target_details[1]
    ip = target_details[2]
    success_string = target_details[3]
    try:
        connection.enable()
        output = connection.send_command(command)
        if success_string not in output:
            LOG.append("%s Failed Backup" % (ip))
        else:
            LOG.append("%s Backup OK" % (ip))
    except (netmiko_exceptions) as e:
        LOG.append("%s %s" % (ip, e))


def get_target_details(target, ip):
    if target == "cisco":
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': 'c',
            'password': 'c',
            'secret': 'cisco',
        }
        connection = netmiko.ConnectHandler(device)
        command = "copy running tftp://%s%s%s.cfg" % (
            BACKUPSRV, CONFIGPATH, connection.base_prompt.strip())
        ip = device['ip']
        success_string = " bytes copied in "
    elif target == "fortigate":
        device = {
            'device_type': 'fortinet',
            'ip': ip,
            'username': 'admin',
            'password': '',
        }
        connection = netmiko.ConnectHandler(device)
        command = "execute backup full-config tftp %s%s.cfg %s" % (
            CONFIGPATH, connection.base_prompt.strip(), BACKUPSRV)
        ip = device['ip']
        success_string = "Send config file to tftp server OK."
    elif target == "hp":
        device = {
            'device_type': 'hp_procurve',
            'ip': ip,
            'username': 'hp',
            'password': 'hp',
        }
        connection = netmiko.ConnectHandler(device)
        command = "copy running tftp %s %s%s.cfg" % (
            BACKUPSRV, CONFIGPATH, connection.base_prompt.strip())
        ip = device['ip']
        success_string = "error"
    else:
        LOG.append("%s device type not found" % (ip))

    return (connection, command, ip, success_string)


def parse_csv(csv):
    targets = []
    try:
        with open(csv, 'rb') as csvfile:
            file_reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                target = row['cmdfor'].lower()
                ip = row['ip']
                target_details = get_target_details(target, ip)
                targets.append(target_details)
    except IOError:
        print("Error: File does not appear to exist.")

    if targets:
        return targets


def write_log(path):
    logfile = datetime.datetime.now().strftime('nw_bot_log'"%b_%d_%H.%M"'.csv')
    logpath = path + logfile
    try:
        with open(logpath, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["IP", "Status"])
            for x in range(len(LOG)):
                writer.writerow(LOG[x].split(' ', 1))
                csv_file.close()
    except IOError:
        print("I/O Error.")
