#!/usr/bin/env python

from datetime import datetime
import gzip
import re
import sys
import math

import maidenhead as mh

my_loc = "JN97FE"


all_file = gzip.open('ALL3.TXT.gz', 'rt')

def dist_az(p1, p2):
    pos1 = mh.to_location(p1);
    pos2 = mh.to_location(p2);
    lat1 = math.radians(pos1[0])
    lon1 = math.radians(pos1[1])
    lat2 = math.radians(pos2[0])
    lon2 = math.radians(pos2[1])
    dlon = math.radians(pos2[1]-pos1[1])
    # compare identical inputs
    if lat1 == lat2 and lon1 == lon2:
        return 0., 0.
    dist = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) \
           * math.cos(lat2) * math.cos(dlon)
    dist = round(math.degrees(math.acos(dist)) * 60 * 1.853)
    x_1 = math.sin(dlon) * math.cos(lat2)
    x_2 = math.cos(lat1) * math.sin(lat2) \
        - (math.sin(lat1) * math.cos(lat2) * math.cos(dlon))

    azimuth = math.atan2(x_1, x_2)
    azimuth = math.degrees(azimuth)
    azimuth = round((azimuth + 360) % 360)
    return dist, azimuth

kms = 500
# ido, 0-500, 500-1000, ...
histogram = []
longest_distances = []
last_hour = ""

while True:
    row = all_file.readline().strip()
    if not row:
        break
    if not row.startswith('2'):
        continue
    msg_time = datetime.strptime(row[0:13] + " UTC", "%y%m%d_%H%M%S %Z")
    msg_freq = row[17:23]
    msg_direction = row[24:26]
    msg_mode = row[27:30]
    msg_text = row[48:]
    qra = ""
    #print(msg_text + "k")
    if not msg_freq == "14.074":
        continue
    if not msg_direction == "Rx":
        continue
    if not msg_mode == "FT8":
        continue
    if m := re.match('CQ ([A-Z0-9/]+) ([A-Z]{2}[0-9]{2})', msg_text):
        qra = m.group(2)
    else:
        pass
    print(msg_time)

    #msg_time.
    if not re.match(r"([A-Ra-r]{2}\d\d)(([A-Za-z]{2})(\d\d)?){0,2}", qra):
        continue
    dist, az = dist_az(my_loc, qra)
    #hours = msg_time.isoformat(timespec='hours')
    hours = msg_time.replace(minute=0, second=0, microsecond=0)
    timestamp = int(hours.timestamp())
    if hours != last_hour:
        last_hour = hours
        foo = [timestamp] + [0] * int((20000/kms))
        histogram.append(foo)
        longest_distances.append((timestamp, dist))
    histogram[-1][int(dist / kms) + 1] = histogram[-1][int(dist / kms) + 1] + 1
    if (longest_distances[-1][-1] < dist):
        longest_distances[-1] = (timestamp, dist)

all_file.close()
with open('longest.csv', "w", encoding="utf-8") as f:
    for e in longest_distances:
        f.write(str(int(e[0])) + "; " + str(e[1]) + "\n")
    f.close()
with open('hist.csv', "w", encoding="utf-8") as f:
    for e in histogram:
        for x in e:
            f.write(str(x) + "; ")
        f.write("\n")
    f.close()
print(longest_distances)
