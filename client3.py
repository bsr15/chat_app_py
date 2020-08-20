#client code

import sys
import socket
import select

HOST = "localhost"
PORT  = 1502

username = raw_input("Enter a username: ")  # for enter user name

def chat_client():
	host = HOST
	port = PORT
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	
	try :
		s.connect((host, port))

	except:
		print 'Unable to connect'
		sys.exit()

	print 'Connected to server\n You can start sending messages'
	sys.stdout.write('[' + username + '] '); sys.stdout.flush()
	
	s.send(username);

	while True:
		socket_list = [sys.stdin, s]
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
		
		for sock in ready_to_read:
			if sock == s:
				data = sock.recv(4096)
				if not data :
					print '\nDisconnected from chat server'

					sys.exit()

				else :
					sys.stdout.write(data)
                    			sys.stdout.write('[' + username + '] '); sys.stdout.flush()
			else:
				msg = sys.stdin.readline()
				s.send(msg)
				sys.stdout.write('[' + username + ']'); sys.stdout.flush()

if __name__ == "__main__":
	sys.exit(chat_client())   
				










