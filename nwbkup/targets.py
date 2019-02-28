import csv
import datetime
import signal
import netmiko

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


def print_device(device, connection, cmd):
    print("Success!"
          "\nDEVICE TYPE: {}".format(device['device_type']),
          "\nIP ADDRESS: {}".format(device['ip']),
          "\nHOSTNAME: {}".format(connection.base_prompt),
          "\nCOMMAND: {}\n".format(cmd))


def get_target_details(target, ip):
    """
    Takes device name and ip address as arguments and transforms them into a
    tuple containing a hashtable with device details, the command one wants to
    run on the device, it's IP address and a string to gauge the success of the
    command by.
    """
    path = datetime.datetime.now().strftime('/Network/'"%Y/%b/")
    server = '10.1.0.6'
    if target == "cisco":
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
            print_device(device, connection, cmd)
        except Exception as e:
            raise e
    elif target == "fortigate":
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
            print_device(device, connection, cmd)
        except Exception as e:
            raise e
    elif target == "hp":
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
            print_device(device, connection, cmd)
        except Exception as e:
            raise e
    else:
        raise ValueError(
            "{} device at {} not supported".format(target, ip))

    return (connection, cmd, success)


def parse_csv(csvpath):
    """
    Takes csv file as an argument, iterates over each row, to get a list of
    targets based on the device and IP columns of the csv, using
    get_target_details.
    """
    targets = []
    with open(csvpath, 'r') as csvfile:
        file_reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        print("\nGetting devices from {}...\n".format(csvpath))
        for row in file_reader:
            target = row['device'].lower()
            ip = row['ip'].lower()
            print("Testing connection to {} at {}...".format(
                target, ip), end=" ")
            try:
                target_details = get_target_details(target, ip)
                targets.append(target_details)
            except Exception as exception:
                print("Failed!\n{}\n".format(exception))

    return targets
