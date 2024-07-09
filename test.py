#!/usr/bin/env python3

import datetime

def log_time():
    now = datetime.datetime.now()
    with open("/home/pi/repos/DielsiGarden/logs/timelog.txt", "a") as f:
        f.write(f"The script ran at {now}\n")

if __name__ == "__main__":
    log_time()
