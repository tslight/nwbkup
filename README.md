A Netmiko wrapper program to automate configuration backup of various networking
devices such as Cisco routers, HP Procurve switches and Fortinet firewalls.

Use csv file to store table of devices to backup, along with their details, and
write results back to a csv file.

```
usage: nwbkup [-h] [-l] [-s [SOURCE]] [-d [DESTINATION]] [-t [TFTP_SERVER]]
			  [-p [TFTP_PATH]]

Backup network devices listed in [SOURCE] csv. Each device is backed up to
[TFTP SERVER/PATH]. Output success or failure to [DESTINATION] csv.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            print a list of supported devices.
  -s [SOURCE], --source [SOURCE]
						a valid path to a csv file.
  -d [DESTINATION], --destination [DESTINATION]
						Path to store the results csv in.
  -t [TFTP_SERVER], --tftp_server [TFTP_SERVER]
						TFTP IP or hostname to send the backups to.
  -p [TFTP_PATH], --tftp_path [TFTP_PATH]
						TFTP path to send the backups to.
```
