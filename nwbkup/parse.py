"""
Process input csv
"""
import csv


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
            device = {
                'device_type': row['device'].lower(),
                'ip': row['ip'].lower(),
                'username': row['username'],
                'password': row['password'],
                'timeout': int(row['timeout']),
            }
            targets.append(device)

    return targets
