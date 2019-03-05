"""
Main
"""
from multiprocessing.pool import ThreadPool
from functools import partial
from .getargs import getargs
from .parse import parse_csv
from .backup import backup
from .results import print_results
from .results import write_results


def main():
    """
    Main function
    """
    args = getargs()
    targets = parse_csv(args.source)
    if targets:
        pool = ThreadPool(8)
        func = partial(backup, args.tftp_server, args.tftp_path)
        results = pool.imap(func, targets)
        pool.close()
        pool.join()

    if results:
        results = print_results(results)
        write_results(results, args.destination)


if __name__ == '__main__':
    main()
