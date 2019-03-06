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
    logfile = datetime.datetime.now().strftime("/nwbkup-%Y-%m-%d-%H.%M.%S.csv")
    logpath = path + logfile

    try:
        with open(logpath, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["DEVICE", "IP ADDRESS", "RESULT", "ERROR"])
            for result in results:
                writer.writerow((result))
                print("Backup up {} at {}... {}. {}".format(*result))
            csv_file.close()
        print("Successfully wrote results to {}".format(logpath))
    except IOError:
        print("I/O Error.")
