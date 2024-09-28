#!/usr/bin/env python

from datetime import datetime
import gzip
import re
import maidenhead as mh

all_file = gzip.open('ALL.TXT.gz', 'rt')

while True:
    row = all_file.readline().strip()
    if not row:
        break
    msg_time = datetime.strptime(row[0:13] + " UTC", "%y%m%d_%H%M%S %Z")
    msg_freq = row[17:23]
    msg_direction = row[24:26]
    msg_mode = row[27:30]
    msg_text = row[48:]
    #print(msg_text + "k")
    if not msg_freq == "14.074":
        continue
    if not msg_direction == "Rx":
        continue
    if not msg_mode == "FT8":
        continue
    if m := re.match('CQ ([A-Z0-9/]+) ([A-Z]{2}[0-9]{2})', msg_text):
        qra = m.group(2)
        lat, lon = mh.to_location(qra)
        print(lon, lat)
    else:
        pass
    #print(msg_time)

all_file.close()
