import re
import socket
from socket import *
import _thread as thread
import sys
import argparse
import time

# Check_port:
# Checks if the port is a valid port. int() converts val to an integer and checks if the integer is in the range of [1024, 65535].
def check_port(val):
    try:
        value = int(val) # converts val to value
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')
    if value< 1024 or value > 65535:
        raise argparse.ArgumentTypeError('It is not a valid port, must be between [1024,65535]')

    return value


# format:
# format converts the input value to Bytes through if. it checks what the format is and converts to bytes
def format(data, form):
    sum = 0
    if form == 'MB':
        sum =data/1_000_000 # if the file size is MB it calculates to B
    elif form =='KB':
        sum = data/1000  # if the file size is KB it calculates to B
    elif form == 'B':  # if the file size is B it will return B
        sum = data
    return sum # returns the value

# checkIp:
# CheckIp checks if the Ip/input value address is a valid IPv4 address.
# takes in an input string, 'ip'. it returns the the input string as a valid Ip address or  raises an exception if it is not a valid IP address.
# if the ip is 127.0.0.1 it returns 127.0.0.1.. if the ip is not 127.0.0.1 the function uses re.match() if it matches the expression
# pattern "[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}". it matches valid IPv4 in a dot-decimal notation
# bool function converts ip_OK to a bool val. it returns true if there is a match, and false if it doesn't find a match
# if ip_OK means if ip_Ok is true the ip address gets split into four numbers by using split() function.
# and checks if each number is between 0 and 255, 0 included. the input will be returned as an invalid Ip address if it is out of range
# if ip_OK is false the function raises and argumentTypeError.
def checkIp(ip):
    if(ip == '127.0.0.1'):
        return '127.0.0.1'
    ip_check = re.match(r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}", str(ip))
    ip_OK = bool(ip_check)
    try:
        if(ip_OK):
            ip_split=ip.split('.') # splits the number with a dot
            for byte in ip_split:
                if (int(byte)>=0 or int(byte)>255): # if byte is bigger or 0, or bigger then 255 it returns the ip
                    return ip
    except:
        raise argparse.ArgumentTypeError(f'{ip}It is not a valid Ip address!')
    

# checkTime:
# checkTime checks if the input value is bigger than 0. and returns the value.
# int() converts the iput string time to an integer.
# if the input string can't be converted to an integer, valuerror will be raised and return none.
# if it is able to convert to convert to an integer the if statement will check if the input value time
# is less than t0, if its less than 0 an argumentTypeError will be raised with message
# if the value is an integer and greater than 0 the function returns the value of time.
def checkTime(time):
    time = int(time) # convertss time to integer
    try:
        if time < 0: # if time is less then 0 there will come an error message
            raise argparse.ArgumentTypeError('Invalid time value. The time value must be greater than 0 seconds')
    except ValueError:
        return None # returns null
    return time

# check_Interval
# Check_interval checks if the given input value is a positive integer.
# the function int() turns the input string to an integer
# and checks in the if statement if the value interval is less or 0.
# if the value is less or 0 an argumentTypeError will be raised with an empty message.
# if itse greater than 0 the function returns the value of interval in integer.
def check_Interval(interval):
    interval = int(interval)
    if interval <= 0:
        raise argparse.ArgumentTypeError('')
    return interval

# check_Parallel
# Check_parallel checks if the input value is a valid integer for parallel connection.
# takes in string connections and converts it to an integer with the function int().
# it checks if the integer is between 1 or 5, 1 and five included.
# if the integer is eiter 1 or 5 or in between the value of con will be returned.
# if not an argumentTypeError will be raised.
def check_Parallel(connections):
    con = int(connections)
    if 1 <= con <= 5:
        return con
    else:
        raise argparse.ArgumentTypeError(f'interval {connections} is not valid. Has to be between 1 and 5 connections')


# check_Num
# checks if the input value is a valid value for num of b or a num of kb or a nu of mb.
# in the first if statement it checks if the input is None, if it's None it will return None.
# if it's not None it converts it to a string and checks if the string matches a pattern using
# regex with the pattern ([0-9]{1,25})((?:B|KB|MB){1,2}), it can have up to 25 digits, followed by bytes,kilobytes or megabytes.
# re.match() returns none if it doesn't match the pattern, if the pattern matches it returns a match object.
# if it matches the pattern the number and the units  gets extracted using groups().
# and checks if the unit s either kilobytes or megabytes.
# if its KB it multiplies the number by 1000 and returns it as an integer. if its mb it multiplies by 1 000 000 and returns it as an integer.
# if its bytes it returns the input as an integer.
def check_Num(num):
    if num is None: # if the values that comes in is null it returns null
        return None

    num = str(num)
    num_check = re.match(r"([0-9]{1,25})((?:B|KB|MB){1,2})", num)
    num_ok = bool(num_check)

    if num_ok:
        items=num_check.groups()
        print(items)

        if items[1] == 'KB':
            if int(items[0]) % 1 == 0:
                return int(items[0]) * 1000
        elif items[1] == 'MB':
            if int(items[0]) % 1 == 0:
                return int(items[0]) * 1_000_000
        else:
            return int(items[0])


parser = argparse.ArgumentParser(description="positional arguments", epilog="end of help")


#arguments with short name and long name
#NOTE: you must access the value with args.longname, e.g., args.num1
parser.add_argument('-p', '--port', type=check_port, default= '8088')

#how to use boolean values here
parser.add_argument('-s', '--server', action='store_true')

#use append

#offer list of options: you must select from the choices

parser.add_argument('-b', '--bind', type=checkIp, default='127.0.0.1')

parser.add_argument('-f', '--format', type=str, default="MB", choices=('MB,KB,B,mb,kb,b'))

parser.add_argument('-c', '--client', action='store_true')

parser.add_argument('-I', '--serverip',default='127.0.0.1',type=str )

parser.add_argument('-t', '--time', type=checkTime, default=25)

parser.add_argument('-i', '--interval',type=int)

parser.add_argument('-P', '--parallel', type=int, default=1)

parser.add_argument('-n', '--num', type=str)

args = parser.parse_args()


# handleClient
# it handles the client connection to the server:
# connection takes in two arguments connection and addr.
# connection reperesents the client connection andd is a socket object. addr is a tuple that contains the ip address and the port number of the client.
# by using the method connection.recv we are able to receive data from the client in 1000 byte chunks.
# it is then decoded by using the method decode(). the lenght is then added to data by using len().
# it sends 1000 megabit and stops when it reaches the BYE message.
# to be able to reach the BYE  message we do -3 to reach the 3 elements. when it reaches the BYE the loop breaks.
# the time when the loop ends gets stored in endtime.
# the server will then send a message to the client when it's done 'ACK BYE'.
# format() formats the data received from the client so it's readable.
# data is then divided by 1 000 000 to convert it to MB.
# then it calculates the transfer rate of the data in Mps by multiplying data.
# we multiply with 8 because there are 8 bits in a byte.
# it is then divided by the time it took to transfer all the data.
# we find out the time it took by substracting endTime with startTime.
# the function will then print out client's the ip address and port number, the interval the data was received.
# the amount of data received in MB, and the transfer rate in Mps.
# and then it closes the connection by using connection.close().
def handleClient(connection, addr):
    data = 0
    startTime = time.time() # time.time gets the time in seconds

    while True:
        bytes = connection.recv(1000).decode()
        data += len(bytes)
        if bytes[-3:] == 'BYE':
            data -= 3
            break
    endTime = time.time()
    connection.send('ACK:BYE'.encode())


    send_data = format(data, args.format)
    data /= 1_000_000

    rate = data * 8 #conv to megabit
    rate /= endTime - startTime

    print('ID\t\t\tInterval\tReceived\tRate\n')
    print(addr[0],':',addr[1],'\t0.0 -','%.2f'%(endTime-startTime),'\t',int(send_data),'MB\t','%.2f'%rate,'Mps')


    connection.close()

# server
# server creates a TCP/IP server by using sockets.
# a socket is created by using socket(). to specify that the socket will use IPv4 protocol I use AF_INET.
# SOCK_STREAM tells the socket to use TCP protocol.
# we get server_ip when the -b flag is used, and serverport is set to serverPort.
# the try clause tries to bind with the given ip and port by using bind() method.
# if it fails to bind an error  message will print out, the program will then exit using sys.exit.
# by using listen() the socket is set to listen for incoming connections with a maximum backlog of 10 connections.
# the function then prints out a message that tells us the server is listening.
# it then goes into a while loop so it can accept incoming connections.
# when the client are able to connect to the server the method accept() returns a new socket object called connectionSocket.
# connectionSocket represents the connection and the address of the client addr.
# a new thread is then created by using the method thread.start_new thread()  to handle client connection.
# to handle the client connection we have to call handleclient() with connectionSocket and addr.
# it will then loop back to accept() and wait for the next connetion.
# the server is closed when it is done accepting connections, by using clos()

def server():

    serverSocket = socket(AF_INET,SOCK_STREAM)
    server_ip= args.bind
    serverPort = 8088


    #This code tries to bind with a given port and retries until an open port is found

    try:
        serverSocket.bind((server_ip, serverPort)) # Assigns IP and port to the created socket
    except OSError:
        print('failed to bind')
        sys.exit()


    serverSocket.listen(10)
    print('------------------------------------------------------------ \n A simpelperf client connection to server ',server_ip, 'port',serverPort,'\n ------------------------------------------------------------')
    while True:
        connectionSocket, addr = serverSocket.accept()  # accept a connection

        print('Client connected with server_IP port ', addr)
        thread.start_new_thread(handleClient, (connectionSocket,addr))
    serverSocket.close()






def newCon(server_ip,port,client_sd):
    sendData = 0
    data = '0' * 1000
    startTime = time.time()
    endTime = time.time() + args.time
    rate = 0

    checkIp(args.serverip)
    num = check_Num(args.num)
    if num is not None:
        start_Time = time.time()
        while sendData < num:

            client_sd.send(data.encode())
            sendData+=1000
        end_Time= time.time()
        sendTime = end_Time - start_Time


       # print('ID\t\t\tInterval\tSent\tBandwith\n')
        #print(server_ip,":",port,'\t0.0 -', "%.2f" %sendTime,'\t', "%.2f" % (format(sendData,args.format)),"\t", args.format, "%.2f" %((sendData*8/sendTime)/1_000_000) + " Mbps")


    else: # checks if t flag is being used
        start_Time = time.time()
        end_Time = start_Time + args.time
        send_Time = end_Time-start_Time

        if args.interval:
            inter = start_Time+args.interval
            interval_Time = 0
            interdata = 0

            print('ID\t\t\tInterval\tSent\tBandwith\n')

            while time.time() < endTime:
                client_sd.send(data.encode())
                sendData += 1000
                interdata+=1000
                if time.time() >= inter:
                    interval_Time += args.interval
                    send_Time = interval_Time-args.interval

                    numInterval = (interdata*8/args.interval)/1_000_000

                    print(server_ip,':',port,'\t',send_Time,'-',"%.1f" %interval_Time,'\t','%.2f'% format(interdata,args.format) ," ", args.format, int(numInterval),'Mbsp','\n')

                    interdata = 0
                    inter+=args.interval

        else:
            while time.time() < endTime:
                client_sd.send(data.encode())
                sendData += 1000
            #end_Time
    client_sd.send('BYE'.encode()) #sender melding til server

    send_data = format(sendData, args.format)
    sendData /= 1_000_000


    rate = sendData * 8 #conv to megabit
    rate /= endTime - startTime


    print('ID\t\t\tInterval\tSent\tBandwith\n')
    print(server_ip,':',port,'\t0.0 -',"%.2f" %(endTime-startTime),'\t',sendData,'MB\t','%.2f'%rate)

    client_sd.close()
    args.parallel -= 1 # makes it able to start new connections after the x connections.





def client():

    port = args.port
    server_ip = args.serverip
    print('------------------------------------------------------------ \n A simpelperf client connection to server ',server_ip, 'port',port,'\n ------------------------------------------------------------')

    for j in range(args.parallel):
        client_sd = socket(AF_INET, SOCK_STREAM)
        try:
            client_sd.connect((server_ip, port))
        except:
            print('failed to connect server')
            sys.exit()
        print('Client connected with server_Ip port', port, '\n')
        thread.start_new_thread(newCon, (server_ip,port,client_sd))
    while args.parallel > 0:
        time.sleep(10)



if args.client and not args.server:
    print('the server is on', args.server)
    client()


#checking if the server flag is set
if args.server and not args.client:
    print('the server is on ', args.server)
    server()


