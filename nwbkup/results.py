"""
Process results
"""
import csv
import re
import datetime


def write_log(results, path):
    """
    Takes a filesystem path as an argument, and creates a csv using the results
    dictionary from parse_results.
    """
    logfile = datetime.datetime.now().strftime("/nwbkup-%H%M%S-%d%m%y.csv")
    logpath = path + logfile
    try:
        with open(logpath, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["IP", "Result"])
            for key, value in results.items():
                writer.writerow([key, value])
            csv_file.close()
        print("\nSuccessfully wrote results to {}\n".format(logpath))
    except IOError:
        print("I/O Error.")


def parse_results(results):
    """
    Extract IP address from results and add to dictionary where key is IP
    address and the the value is whether the command completed successfully.
    """
    new_results = {}
    for result in results:
        print(result)
        found = re.search('at (.+?)\\.\\.\\.', result)
        ipaddr = found.group(1)
        if "Failed" in result:
            new_results[ipaddr] = "Failed"
        else:
            new_results[ipaddr] = "Success"

    return new_results
