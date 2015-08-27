import os
import time
import csv
import subprocess


t=raw_input("Enter the subnet probe\n")
# subnettoprobe= "10.208.26.0/24"
subnettoprobe = t
t1=int(raw_input("Enter frequency per hour (0) for max frequency\n"))
freqinhour = 0
# if 0 then no time delay
# timedelay=0
timedelay=t1

if freqinhour==0:
	timedelay=0
else:
	timedelay = 3600/freqinhour

nmapfile = 'nmaps_kara.csv'
ifconfigfile='ifconfigs.csv'
osmaps = 'osmaps.csv'
count=0


# print "0 to clear files \n1 to start script"
# t=raw_input()
# if t=="0":
# 	os.system("rm -rf *.csv")
# elif t=="1":
while (True):
	print "Starting for: ",count," on ",subnettoprobe
	t1 = time.time()
	l1 = subprocess.Popen(["nmap","-n", "-sP", subnettoprobe],stdout=subprocess.PIPE).communicate()[0]
	print "Done Server On Off"
	#l2 = subprocess.Popen(["nmap","-n", "-O", subnettoprobe],stdout=subprocess.PIPE).communicate()[0]
	#print "Done OS Checking"
	#l3 = subprocess.Popen(["ifconfig"],stdout=subprocess.PIPE).communicate()[0]
	#print "ifconfig"
	count +=1
	# l1 = os.system("nmap -n -sP 10.208.26.0/24")
	# l2 = os.system("nmap -n -O 10.208.26.0/24")
	# l3 = os.system("ifconfig")
	f1 = open(nmapfile,"a")
	# print type(l1),"type of l1",l1
	f1.write(str(t1)+"\n"+l1+"\n")
	f1.close()
	time.sleep(timedelay)
