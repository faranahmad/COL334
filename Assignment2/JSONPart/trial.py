s = "b\nrc\n\ncd\nef"
data_list = s.split("\n")
data_content = ""
started = False
for i in xrange(0,len(data_list)):
    # print data_list[i]
    # print "\n"
    if(data_list[i]==""):
        started = True
    # print started
    if(started==True):
        print "here"
        data_content += ''.join(data_list[i+1:len(data_list)])
        
f = open("logo2.js","wb")
f.write(data_content)