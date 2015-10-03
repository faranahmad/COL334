# TODO: Add Exception
# TODO: Add proxy issues
# TODO: Add threading

import socket
import socks
import os
import thread

# os.environ["https_proxy"]="https://10.10.78.22:3128"
# socket.socket = socks.socksocket
# HOST = "ea-cdn.voxmedia.com"   
# PORT = 80  
#create paket-string from list

current_no_tcp = 0
list_of_thread = {}
thread_socket = {}
count = 0
current_parent_id = 0
prev_parent_id = 0

def makestr(s):
	rs = ""
	rs = "\r\n".join(s)
	rs+="\r\n"
	rs+="\r\n"
	return rs

def sendcapthread(thread_name,s,sdata,HOST,PORT,connect_state):
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
	list_of_thread[thread_name] +=1
	if(connect_state == 0):
		current_no_tcp-=1
		s.close()
	return recvd

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
	# xy.append("Accept-Encoding: gzip, deflate")
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
	# xy.append("Accept-Encoding: null")
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

def getcontent(data):
	datalist = data.split('\r\n\r\n')
	content = datalist[1]
	return content

def download_each_item(thread_name,socket,elem,obj_tree,connect_s):
	current_parent_id = elem[2]
	if(elem[1]!="" ):
		if(leaf(elem,obj_tree,count+1) == False):
			if(current_parent_id == prev_parent_id):
				if (os.path.exists(gethost(elem[1]))==False):
					os.mkdir(gethost(elem[1]))
			else:
				prev_parent_id = current_parent_id
				os.chdir("..")
				if(os.path.exists(gethost(elem[3]))==False):
					os.makedir(gethost(elem[3]))
				os.chdir(gethost(elem[3]))
				os.makedir(gethost(elem[1]))
			os.chdir(gethost(elem[1]))
			host = gethost(elem[1])
			connect_state = "close"
			if(elem[3]==""):
				request = generaterequestwithoutref(elem[1],host,connect_state)
				data = sendcapthread(thread_name,socket,makestr(request),host,80,connect_s)

			else:
				request = generaterequest(elem[1],host,referer,connect_state)
				data = sendcapthread(thread_name,socket,makestr(request),host,80,connect_s)
			f = open(gethost(elem[1]) + ".htm",'w')
			f.write(getcontent(data))
							
		if(leaf(elem,obj_tree,count+1) == True):
			host = gethost(elem[1])
			referer = elem[3]
			connect_state = "close"
			if(referer==""):
				request = generaterequestwithoutref(elem[1],host,connect_state)
				data = sendcapthread(thread_name,socket,makestr(request),host,80,connect_s)

			else:
				request = generaterequest(elem[1],host,referer,connect_state)
				data = sendcapthread(thread_name,socket,makestr(request),host,80,connect_s)
				if(current_parent_id!=prev_parent_id):
					prev_parent_id = current_parent_id
					os.chdir("..")
					if(os.path.exists(gethost(elem[3]))==False):	
						os.mkdir(gethost(elem[3]))
					os.chdir(gethost(elem[3]))
					print getfilename(elem[1])
			f = open(getfilename(elem[1]),'wb')
			f.write(getcontent(data))
	print ("Count done: " + str(count))
	count +=1

def traverse_object_tree(obj_tree):
	count = 0
	current_parent_id = 0
	prev_parent_id = 0
	for elem in obj_tree:
		current_parent_id = elem[2]
		if(elem[1]!="" ):
			if(leaf(elem,obj_tree,count+1) == False):
				if(current_parent_id == prev_parent_id):
					if (os.path.exists(gethost(elem[1]))==False):
						os.mkdir(gethost(elem[1]))
				else:
					prev_parent_id = current_parent_id
					os.chdir("..")
					if(os.path.exists(gethost(elem[3]))==False):
						os.makedir(gethost(elem[3]))
					os.chdir(gethost(elem[3]))
					os.makedir(gethost(elem[1]))
				os.chdir(gethost(elem[1]))
				host = gethost(elem[1])
				connect_state = "close"
				if(elem[3]==""):
					request = generaterequestwithoutref(elem[1],host,connect_state)
					data = sendcap(makestr(request),host,80)

				else:
					request = generaterequest(elem[1],host,referer,connect_state)
					data = sendcap(makestr(request),host,80)
				f = open(gethost(elem[1]) + ".htm",'w')
				f.write(getcontent(data))
								
			if(leaf(elem,obj_tree,count+1) == True):
				host = gethost(elem[1])
				referer = elem[3]
				connect_state = "close"
				if(referer==""):
					request = generaterequestwithoutref(elem[1],host,connect_state)
					data = sendcap(makestr(request),host,80)

				else:
					request = generaterequest(elem[1],host,referer,connect_state)
					data = sendcap(makestr(request),host,80)
					if(current_parent_id!=prev_parent_id):
						prev_parent_id = current_parent_id
						os.chdir("..")
						if(os.path.exists(gethost(elem[3]))==False):	
							os.mkdir(gethost(elem[3]))
						os.chdir(gethost(elem[3]))
						print getfilename(elem[1])
				f = open(getfilename(elem[1]),'wb')
				f.write(getcontent(data))
		print ("Count done: " + str(count))
		count +=1


def threaded_downloader(obj_tree,max_tcp,object_per_tcp):
	current_no_tcp = 0
	i = 1
	
	for counter in xrange(0,len(obj_tree)):
		if(current_no_tcp < max_tcp):
			#  create new socket
			print "no of tcp's are less than maximum no. of tcp"
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect()
			thread.start_new_thread( download_each_item, ("Thread-"+str(i), s,obj_tree[counter], obj_tree,1,))
			list_of_thread["Thread-"+str(i)] = 1
			thread_socket["Thread-"+str(i)] = s
			current_no_tcp +=1
			i+=1
			counter+=1
   		else:
   			found_key = ''
   			found = False
   			for key,value in list_of_thread.iteritems():
   				if(value<object_per_tcp):
   					found = True
   					found_key = key
   					break

   			if found == False:
   				counter = counter
   			# 	# wait for some socket to close
   			# 		# do nothing
   			# 	#  create new socket

   			# 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   			# 	thread.start_new_thread(download_each_item,("Thread-"+str(i),s,elem,obj_tree,1,))
   			# 	list_of_thread["Thread-"+str(i)] = 1
   			# 	thread_socket["Thread-"+str(i)] = s
   			# 	current_no_tcp +=1
   			# 	i+=1
   			else:
   				socket = thread_socket[found_key]
   				if(list_of_thread[found_key]==object_per_tcp):
   					download_each_item(found_key,socket,elem,obj_tree[counter],0)
   				else:
   					download_each_item(found_key,socket,elem,obj_tree[counter],1)
   				counter+=1




################## Downloader testing without threadng #######################
lis = [[0, '', 0, ''], [1, u'http://www.vox.com/a/maps-explain-the-middle-east', 0, ''], [2, u'http://ea-cdn.voxmedia.com/production/vox-40-maps/stylesheets/styles-dde012bd.css', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [3, u'http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [4, u'http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min.js', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [5, u'http://ox-d.sbnation.com/w/1.0/jstag', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [6, u'http://ea-cdn.voxmedia.com/production/vox-40-maps/javascripts/top-91c80ccb.js', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [7, u'http://cdn3.vox-cdn.com/assets/4395599/Israeli_territory_1949_to_1967_crop.jpg', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [8, u'http://cdn2.vox-cdn.com/assets/4397359/west_bank_larger_sidebar_crop3.jpg', 1, u'http://www.vox.com/a/maps-explain-the-middle-east'], [9, u'http://cdn2.vox-cdn.com/assets/4395615/Iran_under_1900s_qajars_wikimedia_crop.jpg', 1, u'http://www.vox.com/a/maps-explain-the-middle-east']]
threaded_downloader(lis,4,1)
# traverse_object_tree(lis)

# print leaf(lis[2],lis,2)

################# Testing of single file download ########################

# a2 = "http://cdn2.vox-cdn.com/assets/4397359/west_bank_larger_sidebar_crop3.jpg"
# b2 = gethost(a2)
# a = "http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"
# b = gethost("http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js")
# a3 = 'http://ea-cdn.voxmedia.com/production/vox-40-maps/stylesheets/styles-dde012bd.css'
# b3 = gethost(a3)
# a4 = 'http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min.js'
# b4 = gethost(a4)
# xy = generaterequest(a3,b3,"http://www.vox.com/a/maps-explain-the-middle-east","close")
# data = sendcap(makestr(xy),b3,80)
# datalist = data.split('\r\n\r\n')
# content = datalist[1]
# headers = datalist[0]
# print headers
# f = open(getfilename(a3),"wb")
# f.write(content)

# # print makestr(xy)
# data_list = data.split('\n')
# print data
# data_content = ""
# started = False
# for i in xrange(0,len(data_list)):
# 	# print data_list[i]
# 	# print "\n"
# 	if(data_list[i]==""):
# 		started = True
# 	print started
# 	if(started==True):
# 		data_content += ''.join(data_list[i+1:len(data_list)])
# print data_content