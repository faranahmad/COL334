import os
import time
import csv
import subprocess
import re


# print "0 to clear files \n1 to start script"
# t=raw_input()
# if t=="0":
# 	os.system("rm -rf *.csv")
# elif t=="1":

def findchar(s):
	a=[]
	for i in xrange(len(s)):
		if s[i]==".":
			a.append(i)
	return a

def checkipadd(s):
	ans=findchar(s)
	# print ans,s
	if len(ans)>=3:
		print ans
		return True
	else:
		return False

a= open('switzerland.txt')
read= a.read()
splittedinp = read.split('\n')

ans=[]
for i in xrange(len(splittedinp)):
	elem = splittedinp[i]
	if checkipadd(elem):
		ans.append([i,elem.replace('\r','')])

# print ans

def giveforip(ipadd):
	path="https://who.is/whois-ip/ip-address/" + ipadd
	l1 = subprocess.Popen(["curl",path],stdout=subprocess.PIPE).communicate()[0]
	splitted = l1.split('\n')

	ans=[ipadd]
	for elem in splitted:
		if elem[0:7].lower()=="netname" or elem[0:20].lower()=="network:network-name":
			ans.append(elem)
		if elem[0:7].lower()=="country" or elem[0:15].lower()=="network:country":
			ans.append(elem)
	return ans

# ansmapped=map(lambda x: [x[0],x[1],giveforip(x[1])],ans)
ansmapped=[]
for i in xrange(len(ans)):
	anspresent = giveforip(ans[i][1])
	print anspresent
	ansmapped.append([ans[i][0],anspresent])

print "%%%%%%%%%%%%%%"
print ansmapped

def getstringrel(a):
	if len(a[1])==1:
		return "\n"
	elif (len(a[1])==2):
		return a[1][1]+"\n"
	elif (len(a[1])>=3):
		return a[1][1]+"\n"+a[1][2]+"\n"
	else:
		return "\n"	

for elem in ansmapped:
	print elem
	indexnum=elem[0]
	splittedinp[indexnum] += "\n" + getstringrel(elem)

joined = "\n".join(splittedinp)

writtenfile= open("outfileswitzerland.txt",'w')
writtenfile.write(joined)
writtenfile.close()

# print l1