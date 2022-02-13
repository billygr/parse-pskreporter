#!/usr/bin/python3
# Parse https://www.pskreporter.info/cgi-bin/psk-freq.pl to my liking
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import os
import time
import datetime
import re

print ("Content-type: text/plain; charset=us-ascii\r\n")

#bug on string match 1810000 160m/17m
rep = {
    "1820000" : "160m", "1830000" : "160m",
    "1840000" : "160m",

    "3500000" : "80m", "3510000" : "80m", "3520000" : "80m",
    "3530000" : "80m", "3540000" : "80m", "3550000" : "80m",
    "3560000" : "80m", "3570000" : "80m", "3580000" : "80m",
    "3680000" : "80m", "3370000" : "80m",

    "5290000" : "60m", "5360000" : "60m",

    "7000000" : "40m", "7010000" : "40m", "7020000" : "40m",
    "7030000" : "40m", "7040000" : "40m", "7050000" : "40m",
    "7060000" : "40m", "7070000" : "40m", "7080000" : "40m",
    "7140000" : "40m",

    "10100000" : "30m", "10110000" : "30m", "10120000" : "30m",
    "10130000" : "30m", "10140000" : "30m", "10150000" : "30m",

    "14000000" : "20m", "14010000" : "20m", "14020000" : "20m",
    "14030000" : "20m", "14040000" : "20m", "14050000" : "20m",
    "14060000" : "20m", "14070000" : "20m", "14080000" : "20m",
    "14090000" : "20m", "14100000" : "20m", "14110000" : "20m",
    "14120000" : "20m", "14230000" : "20m", "14240000" : "20m",
    "14260000" : "20m",

    "18000000" : "17m", "18070000" : "17m", "18080000" : "17m",
    "18090000" : "17m", "18100000" : "17m", "18110000" : "17m",
    "18150000" : "17m",

    "21000000" : "15m", "21010000" : "15m", "21020000" : "15m",
    "21030000" : "15m", "21040000" : "15m", "21050000" : "15m",
    "21060000" : "15m", "21070000" : "15m", "21080000" : "15m",
    "21090000" : "15m", "21100000" : "15m", "21120000" : "15m",
    "21140000" : "15m", "21150000" : "15m", "21270000" : "15m",

    "24890000" : "12m", "24900000" : "12m", "24910000" : "12m",
    "24920000" : "12m", "24930000" : "12m",

    "27250000" : "10m",
    "28000000" : "10m", "28010000" : "10m", "28020000" : "10m",
    "28030000" : "10m", "28040000" : "10m", "28050000" : "10m",
    "28060000" : "10m", "28070000" : "10m", "28080000" : "10m",
    "28120000" : "10m", "28130000" : "10m", "28140000" : "10m",
    "28180000" : "10m", "28300000" : "10m", "28410000" : "10m",
    "28450000" : "10m", "28600000" : "10m",

    "50100000" : "6m", "50110000" : "6m", "50130000" : "6m",
    "50140000" : "6m", "50310000" : "6m", "50320000" : "6m",
    "50280000" : "6m", "51980000" : "6m",

    "70160000" : "4m",

    "144170000" : "2m", "144180000" : "2m",

    "1296600000" : "23cm"
}

lines = []

try:
    with open('psk-freq.pl','r') as f_in :
        #file_content=f_in.readlines()
        #lines = filter(None, (lines.rstrip() for lines in file_content))
        for line in f_in:
            if not line.startswith('#'):
              if not line.startswith('0'):
                line.rstrip()
                lines.append(line)
#                print(line)
    pass
except IOError as e:
# In case file does not exist OR you have no read permissions
    sys.exit("Unable to open file psk-freq.pl")

dt = os.path.getmtime("psk-freq.pl")
print ("Last Modified: ", (datetime.datetime.utcfromtimestamp(dt)),"UTC")

psk_wavelength_list = []

# Convert freq to wavelength
for line in lines:
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    line = pattern.sub(lambda m: rep[re.escape(m.group(0))], line)
    psk_wavelength_list.append(line)
# debug
    # print ("",line)

# debug
#print ("psk_wavelength_list content:\r\n",* psk_wavelength_list)
#print ("end of list")

# Sorted with wavelength
psk_wavelength_list.sort()

#    0        1     2     3   4
# frequency score #spots #tx #rx
# grid KM%, 10 mins

# Use a list for keeping the bands
band_list = []

score23cm = 0; spots23cm = 0
score2m = 0 ; spots2m = 0
score4m = 0 ; spots4m = 0
score6m = 0 ; spots6m = 0
score10m = 0 ; spots10m = 0
score12m = 0 ; spots12m = 0
score15m = 0 ; spots15m = 0
score17m = 0 ; spots17m = 0
score20m = 0 ; spots20m = 0
score30m = 0 ; spots30m = 0
score40m = 0 ; spots40m = 0
score60m = 0 ; spots60m = 0
score80m = 0 ; spots80m = 0
score160m = 0; spots160m = 0

for wavelength in psk_wavelength_list:
    m = re.split('\s+',wavelength)
    if m[0] == "6m":
        score6m = score6m + int(m[1])
        spots6m = spots6m + int(m[2])
        band_list.append("6m")
    elif m[0] == "10m":
        score10m = score10m + int(m[1])
        spots10m = spots10m + int(m[2])
        band_list.append("10m")
    elif m[0] == "12m":
        score12m = score12m + int(m[1])
        spots12m = spots12m + int(m[2])
        band_list.append("12m")
    elif m[0] == "15m":
        score15m = score15m + int(m[1])
        spots15m = spots15m + int(m[2])
        band_list.append("15m")
    elif m[0] == "17m":
        score17m = score17m + int(m[1])
        spots17m = spots17m + int(m[2])
        band_list.append("17m")
    elif m[0] == "20m":
        score20m = score20m + int(m[1])
        spots20m = spots20m + int(m[2])
        band_list.append("20m")
    elif m[0] == "30m":
        score30m = score30m + int(m[1])
        spots30m = spots30m + int(m[2])
        band_list.append("30m")
    elif m[0] == "40m":
        score40m = score40m + int(m[1])
        spots40m = spots40m + int(m[2])
        band_list.append("40m")
    elif m[0] == "60m":
        score40m = score60m + int(m[1])
        spots40m = spots60m + int(m[2])
        band_list.append("60m")
    elif m[0] == "80m":
        score80m = score80m + int(m[1])
        spots80m = spots80m + int(m[2])
        band_list.append("80m")
    elif m[0] == "160m":
        score160m = score160m + int(m[1])
        spots160m = spots160m + int(m[2])
        band_list.append("160m")
    elif m[0] == "2m":
        score2m = score2m + int(m[1])
        spots2m = spots2m + int(m[2])
        band_list.append("2m")
    elif m[0] == "4m":
        score2m = score4m + int(m[1])
        spots2m = spots4m + int(m[2])
        band_list.append("4m")
    elif m[0] == "23cm":
        score23m = score23cm + int(m[1])
        spots23m = spots23cm + int(m[2])
        band_list.append("23cm")
    else:
# just in case more frequencies added
        print ("Additional frequencies to add: ", wavelength);#print("m[0] value:",m[0])

# Score displayed is the SUM of all scores provided for all frequencies in this band
print("\r\n")
print ("Scored displayed is the SUM of all score provided for all frequencies in this band")

print ("  4m score: %-*s spots: %s" % (5,score4m, spots4m))
print ("  6m score: %-*s spots: %s" % (5,score6m, spots6m))
print (" 10m score: %-*s spots: %s" % (5,score10m, spots10m))
print (" 12m score: %-*s spots: %s" % (5,score12m, spots12m))
print (" 15m score: %-*s spots: %s" % (5,score15m, spots15m))
print (" 17m score: %-*s spots: %s" % (5,score17m, spots17m))
print (" 20m score: %-*s spots: %s" % (5,score20m, spots20m))
print (" 30m score: %-*s spots: %s" % (5,score30m, spots30m))
print (" 40m score: %-*s spots: %s" % (5,score40m, spots40m))
print (" 60m score: %-*s spots: %s" % (5,score60m, spots60m))
print (" 80m score: %-*s spots: %s" % (5,score80m, spots80m))
print ("160m score: %-*s spots: %s" % (5,score160m, spots160m))

print("\r\n")
print ("  4m Frequencies: %-*s spots: %s" % (5,band_list.count("4m"),spots4m))
print ("  6m Frequencies: %-*s spots: %s" % (5,band_list.count("6m"),spots6m))
print (" 10m Frequencies: %-*s spots: %s" % (5,band_list.count("10m"),spots10m))
print (" 12m Frequencies: %-*s spots: %s" % (5,band_list.count("12m"),spots12m))
print (" 15m Frequencies: %-*s spots: %s" % (5,band_list.count("15m"),spots15m))
print (" 17m Frequencies: %-*s spots: %s" % (5,band_list.count("17m"),spots17m))
print (" 20m Frequencies: %-*s spots: %s" % (5,band_list.count("20m"),spots20m))
print (" 30m Frequencies: %-*s spots: %s" % (5,band_list.count("30m"),spots30m))
print (" 40m Frequencies: %-*s spots: %s" % (5,band_list.count("40m"),spots40m))
print (" 60m Frequencies: %-*s spots: %s" % (5,band_list.count("60m"),spots60m))
print (" 80m Frequencies: %-*s spots: %s" % (5,band_list.count("80m"),spots80m))
print ("160m Frequencies: %-*s spots: %s" % (5,band_list.count("160m"),spots160m))
