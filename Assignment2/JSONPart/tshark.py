import os
import time
import csv
import subprocess   
webpcap = "vox.pcap"
command = 'tshark -r ' + webpcap +" -E separator=| -T fields -e frame.time_epoch -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e http.host -e http.request.uri -e http.referer -e frame.time -e tcp.flags.fin -e tcp.flags.reset -e tcp.flags.syn -e tcp.stream" 

splittedstring = command.split(' ')
# print " ".join(splittedstring)

l1 = subprocess.Popen(splittedstring,stdout=subprocess.PIPE).communicate()[0]

l2 = l1.split('\n')[:-1]


# print l1

connectionid = 0
mapping = {}
tree = []
line = 0

for elem in l2:
	# line+=1
	l3 = elem.split("|")
	# print l3
	if not(l3[5] == ''):
		# print line
		# print str(len(l3)) + str("  length of 13th array")
		if not(l3[12] == ''):
			# print l3
			# print int(l3[13])
			if int(l3[12]) in mapping:
				tree.append((mapping[int(l3[12])],l3[5],l3[5] + l3[6]))
			else:
				mapping[int(l3[12])] = connectionid
				tree.append((connectionid,l3[5],l3[5] + l3[6]))		
				connectionid += 1

tree.sort(key=lambda x:x[0])

# print "tree starting\n"
strans = ""
for elem in tree:
	strans +=  str(elem[0]) + "|" + str(elem[1]) + "|" + str(elem[2]) +"\n"

fieout = webpcap + "_downloadtree.txt"
foen = open(fieout,'w')
foen.write(strans)
foen.close()

# text_file = open("Output5.txt", "w")

# # print l1[:200]

# # for elem in l2:
# # 	print elem
# # 	text_file.write(elem)

# text_file.write(l1)

# text_file.close()

# conop = 0
# lineno = 0
# connectionsclosed = 0
# for i in xrange(len(l2)):
# 	l3 = l2[i].split(',')
# 	# print len(l3)
# 	# lineno += 1
# 	# if(len(l3) == 1):
# 		# print l3[0]
# 		# print lin/eno
# 	# if (len(l3) > 11):
# 	if(l3[9] == '1' or l3[10] == '1'):
# 		connectionsclosed += 1
# 	if(l3[11] == '1'):		
# 		conop += 1


# print conop
# print connectionsclosed

