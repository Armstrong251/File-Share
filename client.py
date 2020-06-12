from socket import *
import select,sys,socket


HOST = socket.gethostbyname(socket.gethostname())    # The remote host
PORT = 5001           # The same port as used by the server
SPORT = 5006
MYIP = '127.0.0.1'#if the ip's of the 2 clients are the same issues will arrise
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not 
clientsoc= socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram,
recvsoc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram,


#stream
inputs = [s , sys.stdin, clientsoc]
#options for the user
print "To share a file type : 'Share filename file location ...'"
print "To list all files on server type: 'List'"
print "To search for a file type: 'search filename' "
print "To download a file type: 'download filename' "
#main loop to handle everything
print HOST
while inputs:
	readable, writable, exceptional = select.select(inputs, inputs, inputs)
	for socket in readable:
		buffer = ""
		data = ""
		if socket is s or socket is clientsoc:
			#loops to receive packets and stor in a buffer
			if socket is s:
				while True:
					data += s.recv(2000)
					if not data: break
					buffer +=data
					if "END" in buffer:
						break
				data2 = data.split()
			elif socket is clientsoc:
				while True:
					data += clientsoc.recv(2000)
					if not data: break
					buffer +=data
					if "END" in buffer:
						break
				data2 = data.split()
			#handles if the user is requesting to download a file
			if data2[0] == "down" :
				recvsoc.bind((MYIP,SPORT))
				clientsoc.sendto("request " + MYIP +" " + data2[2] + " END",(data2[3],SPORT))
				f =open(data2[2],'wb')
				data,addr = recvsoc.recvfrom(2000)

				try:
					while(data):
						f.write(data)
						recvsoc.settimeout(2)
						data,addr = recvsoc.recvfrom(2000)
				except timeout:
					f.close()
					print"file downloaded"
					recvsoc.close()



			#handles when the user asks for the list of avaliable files
			elif data2[0] == "list":
				count=1
				for x in data2:
					if count <= len(data2)-3:
						print data2[count] +" " + data2[count+1] + " " +data2[count+2] +" " + data2[count+3]

					count=count+4
			#handles when the host is being asked for a file to download 
			elif data2[0] == "request" :
				print "DATA REQUESTED"
				f = open(data2[2], 'rb')
				stuff = f.read(2000)
				while(stuff):
					if(clientsoc.sendto(stuff,(data2[1],SPORT))):
						print "sending files "
						stuff = f.read(2000)
				
				f.close()
				print "DONE SENDING"

			else:
				msg=""
				count=0
				for x in data2:
					if count < len(data2)-1:
						msg = msg+" "+data2[count]
					count=count+1
				print msg


		#This portion of the loop handles console inputs 
		elif socket is sys.stdin:
			command = raw_input()
			words = command.split()
			for i, word in enumerate(words):#Users options 
				if words[i] == "Share":
					p = i+1
					msg = ""
					while p < len(words):
						msg = msg + " " + words[p]
						p = p+1

					s.sendto(("share" + msg + " END"), (HOST ,PORT))
					clientsoc.bind((MYIP,SPORT))
				elif words[i] == "List":
					s.sendto(("list END"), (HOST ,PORT))

				elif words[i] == "search":
					s.sendto(("search "+words[1] + " END"),(HOST,PORT))

				elif words[i] == "download": 
					s.sendto(("download "+ words[1] + " END"),(HOST,PORT))


clientsoc.close()
s.close()

