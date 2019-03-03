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
            device = row['device'].lower()
            ip = row['ip'].lower()
            target = (device, ip)
            targets.append(target)
