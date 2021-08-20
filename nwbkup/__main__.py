"""
Let's get this party started!
"""
from multiprocessing.pool import ThreadPool
from functools import partial
from columns import prtcols
from .args import getargs
from .parse import parse_csv
from .backup import backup
from .results import write_results
from .supported import get_supported


def main():
    """
    Iterate over csv to collect device details into list of targets. Create
    multithreading pool and map each element of targets to a thread. Print and
    write results list returned from backup function to destination csv.
    """
    args = getargs()
    if args.list:
        prtcols(get_supported(), 4)
        exit()

    targets = parse_csv(args.source)
    if targets:
        pool = ThreadPool(8)
        func = partial(backup, args.tftp_server, args.tftp_path)
        results = pool.imap(func, targets)
        pool.close()
        pool.join()
        if results:
            write_results(results, args.destination)


if __name__ == '__main__':
    main()
