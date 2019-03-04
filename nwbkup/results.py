"""
Process results
"""
import csv
import re
import datetime


def write_destination_csv(results, path):
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


def parse_results(results):
    """
    Extract IP address from results and add to dictionary where key is IP
    address and the the value is whether the command completed successfully.
    """
    new_results = []
    for result in results:
        print(result)
        new_result = []
        device = re.search('to (.+?) at', result)
        device = device.group(1)
        new_result.append(device)
        ipaddr = re.search('at (.+?)\\.\\.\\.', result)
        ipaddr = ipaddr.group(1)
        new_result.append(ipaddr)
        if "Failed" in result:
            error = re.search('Failed\\!\\n(.+?)$', result)
            error = error.group(1)
            new_result.append("Failed")
            new_result.append(error)
        else:
            new_result.append("Success")
            new_result.append("")
        new_results.append(new_result)

    return new_results
