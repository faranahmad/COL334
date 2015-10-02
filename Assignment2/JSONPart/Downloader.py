# TODO: Add Exception
# TODO: Add proxy issues
# TODO: Figure out Accept header
# TODO: Figure out how to make files with the content
# TODO: Add threading

import socket
import socks
import os

# os.environ["https_proxy"]="https://10.10.78.22:3128"
# socket.socket = socks.socksocket
# HOST = "ea-cdn.voxmedia.com"   
# PORT = 80  
#create paket-string from list
def makestr(s):
	rs = ""
	rs = "\r\n".join(s)
	rs+="\r\n"
	rs+="\r\n"
	return rs


#  opening the port and sending the get request and recieving the data
def sendcap(sdata,HOST,PORT):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, "10.10.78.22", 3128)
	# s.set_proxy(socks.HTTP, "10.10.78.22", 3128)
	
	s.connect((HOST, PORT))
	s.sendall(sdata)

	recvd=""
	print "started data\n"
	while True:
		print "Data coming\n"
		data = s.recv(4096)
		if not data: 
			print " Done \n"; break
		recvd += data
	s.close()

	return recvd

def generaterequestwithoutref(url_name,HOST,state_of_connection):
	xy = []  
	xy.append("GET " + url_name + " HTTP/1.1")
	xy.append("Host: " + HOST )
	xy.append("User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0")
	#  this can vary
	xy.append("Accept: */*")
	xy.append("Accept-Language: en-us;en;q=0.35")
	xy.append("Accept-Encoding: gzip, deflate")
	xy.append("DNT: 1")
	xy.append("Connection: " + state_of_connection)
	return xy

#  generating a get request
def generaterequest(url_name,HOST,Referer,state_of_connection):
	xy = []  
	xy.append("GET " + url_name + " HTTP/1.1")
	xy.append("Host: " + HOST )
	xy.append("User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0")
	#  this can vary
	xy.append("Accept: image/png,image/*;q=0.8,*/*;q=0.5")
	xy.append("Accept-Language: en-us;en;q=0.35")
	xy.append("Accept-Encoding: gzip, deflate")
	xy.append("DNT: 1")
	xy.append("Referer: " + Referer)
	xy.append("Connection: " + state_of_connection)
	return xy



def leaf(elem,obj_tree,counter):
	for x in xrange(counter,len(obj_tree)):
		if(obj_tree[x][2]==elem[0]):
			return False
	return True

def gethost(url_name):
	a = url_name.split('/')
	# print a
	return a[2]

def getfilename(url_name):
	a = url_name.split('/')
	return a[len(a)-1]

# def traverse_object_tree(obj_tree):
# 	count = 0
# 	current_parent_id = 0
# 	prev_parent_id = 0
# 	for elem in obj_tree:
# 		current_parent_id = elem[2]
# 		if(elem[1]!="" ):
# 			if(leaf(elem,obj_tree,count+1) == False):
# 				# if(elem[3]!=""):
# 				if(current_parent_id == prev_parent_id):
# 					if (os.path.exists(gethost(elem[1]))==False):
# 						os.mkdir(gethost(elem[1]))
# 				else:
# 					prev_parent_id = current_parent_id
# 					os.chdir("..")
# 					os.chdir("../" + gethost(elem[3]))
# 					os.makedir(gethost(elem[1]))
# 			if(leaf(elem,obj_tree,count+1) == True):
# 				host = gethost(elem[1])
# 				referer = elem[3]
# 				connect_state = "close"
# 				if(referer==""):
# 					request = generaterequestwithoutref(elem[1],host,connect_state)
# 					data = sendcap(makestr(request),host,80)

# 				else:
# 					request = generaterequest(elem[1],host,referer,connect_state)
# 					data = sendcap(makestr(request),host,80)
# 				if(current_parent_id == prev_parent_id):
# 					f = open(getfilename(elem[1]))
# 					f.write(data)
# 				else:
# 					prev_parent_id = current_parent_id
# 					os.chdir("..")
# 					os.chdir("../" + gethost(elem[3]))
# 					f = open(getfilename(elem[1]))
# 					f.write(data)
# 		count +=1

# lis = [[0, '', 0, ''], [1, u'http://www.vox.com/a/maps-explain-the-middle-east', 0, ''], [2, u'http://ea-cdn.voxmedia.com/production/vox-40-maps/stylesheets/styles-dde012bd.css', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [3, u'http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [4, u'http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min.js', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [5, u'http://ox-d.sbnation.com/w/1.0/jstag', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [6, u'http://ea-cdn.voxmedia.com/production/vox-40-maps/javascripts/top-91c80ccb.js', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [7, u'http://cdn3.vox-cdn.com/assets/4395599/Israeli_territory_1949_to_1967_crop.jpg', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [8, u'http://cdn2.vox-cdn.com/assets/4397359/west_bank_larger_sidebar_crop3.jpg', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [9, u'http://cdn2.vox-cdn.com/assets/4395615/Iran_under_1900s_qajars_wikimedia_crop.jpg', 1, u'http://www.vox.com/a/maps-explain-the-middle-east']]
# traverse_object_tree(lis)
# print leaf(lis[2],lis,2)
a2 = "http://cdn2.vox-cdn.com/assets/4397359/west_bank_larger_sidebar_crop3.jpg"
b2 = gethost(a2)
a = "http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"
b = gethost("http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js")
xy = generaterequest(a,b,"http://www.vox.com/a/maps-explain-the-middle-east","close")
# print makestr(xy)
data = sendcap(makestr(xy),b,80)
data_list = data.split('\n')
# print data
data_content = ""
started = False
for i in xrange(0,len(data_list)):
	# print data_list[i]
	# print "\n"
	if(data_list[i]==""):
		started = True
	print started
	if(started==True):
		data_content += ''.join(data_list[i+1:len(data_list)])
		# print data_content
f = open("logo2.js","w")
f.write(data_content)