#!/usr/bin/python3

from datetime import datetime
import gzip

all_file = gzip.open('ALL.TXT.gz', 'rt')

while True:
    row = all_file.readline()
    if not row:
        break
    msg_freq = row[17:23]
    if not msg_freq == "14.074":
        continue
    msg_time = datetime.strptime(row[0:13] + " UTC", "%y%m%d_%H%M%S %Z")
    print(msg_time)

all_file.close()

