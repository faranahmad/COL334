import json
from haralyzer import HarParser, HarPage

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
print DownloadTreeRead

ForEachConnection=[0]*(1+ DownloadTreeRead[-1][0])
for i in xrange(len(ForEachConnection)):
	ForEachConnection[i]=[i,[0 for j in xrange(6)],""]

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

print ForEachConnection

count1 = 0
for elem in harpage.entries:
	# print elem['request']['url']
	presentname=""
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
		# print int(elem['timings']['blocked'])
		# print int(elem['timings']['dns'])
		# print int(elem['timings']['connect'])
		# print int(elem['timings']['send'])
		# print int(elem['timings']['wait'])
		# print int(elem['timings']['receive'])

print ForEachConnection

	# print presentURL, elem[' ']

	# for elem1 in elem['timings']['headers']:
	# 	if elem1['name']=="Host":
	# 		presentname = elem1['value']
	# 		if (presentname) in DifferentDomains:
	# 			DifferentDomains[presentname]+=1
	# 		else:
	# 			DifferentDomains[presentname] = 1 
	# 		# print "Host is", elem1['value']
	# 	elif elem1['name']== "Referer":
	# 		# print "Referer is", elem1['value']
	# 		# URLandRef[presentURL]= elem1['value']
	# 		URLandRef = InsertNewUrl(URLandRef, presentURL, elem1['value'])
	# 	# elif elem1['name']=="Connection":
	# 		# print "Type of connection is", elem1['value']

# print DifferentDomains
# print SizeFromDomains
# print TypesOfFiles

print count1

def GenerateStringFromHashTable(hs):
	ans=""
	for elem in hs.keys():
		ans+= elem + ","+ str(hs[elem]) + "\n"
	return ans

# strDomNames = GenerateStringFromHashTable(DifferentDomains)
# strSizDomains = GenerateStringFromHashTable(SizeFromDomains)
# strTypeFiles = GenerateStringFromHashTable(TypesOfFiles)

# a= open('DomainNames.csv','w')
# a.write(strDomNames)
# a.close()

# a= open('SizeDomainNames.csv','w')
# a.write(strSizDomains)
# a.close()

# a= open('TypesOfFiles.csv','w')
# a.write(strTypeFiles)
# a.close()

# print URLandRef[0:10]

# print (har_parser.browser)

# print har_parser.']
# print har_parser.creator
# print har_parser.ima
# print harpage.image_size
# print harpage.image_load_time

