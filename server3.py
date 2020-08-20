#server programme
import sys
import socket
import select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 1502
USERNAMES = {} # datastructure for names

def chat_server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)

	SOCKET_LIST.append(server_socket)

	print "Chat server started on port " + str(PORT)

	my_dict = {}
	list_of_client = []
	while True:
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

		for sock in ready_to_read:
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
			
				SOCKET_LIST.append(sockfd)
				username = sockfd.recv(1024) #for name 
				print "Client (%s, %s) connected clientName :" % addr,username
				USERNAMES[sockfd.getpeername()] = username #user name
						
				list_of_client.append(username)
			
			 	broadcast(server_socket, sockfd, ": %s entered our chatting room\n" % username)
				
				my_dict1 = dict()
				key = sockfd
				value = username
				my_dict1[key] = value
				my_dict.update(my_dict1)
			else :
				data = sock.recv(RECV_BUFFER)

                                if data.split(" ",2)[0] == "active":
                                        send_msg(server_socket, sock, " : %s are Active select to chat\n" % list_of_client)

                                elif data.split("\n")[0] == "exit":
                                        if sock in SOCKET_LIST:
                                                SOCKET_LIST.remove(sock)
                                        broadcast(server_socket, sock,"Client (%s, %s) is offline\n" % addr)

                                elif data.split(" ",3)[0] == "all" :
					data1 = data.strip("all")
                                        broadcast(server_socket, sock, "\r" + '' + str(USERNAMES[sock.getpeername()]) + ': ' + data1)
				elif data.split(" ",3)[0] == "to":
					
					for key in my_dict :
						if data.split(" ",3)[1] == my_dict[key] :
							sock1 = key
							data1 = " ".join(data.split(" ")[2:]) #use for remove the to username in receiver string
							send_msg(server_socket, sock1, "\r" + '' + str(USERNAMES[sock.getpeername()]) + ': ' + data1)

				else :
					send_msg(server_socket, sock, "please start msg with'all or to'\n")				
					

	server_socket.close()
def broadcast (server_socket, sock, message):
	 for socket in SOCKET_LIST:
		 if socket != server_socket and socket != sock :
			try:
				socket.send(message)
			except:
				socket.close()	
				if socket in SOCKET_LIST:
					 SOCKET_LIST.remove(socket)

def send_msg(server_socket, sock, message):
	sock.send(message)


if __name__ == "__main__":
	 sys.exit(chat_server())


