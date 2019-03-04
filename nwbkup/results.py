import csv
import re
import datetime


def write_log(results, path):
    """
    Takes a filesystem path as an argument, and creates a csv using our log
    list. Each element of the list is a row in the csv.
    """
    logfile = datetime.datetime.now().strftime("/nwbkup-%H%M%S-%d%m%y.csv")
    logpath = path + logfile
    try:
        with open(logpath, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["IP", "Status"])
            for key, value in results.items():
                writer.writerow([key, value])
            csv_file.close()
        print("\nSuccessfully wrote results to {}".format(logpath))
    except IOError:
        print("I/O Error.")


def parse_results(results):
    new_results = {}
    for r in results:
        print(r)
        ip = re.search("at (.+?)\.\.\.", r)
        ip = ip.group(1)
        if "Failed" in r:
            new_results[ip] = "Failed"
        else:
            new_results[ip] = "Success"

    return new_results
