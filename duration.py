#!/usr/bin/env python3

__version__ = "0.1.0"
from datetime import datetime, timedelta
from argparse import Namespace
import argparse
import calendar
import sys

def units( aand: bool, cou: int, short: bool, y=0, m=0, w=0, d=0, H=0, M=0, S=0) -> str:
    
    if short:
        parts = []
        if y > 0: parts.append(f"{y}y")
        if m > 0: parts.append(f"{m}mo")
        if w > 0: parts.append(f"{w}w")
        if d > 0: parts.append(f"{d}d")
        if H > 0: parts.append(f"{H}h")
        if M > 0: parts.append(f"{M}min")
        if S > 0: parts.append(f"{S}s")

        if cou:
            parts = parts[:cou]
        
        return ", ".join(parts) if parts else "0s"
    
    else:
        parts = []
        
        if y == 1:  parts.append("1 year")
        elif y > 1: parts.append(f"{y} years")
        
        if m == 1:  parts.append("1 month")
        elif m > 1: parts.append(f"{m} months")
        
        if w == 1:  parts.append("1 week")
        elif w > 1: parts.append(f"{w} weeks")
        
        if d == 1:  parts.append("1 day")
        elif d > 1: parts.append(f"{d} days")
        
        if H == 1:  parts.append("1 hour")
        elif H > 1: parts.append(f"{H} hours")
        
        if M == 1:  parts.append("1 minute")
        elif M > 1: parts.append(f"{M} minutes")
        
        if S == 1:  parts.append("1 second")
        elif S > 1: parts.append(f"{S} seconds")
        
        if not parts:
            return "0 seconds"
        
        if cou:
            parts = parts[:cou]
        
        if aand:
            if len(parts) == 1:
                return parts[0]
            elif len(parts) == 2:
                return f"{parts[0]} and {parts[1]}"
            else:
                return ", ".join(parts[:-1]) + f", and {parts[-1]}"
        else:
            return ", ".join(parts)

def conversion(S: int, use_weeks: bool, only_weeks: bool) -> tuple:
    if S == 0:
        return 0, 0, 0, 0, 0, 0, 0

    remaining_seconds = S

    current = datetime.now()

    y = m = 0

    if not only_weeks:
        while True:
            try:
                test_date = current.replace(year=current.year - 1)
            except ValueError:
                if current.month == 2 and current.day == 29:
                    test_date = current.replace(year=current.year - 1, day=28)
                else:
                    break

            delta_sec = (current - test_date).total_seconds()

            if delta_sec > remaining_seconds:
                break

            current = test_date
            y += 1
            remaining_seconds -= delta_sec

        while True:
            prev_month = current.month - 1
            prev_year = current.year

            if prev_month == 0:
                prev_month = 12
                prev_year -= 1

            last_day = calendar.monthrange(prev_year, prev_month)[1]
            day = min(current.day, last_day)

            test_date = current.replace(year=prev_year, month=prev_month, day=day)

            delta_sec = (current - test_date).total_seconds()

            if delta_sec > remaining_seconds:
                break

            current = test_date
            m += 1
            remaining_seconds -= delta_sec

    extra_days = int(remaining_seconds // 86400)
    remaining_seconds %= 86400

    H = int(remaining_seconds // 3600)
    remaining_seconds %= 3600

    M = int(remaining_seconds // 60)
    S = int(remaining_seconds % 60)

    total_days = extra_days

    if use_weeks or only_weeks:
        w = total_days // 7
        d = total_days % 7
    else:
        w = 0
        d = total_days

    return y, m, w, d, H, M, S

def get_arg() -> Namespace:

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--version',
                        action='version',
                        version=f"duration {__version__}"
    )

    parser.add_argument('-s', '--short',
                        action='store_true',
                        default=False,
                        dest='short',
                        help='short units output format'
    )

    parser.add_argument('-c', '--count',
                        type=int,
                        default=0,
                        dest='count',
                        metavar='N',
                        help='maximum number of units in the output'
    )
    
    parser.add_argument('-w', '--weeks',
                        action='store_true',
                        dest='week',
                        default=False,
                        help='weeks will also be used in the output'
    )

    parser.add_argument('-W', '--max-weeks',
                        action='store_true',
                        dest='only_week',
                        default=False,
                        help='show weeks as the highest time unit'
    )

    parser.add_argument('-a', '--add-and',
                        action='store_true',
                        dest='add_and',
                        default=False,
                        help='shows "and" before the last unit (long format)'
    )

    parser.add_argument('-r', '--real-time',
                        action='store_true',
                        dest='real_time',
                        default=False,
                        help='show real date/time alongside relative'
    )

    parser.add_argument('-R', '--real-only',
                        action='store_true',
                        dest='real_only',
                        default=False,
                        help='show real date/time'
    )

    parser.add_argument('sec',
                        nargs='?',
                        type=int,
                        default=None,
                        help='time interval in seconds'
    )
    
    args = parser.parse_args()

    if len(sys.argv) == 1 and sys.stdin.isatty():
        parser.print_help()
        sys.exit(1)

    return args

def test2k(sec: int) -> bool:
    a2k = ( 2000 * 365 * 24 * 3600 ) + ( 500 * 24 * 3600 )
    if sec > a2k:
        print("Error: The time interval exceeds 2000 years.", file=sys.stderr)
        sys.exit(1)
    return True

def original_time(sec: int) -> str:
    now = datetime.now()
    ago = now - timedelta(seconds=sec)
    return f'({ago.strftime("%a, %-d.%b %Y %H:%M")})'

def get_sec(sec: int | None) -> int:
    if sec is not None:
        value = sec
    elif not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if not data:
            print("Error: No input provided via pipe.", file=sys.stderr)
            sys.exit(1)
        try:
            value = int(data)
        except ValueError:
            print("Error: Piped input must be an integer.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: Value in seconds is required.", file=sys.stderr)
        sys.exit(1)

    if value < 0:
        print("Warning: Negative value provided, treating as absolute duration", 
              file=sys.stderr)
        return abs(value)
    
    return value

def main():
    arg = get_arg()
    sec = get_sec(arg.sec)
    test2k(sec)
    cou = abs(arg.count)

    ys = conversion( sec, arg.week, arg.only_week )

    rt = original_time(sec)
    rl = units( arg.add_and, cou, arg.short, *ys )

    match ( arg.real_time, arg.real_only ):

        case ( False, False ):
            print(f"{rl}")

        case ( True, False ):
            print(f"{rl} {rt}")

        case ( _, True ):
            print(f"{rt}")

if __name__ == "__main__":
    main()
