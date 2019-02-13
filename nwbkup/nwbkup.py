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
    """
    Takes a tuple or list of device details as an argument. First element is the
    connection object returned from ConnectHandler, second element is the backup
    command to run, third is the IP address of the device and the last is the
    string from the command's output that we are looking for to gauge success.

    Runs the command using the connection object and appends success status to
    log based on return string from command and IP address.
    """
    netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                          netmiko.ssh_exception.NetMikoAuthenticationException)
    connection, command, ipaddr, success_string = target_details
    try:
        connection.enable()
        output = connection.send_command(command)
        if success_string not in output:
            LOG.append("%s Failed Backup" % (ipaddr))
        else:
            LOG.append("%s Backup OK" % (ipaddr))
    except (netmiko_exceptions) as exception:
        LOG.append("%s %s" % (ipaddr, exception))


def get_target_details(target, ipaddr):
    """
    Takes device name and ip address as arguments and transforms them into a
    tuple containing a hashtable with device details, the command one wants to
    run on the device, it's IP address and a string to gauge the success of the
    command by.
    """
    if target == "cisco":
        device = {
            'device_type': 'cisco_ios',
            'ip': ipaddr,
            'username': 'c',
            'password': 'c',
            'secret': 'cisco',
        }
        connection = netmiko.ConnectHandler(device)
        command = "copy running tftp://%s%s%s.cfg" % (
            BACKUPSRV, CONFIGPATH, connection.base_prompt.strip())
        success_string = " bytes copied in "
    elif target == "fortigate":
        device = {
            'device_type': 'fortinet',
            'ip': ipaddr,
            'username': 'admin',
            'password': '',
        }
        connection = netmiko.ConnectHandler(device)
        command = "execute backup full-config tftp %s%s.cfg %s" % (
            CONFIGPATH, connection.base_prompt.strip(), BACKUPSRV)
        success_string = "Send config file to tftp server OK."
    elif target == "hp":
        device = {
            'device_type': 'hp_procurve',
            'ip': ipaddr,
            'username': 'hp',
            'password': 'hp',
        }
        connection = netmiko.ConnectHandler(device)
        command = "copy running tftp %s %s%s.cfg" % (
            BACKUPSRV, CONFIGPATH, connection.base_prompt.strip())
        success_string = "error"
    else:
        LOG.append("%s device type not found" % (ipaddr))

    return (connection, command, ipaddr, success_string)


def parse_csv(csvpath):
    """
    Takes csv file as an argument, iterates over each row, to get a list of
    targets based on the device and IP columns of the csv, using
    get_target_details.
    """
    targets = []
    try:
        with open(csvpath, 'rb') as csvfile:
            file_reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                target = row['Device'].lower()
                ipaddr = row['IP']
                target_details = get_target_details(target, ipaddr)
                targets.append(target_details)
    except IOError:
        print("Error: File does not appear to exist.")

    return targets


def write_log(path):
    """
    Takes a filesystem path as an argument, and creates a csv using our log
    list. Each element of the list is a row in the csv.
    """
    logfile = datetime.datetime.now().strftime('nw_bot_log'"%b_%d_%H.%M"'.csv')
    logpath = path + logfile
    try:
        with open(logpath, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["IP", "Status"])
            for row in enumerate(LOG):
                writer.writerow(LOG[row].split(' ', 1))
                csv_file.close()
    except IOError:
        print("I/O Error.")
