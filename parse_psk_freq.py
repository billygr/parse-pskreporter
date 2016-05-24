#!/usr/bin/python
# Parse https://www.pskreporter.info/cgi-bin/psk-freq.pl to my liking

import sys
import os
import time
import datetime
import re

print "Content-type: text/plain; charset=us-ascii\r\n"

#Pending 160m frequencies 1820000
rep = {
       "3500000" : "80m", "3510000" : "80m", "3530000" : "80m",
       "3580000" : "80m", "3680000" : "80m",

       "7000000" : "40m", "7010000" : "40m", "7020000" : "40m",
       "7030000" : "40m", "7040000" : "40m", "7080000" : "40m",

       "10100000" : "30m", "10110000" : "30m", "10120000" : "30m",
       "10130000" : "30m", "10140000" : "30m",

       "14000000" : "20m", "14010000" : "20m", "14020000" : "20m",
       "14030000" : "20m", "14040000" : "20m", "14050000" : "20m",
       "14060000" : "20m", "14070000" : "20m", "14080000" : "20m",
       "14090000" : "20m", "14100000" : "20m", "14110000" : "20m",
       "14120000" : "20m",

       "18000000" : "17m", "18070000" : "17m", "18080000" : "17m",
       "18090000" : "17m", "18100000" : "17m", "18110000" : "17m",

       "21000000" : "15m", "21010000" : "15m", "21020000" : "15m",
       "21030000" : "15m", "21040000" : "15m", "21070000" : "15m",
       "21080000" : "15m", "21090000" : "15m",

       "24890000" : "12m", "24900000" : "12m", "24910000" : "12m",

       "28010000" : "10m", "28020000" : "10m", "28030000" : "10m",
       "28040000" : "10m", "28070000" : "10m", "28080000" : "10m",
       "28120000" : "10m", "28140000" : "10m",

       "50100000" : "6m", "50280000" : "6m"
} 

try:
    with open('psk-freq.pl') as f_in:
      lines = filter(None, (lines.rstrip() for lines in f_in))
      pass
except IOError as e:
    #print "Unable to open file psk-freq.pl" #Does not exist OR no read permissions
    sys.exit("Unable to open file psk-freq.pl")

dt = os.path.getmtime("psk-freq.pl")
print "Last Modified: ", (datetime.datetime.utcfromtimestamp(dt)),"UTC"

psk_wavelength_list = []

#Convert freq to wavelength
for line in lines:
  rep = dict((re.escape(k), v) for k, v in rep.iteritems())
  pattern = re.compile("|".join(rep.keys()))
  line = pattern.sub(lambda m: rep[re.escape(m.group(0))], line)
  psk_wavelength_list.append(line)

# Sorted with wavelength
psk_wavelength_list.sort()

#    0        1     2     3   4
# frequency score #spots #tx #rx
# grid KM%, 15 mins

score6m = 0
score10m = 0
score12m = 0
score15m = 0
score17m = 0
score20m = 0
score30m = 0
score40m = 0
score80m = 0

spots6m = 0
spots10m = 0
spots12m = 0
spots15m = 0
spots17m = 0
spots20m = 0
spots30m = 0
spots40m = 0
spots80m = 0

for wavelength in psk_wavelength_list:
  m = re.split('\s+',wavelength)
  if m[0] == "6m":
    score6m = score6m + int(m[1])
    spots6m = spots6m + int(m[2])
  elif m[0] == "10m":
    score10m = score10m + int(m[1])
    spots10m = spots10m + int(m[2])
  elif m[0] == "12m":
    score12m = score12m + int(m[1])
    spots12m = spots12m + int(m[2])
  elif m[0] == "15m":
    score15m = score15m + int(m[1])
    spots15m = spots15m + int(m[2])
  elif m[0] == "17m":
    score17m = score17m + int(m[1])
    spots17m = spots17m + int(m[2])
  elif m[0] == "20m":
    score20m = score20m + int(m[1])
    spots20m = spots20m + int(m[2])
  elif m[0] == "30m":
    score30m = score30m + int(m[1])
    spots30m = spots30m + int(m[2])
  elif m[0] == "40m":
    score40m = score40m + int(m[1])
    spots40m = spots40m + int(m[2])
  elif m[0] == "80m":
    score80m = score80m + int(m[1])
    spots80m = spots80m + int(m[2])
# just in case more frequencies added 
  else:
    print wavelength

print "6m score:", score6m, "spots:", spots6m
print "10m score:", score10m, "spots:", spots10m
print "12m score:", score12m, "spots:", spots12m
print "15m score:", score15m, "spots:", spots15m
print "17m score:", score17m, "spots:", spots17m
print "20m score:", score20m, "spots:", spots20m
print "30m score:", score30m, "spots:", spots30m
print "40m score:", score40m, "spots:", spots40m
print "80m score:", score80m, "spots:", spots80m
