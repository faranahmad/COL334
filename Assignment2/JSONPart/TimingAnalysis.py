import os
import time
import csv
import subprocess
import copy
import json
from haralyzer import HarParser, HarPage

webpcap = "vox.pcap"
command = 'tshark -r ' + webpcap +" -E separator=| -T fields -e frame.time_epoch -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e http.host -e http.request.uri -e http.referer -e frame.time -e tcp.flags.fin -e tcp.flags.reset -e tcp.flags.syn -e tcp.stream -e http.response.code" 

splittedstring = command.split(' ')

l1 = subprocess.Popen(splittedstring,stdout=subprocess.PIPE).communicate()[0]

l2 = l1.split('\n')[:-1]

fieout1 = webpcap + "_tsharkresp.txt"
foen1 = open(fieout1,'w')
foen1.write(l1)
foen1.close()

connectionid = 0
mapping = {}
tree = []
line = 0

tcp_url = [] ################## for tcp stream and url mapping ###################

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
				tcp_url.append([mapping[int(l3[12])],int(l3[12]),l3[5],l3[5]+l3[6],float(l3[0])])
			else:
				mapping[int(l3[12])] = connectionid
				tree.append((connectionid,l3[5],l3[5] + l3[6]))
				tcp_url.append([mapping[int(l3[12])],int(l3[12]),l3[5],l3[5]+l3[6],float(l3[0])])		
				connectionid += 1

tcp_url.sort(key=lambda x:x[0])
tree.sort(key=lambda x:x[0])
print tcp_url[0:5]
print tree[0:5]

print "len tcp", len(tcp_url), len(tree)


command3 = 'tshark -r vox.pcap -E separator=| -T fields -R '.split() +  ["tcp.flags.fin==1"] +  ' -e tcp.stream -e frame.time_epoch'.split()
# print " ".join(command3)
l22 = subprocess.Popen(command3,stdout=subprocess.PIPE).communicate()[0]
l23 = l22.split('\n')[:-1]


ending_times = []
for elem in l23:
	l31 = elem.split("|")
	ending_times.append(l31)

# print ending_times
# print len(ending_times)


with open('www.vox.com.har','r') as f:
# with open('google.har','r') as f:
# with open('www.nytimes.com.har','r') as f:
	har_parser = HarParser(json.loads(f.read()))

pageid = None

for alpha in har_parser.pages:
	pageid= alpha.actual_page['pageref']


DifferentDomains={}
SizeFromDomains={}
TypesOfFiles={}
DomainDNSTimes={}

def InsertNewUrl(inputarr,url,parenturl):
	ans = [len(inputarr),url,0,parenturl]
	idfound=-1
	for i in xrange(len(inputarr)):
		if inputarr[i][1]==parenturl:
			# ans[2]=i
			idfound=i
			break
	if idfound==-1:
		ans1 = [len(inputarr),parenturl,0,""]
		inputarr.append(ans1)
		idfound = len(inputarr)-1
	ans[0] = len(inputarr)
	ans[2] = idfound
	inputarr.append(ans)
	return inputarr

URLandRef = [[0,"",0,""]]

with open('www.vox.com.har','r') as f:
# with open('google.har','r') as f:
# with open('www.nytimes.com.har','r') as f:
	# har_parser = HarParser(json.loads(f.read()))
	harpage = HarPage(pageid,har_data=json.loads(f.read()))


DownloadTreeRead=map(lambda x: x.split('|'), open('vox.pcap_downloadtree.txt','r').read().split('\n')[:-1])
DownloadTreeRead = map(lambda x: [int(x[0])] + x[1:], DownloadTreeRead)
# print len(DownloadTreeRead)
# print DownloadTreeRead

ForEachConnection=[0]*(1+ DownloadTreeRead[-1][0])
for i in xrange(len(ForEachConnection)):
	ForEachConnection[i]=[i,[0 for j in xrange(6)],"",999999999999,0,0,[],"0"]

for elem in DownloadTreeRead:
	ForEachConnection[elem[0]][2]+=elem[2]+"|"

def FindConnId(webpath):
	for i in xrange(len(DownloadTreeRead)):
		if webpath==DownloadTreeRead[i][2]:
			return DownloadTreeRead[i][0]
	return -1

def RemoveHttp(s):
	# print s,
	if s[0:7]=="http://":
		s=s[7:]
	if s[0:8]=="https://":
		s=s[8:]
	# print s,
	# if s[0:4]=="www.":
	# 	s=s[4:]
	# print s
	return s

# print ForEachConnection

def ParseTime(s):
	# print s
	x1 = s.index('T')
	x2 = s.index('+')
	req = s[x1+1:x2]
	return map(float,req.split(':'))

inittime,fintime=0,0

count1 = 0
for elem in harpage.entries:
	# print elem['request']['url']
	if(count1==0):
		inittime = elem['startedDateTime']
	fintime=elem['startedDateTime']
	presentname=""
	domname=""
	for beta in  elem['request']['headers']:
		if beta['name']=="Host":
			domname = beta['value']	
	if domname in DomainDNSTimes:
		DomainDNSTimes[domname]=DomainDNSTimes[domname]+[elem['timings']['dns']]
	else:
		DomainDNSTimes[domname]=[elem['timings']['dns']]
	presentURL = RemoveHttp(elem['request']['url'])
	count1 +=1
	connid = FindConnId(presentURL)
	if connid<0:
		print "Not found", presentURL, elem['response']['status']
	else:
		# print elem['timings'], connid, presentURL
		ForEachConnection[connid][1][0]+=int(elem['timings']['blocked'])
		ForEachConnection[connid][1][1]+=int(elem['timings']['dns'])
		ForEachConnection[connid][1][2]+=int(elem['timings']['connect'])
		ForEachConnection[connid][1][3]+=int(elem['timings']['send'])
		ForEachConnection[connid][1][4]+=int(elem['timings']['wait'])
		ForEachConnection[connid][1][5]+=int(elem['timings']['receive'])
		ForEachConnection[connid][5]+=int(elem['response']['content']['size'])
		ForEachConnection[connid][6].append([int(elem['response']['content']['size']),int(elem['timings']['receive'])])
		ForEachConnection[connid][7]=domname

tcpidconnid={}

for elem in tcp_url:
	connid = elem[0]
	tcpidconnid[elem[1]]=connid
	ForEachConnection[connid][3]=min(ForEachConnection[connid][3],elem[4])

print tcpidconnid

ending_times = map(lambda x: [int(x[0]),float(x[1])], ending_times)

for elem in ending_times:
	if elem[0] in tcpidconnid:
		connid = tcpidconnid[elem[0]]
		ForEachConnection[connid][4]=max(ForEachConnection[connid][4],elem[1])
	else:
		"No idea about starting time of ", elem 

# print ForEachConnection

ProcessedTimes=[]
TimingGraph = []
DomainTimings =[]

for elem in ForEachConnection:
	ans=[0]*11
	# print elem
	# Connid, valid, times, websites, totaltime, active percentage, idle percentage, data recv, avg goodput, max goodput, domain
	ans[0]=elem[0]
	ans[1]=sum(elem[1])>0
	ans[2]=elem[1]
	ans[3]=elem[2]
	ans[4]=elem[4]-elem[3]
	ans[5]=(elem[1][3]+elem[1][4]+elem[1][5])/(1000*ans[4])
	ans[6]=1-ans[5]
	ans[7]=elem[5]
	if (elem[1][5]>0):
		ans[8]=(1.0*ans[7])/(elem[1][5])
	elem[6].sort(key= lambda x: x[0])
	if len(elem[6]):
		ans[9]=elem[6][-1]
		if ans[9][1]>0:
			ans[9]=(1.0*ans[9][0])/ans[9][1]
		else:
			ans[9]=0
	ans[10]=elem[7]
	print ans
	ProcessedTimes.append(ans)
	TimingGraph.append([elem[0],elem[2],elem[3],elem[4],0,elem[7]])

AverageGoodput = 0
totalt = 0
MaxMax = 0
for elem in ProcessedTimes:
	AverageGoodput += elem[7]
	totalt += elem[2][5]
	MaxMax = max(MaxMax,elem[9])

AverageGoodput*=1.0
AverageGoodput/=totalt
print "Average Goodput ", AverageGoodput, "Max goodput ", MaxMax
t1 = ParseTime(inittime)
t2 = ParseTime(fintime)
t3 = [t2[0]-t1[0],t2[1]-t1[1],t2[2]-t1[1]]
print "Total time is: ", t3[0], " hours, ", t3[1] ," minutes, ", t3[2] , " seconds."

# print TimingGraph
TimingGraph.sort(key=lambda x: x[2])

def FindNumInRange(t,totalarr):
	ans=0
	for elem in totalarr:
		if (t>=elem[2]) and (t <=elem[3]):
			ans +=1
	return ans

def FindNumInDomainRange(t,dom,totalarr):
	ans=0
	for elem in totalarr:
		if (t>=elem[2]) and (t <=elem[3]) and (dom == elem[5]):
			ans +=1
	return ans

def FindMaxPerDomain(arr):
	sofar=0
	for elem in arr[1:]:
		sofar= max(sofar,elem[1])
	return sofar

for elem in DomainDNSTimes:
	temp=[elem]
	for elem2 in TimingGraph:
		k=FindNumInDomainRange(elem2[2],elem,TimingGraph)
		temp.append([elem2[2],k])
	temp.append(FindMaxPerDomain(temp))
	DomainTimings.append(temp)
	print elem, DomainDNSTimes[elem]


for i in xrange(len(TimingGraph)):
	TimingGraph[i][4]= FindNumInRange(TimingGraph[i][2],TimingGraph)

print TimingGraph
for elem in DomainTimings:
	print elem

# print ending_times[0:10]