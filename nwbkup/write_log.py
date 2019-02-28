import csv
import datetime


def write_log(path, log):
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
            for row in enumerate(log):
                writer.writerow(log[row].split(' ', 1))
                csv_file.close()
    except IOError:
        print("I/O Error.")
