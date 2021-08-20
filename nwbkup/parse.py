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
        print("Getting devices from {}...".format(csvpath))
        for row in file_reader:
            device = {
                'device_type': row['DEVICE'].lower(),
                'ip': row['IP'].lower(),
                'username': row['USERNAME'],
                'password': row['PASSWORD'],
                'timeout': int(row['TIMEOUT']),
            }
            targets.append(device)

    return targets
