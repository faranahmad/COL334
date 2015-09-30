import os
import time
import csv
import subprocess

command = 'tshark -r vox.pcap -T fields -e frame.time_epoch -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e http.host -e http.request.uri -e http.referer -e frame.time -e tcp.flags.fin -e tcp.flags.reset -e tcp.flags.syn' 

splittedstring = command.split(' ')

l1 = subprocess.Popen(splittedstring,stdout=subprocess.PIPE).communicate()[0]

print l1