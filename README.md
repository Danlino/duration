```bash
$ duration 
usage: duration [-h] [-v] [-s] [-c N] [-w] [-W] [-a] [sec]

positional arguments:
  sec              time interval in seconds

options:
  -h, --help       show this help message and exit
  -v, --version    show program s version number and exit
  -s, --short      short units output format
  -c N, --count N  maximum number of units in the output
  -w, --weeks      weeks will also be used in the output
  -W, --max-weeks  show weeks as the highest time unit
  -a, --add-and    displays and before the last time unit
```
Example:
```
$ cut -d. -f1 /proc/uptime | duration
12 days, 4 hours, 57 minutes, 23 seconds

$ echo '123456789' | duration 
3 years, 10 months, 29 days, 21 hours, 33 minutes, 9 seconds

$ duration 123456789 -s
3y, 10mo, 29d, 21h, 33min, 9s

$ duration 123456789 -w
3 years, 10 months, 4 weeks, 1 day, 21 hours, 33 minutes, 9 seconds

$ duration 123456789 -W
204 weeks, 21 hours, 33 minutes, 9 seconds

$ duration 123456789 -c2
3 years, 10 months

$ duration 123456789 -c3 -a
3 years, 10 months, and 29 days
```
