import socket
HOST = ''
PORT = 5001
files = []
locations = []
addrs = []
clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, 
#but not stream
clientsock.bind((HOST, PORT))
##Prints ip
print socket.gethostbyname(socket.gethostname())
#main execution loop
while True:
  print "Waiting for packets..."
  buffer = ""
  data=""
#takes in data packets and stores in buffer
  while True:
	data,(address,port) =clientsock.recvfrom(2000)
	addr = (address,port)
	if not data:break
	buffer +=data
	if "END" in buffer:
		break

  words = buffer.split(' ')
  print words
  for i, word in enumerate(words):
	#if it starts with list dend the required message back
	if word == "list":
		clientsock.sendto("list ", addr)
		count =0
		for x in files:
			clientsock.sendto( (x + " found at-> "), addr)
			clientsock.sendto( (locations[count]+" ") , addr)
			count = count+1

		clientsock.sendto( "END", addr)
	#if it starts with share store the required info
	elif word == "share" : 
		p = i+1
		while p < len(words)-1:
			files.append(words[p])
			print("Added " + words[p] +" to the file list")
			locations.append(words[p+1])
			print("It can be found at this directory " + words[p+1]) 
			print address
			addrs.append(address)
			p = p+ 2
	#if it starts with search see if the file is in storage and report findings to user
	elif word == "search" :
		filename = words[i+1]
		found = -1
		print filename
		for x in files:
			if(x == filename):
				found = 0

		if found==0:
			clientsock.sendto("File is in the list of shared files END" , addr)

		else: 
			clientsock.sendto("No file of that name in shared files END" ,addr)
	#if download supply the user with the host info who has the desired data
	elif word == "download" :
		p = 0
		count =0
		for x in files: 
			if (x == word[i+1]):
				p =count

			count = count+1
		
		clientsock.sendto("down "+files[p]+" ",addr)
		clientsock.sendto(locations[p] + " ", addr)
		clientsock.sendto(addrs[p], addr)
		clientsock.sendto(" END", addr)

