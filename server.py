"""
Server side: it simultaneously handle multiple clients
and broadcast when a client new client joins or a client
sends a message.
"""
from socket import *
import _thread as thread
import time
import sys


#this is too keep all the newly joined connections! 
all_client_connections = []

def now():
	"""
	returns the time of day
	"""
	return time.ctime(time.time())

def handleClient(connection, addr):
	"""
	a client handler function 
	"""
	#this is where we broadcast everyone that a new client has joined
	
	### Write your code here ###

	all_client_connections.append(connection)
	broadcast(connection, "Client " + str(addr) + " joined.")

	# append this this to the list for broadcast
	# create a message to inform all other clients 
	# that a new client has just joined.

	### Your code ends here ###

	while True:
		message = connection.recv(2048).decode()
		print (now() + " " +  str(addr) + "#  ", message)
		if (message == "exit" or not message):
			break
		### Write your code here ###
		#broadcast this message to the others

		### Your code ends here ###
	connection.close()
	all_client_connections.remove(connection)

def broadcast(connection, message):
	print ("Broadcasting")
	### Write your code here ###
	for client in all_client_connections:
		if client != connection:
			client.send(message.encode())


	### Your code ends here ###

def main():
	"""
	creates a server socket, listens for new connections,
	and spawns a new thread whenever a new connection join
	"""
	serverPort = 12000
	serverSocket = socket(AF_INET,SOCK_STREAM)
	try:
		# Use the bind function wisely!
		### Write your code here ###

		serverSocket.bind(("", serverPort))

		### Your code ends here ###
		
	except: 
		print("Bind failed. Error : ")
		sys.exit()
	serverSocket.listen(10)
	print ('The server is ready to receive')
	while True:
		### Write your code here ###
		connectionSocket, addr = serverSocket.accept() # accept a connection
		### You code ends here ###
		 
		print('Server connected by ', addr) 
		print('at ', now())
		thread.start_new_thread(handleClient, (connectionSocket,addr)) 
	serverSocket.close()

if __name__ == '__main__':
	main()
