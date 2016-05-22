# parse-pskreporter

I am using the PSK Automatic Propagation Reporter (https://www.pskreporter.info) Best Frequency script
to get info about spotters and most used frequencies.

I do prefer a generic band mode, so this parser convert the data to wavelengths.

# HOWTO
* parse_psk_freq.py does the parsing and expect a psk-freq.pl in the current directory. I run it as a CGI (or directly from command line) put it on your /usr/lib/cgi-bin/

* update-psk-freq grabs the https://www.pskreporter.info/cgi-bin/psk-freq.pl using curl and it is run though a cron job every 15 min (rememeber to change the grid to your value, used to avoid the geo location of pskreporter
