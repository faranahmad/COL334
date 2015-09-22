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

for elem in harpage.entries:
	# print elem['request']['url']
	presentname=""
	presentURL = elem['request']['url']

	for elem1 in elem['request']['headers']:
		if elem1['name']=="Host":
			presentname = elem1['value']
			if (presentname) in DifferentDomains:
				DifferentDomains[presentname]+=1
			else:
				DifferentDomains[presentname] = 1 
			# print "Host is", elem1['value']
		elif elem1['name']== "Referer":
			# print "Referer is", elem1['value']
			# URLandRef[presentURL]= elem1['value']
			URLandRef = InsertNewUrl(URLandRef, presentURL, elem1['value'])
		# elif elem1['name']=="Connection":
			# print "Type of connection is", elem1['value']
	for elem1 in elem['response']['headers']:
		if elem1['name']=="Content-Type":
			typefile = elem1['value']
			if typefile in TypesOfFiles:
				TypesOfFiles[typefile] +=1
			else:
				TypesOfFiles[typefile] =1
			# print "Type of file:", elem1['value']
		elif elem1['name']=="Content-Length":
			typefile = elem1['value']
			if presentname in SizeFromDomains:
				SizeFromDomains[presentname] += int(elem1['value'])
			else:
				SizeFromDomains[presentname] = int(elem1['value'])
			# print "Length of file",elem1['value']

# print DifferentDomains
# print SizeFromDomains
# print TypesOfFiles

def GenerateStringFromHashTable(hs):
	ans=""
	for elem in hs.keys():
		ans+= elem + ","+ str(hs[elem]) + "\n"
	return ans

strDomNames = GenerateStringFromHashTable(DifferentDomains)
strSizDomains = GenerateStringFromHashTable(SizeFromDomains)
strTypeFiles = GenerateStringFromHashTable(TypesOfFiles)

a= open('DomainNames.csv','w')
a.write(strDomNames)
a.close()

a= open('SizeDomainNames.csv','w')
a.write(strSizDomains)
a.close()

a= open('TypesOfFiles.csv','w')
a.write(strTypeFiles)
a.close()

print URLandRef[0:10]

# print (har_parser.browser)

# print har_parser.']
# print har_parser.creator
# print har_parser.ima
# print harpage.image_size
# print harpage.image_load_time

