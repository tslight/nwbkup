"""
Process results
"""
import csv
import datetime


def write_results(results, path):
    """
    Takes a filesystem path as an argument, and creates a csv using the results
    dictionary from parse_results.
    """
    logfile = datetime.datetime.now().strftime("/nwbkup-%H%M%S-%d%m%y.csv")
    logpath = path + logfile
    try:
        with open(logpath, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["DEVICE", "IP ADDRESS", "RESULT", "ERROR"])
            for result in results:
                writer.writerow((result))
            csv_file.close()
        print("\nSuccessfully wrote results to {}\n".format(logpath))
    except IOError:
        print("I/O Error.")


def print_results(results):
    """
    Extract IP address from results and add to dictionary where key is IP
    address and the the value is whether the command completed successfully.
    """
    for result in results:
        print("\nBackup up {} at {}... {}\n{}".format(*result))
