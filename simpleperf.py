import re                                                                                                                                                               
import socket                                                                                                                                                           
from socket import *                                                                                                                                                    
import _thread as thread                                                                                                                                                
import sys                                                                                                                                                              
import argparse                                                                                                                                                         
import time                                                                                                                                                             
                                                                                                                                                                        
def check_port(val):                                                                                                                                                    
    try:                                                                                                                                                                
        value = int(val)                                                                                                                                                
    except ValueError:                                                                                                                                                  
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')                                                                                
    if value< 1024 or value > 65535:                                                                                                                                    
        raise argparse.ArgumentTypeError('It is not a valid port, must be between [1024,65535]')                                                                        
                                                                                                                                                                        
    return value                                                                                                                                                        
# allows to use select port number on which the server should                                                                                                           
# listen; the port must be an integer and in the range [1024, 65535],default:8088                                                                                       
                                                                                                                                                                        
                                                                                                                                                                        
def serverConnect(socketAd, port):                                                                                                                                      
    try:                                                                                                                                                                
        socket.bind((socketAd, port))                                                                                                                                   
        socket.listen()                                                                                                                                                 
        print(f"Server listening on {port}")                                                                                                                            
                                                                                                                                                                        
    except socket.error:                                                                                                                                                
        raise argparse.ArgumentTypeError('Couldn`t find the port')                                                                                                      
    socket.close()                                                                                                                                                      
# enable the server mode                                                                                                                                                
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
def server_bind(ip_address):                                                                                                                                            
    try:                                                                                                                                                                
        socket.bind(ip_address)                                                                                                                                         
        print('it is a valid IP address')                                                                                                                               
    except:                                                                                                                                                             
        argparse.ArgumentTypeError('It is not a valid IP address')                                                                                                      
        sys.exit()                                                                                                                                                      
                                                                                                                                                                        
# allows to select the ip address of the server’s interface where the                                                                                                   
# client should connect - use a default value if it’s not                                                                                                               
# provided. It must be in the dotted decimal notation format, e.g. 10.0.0.2                                                                                             
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
def format(data, target):                                                                                                                                               
    sum = 0                                                                                                                                                             
    if target == 'MB':                                                                                                                                                  
        sum =data/1_000_000                                                                                                                                             
    elif target =='KB':                                                                                                                                                 
        sum = data/1000                                                                                                                                                 
    elif target == 'B':                                                                                                                                                 
        sum = data                                                                                                                                                      
    return sum                                                                                                                                                          
                                                                                                                                                                        
# allows you to choose the format of the summary of results - it should be                                                                                              
# either in B, KB or MB,default=MB)                                                                                                                                     
                                                                                                                                                                        
def clientConnect(server_ip,port):                                                                                                                                      
                                                                                                                                                                        
    try:                                                                                                                                                                
        socket.connect((server_ip,port))                                                                                                                                
        print('connected to server at ',server_ip,' ',port)                                                                                                             
                                                                                                                                                                        
    except socket.error:                                                                                                                                                
        raise argparse.ArgumentTypeError('Couldn`t connect to the server')                                                                                              
    socket.close()                                                                                                                                                      
                                                                                                                                                                        
def Checkip(val):                                                                                                                                                       
    if(val == '127.0.0.1'):                                                                                                                                             
        return '127.0.0.1'                                                                                                                                              
    ip_check = re.match(r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}", str(val))                                                                                       
    ip_OK = bool(ip_check)                                                                                                                                              
    if(ip_OK):                                                                                                                                                          
        ip_split=val.split('.')                                                                                                                                         
        for byte in ip_split:                                                                                                                                           
            if (int(byte)<0 or int(byte)>255):                                                                                                                          
                return val                                                                                                                                              
                                                                                                                                                                        
# selects the ip address of the server - use a default value if it’s not                                                                                                
# provided. It must be in the dotted decimal notation format,e.g. 10.0.0.2                                                                                              
                                                                                                                                                                        
                                                                                                                                                                        
def checkTime(time):                                                                                                                                                    
    time = int(time)                                                                                                                                                    
    try:                                                                                                                                                                
        if time < 0:                                                                                                                                                    
            raise argparse.ArgumentTypeError('Invalid time value. The time value must be greater than 0 seconds')                                                       
    except ValueError:                                                                                                                                                  
        return None                                                                                                                                                     
    return time                                                                                                                                                         
        # the total duration in seconds for which data should be generated, also sent to                                                                                
# the server (if it is set with -t flag at the                                                                                                                          
# client side) and must be > 0. NOTE If you do not use -t flag, your experiment should run for 25 seconds                                                               
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
def checkInterval(interval):                                                                                                                                            
    interval = int(interval)                                                                                                                                            
    if interval <= 0:                                                                                                                                                   
        raise argparse.ArgumentTypeError('')                                                                                                                            
    return interval                                                                                                                                                     
                                                                                                                                                                        
# hvor mye som data som sendes innen de sekundene(intervaller)                                                                                                          
#print statistics per z second                                                                                                                                          
                                                                                                                                                                        
def parallel(connections):                                                                                                                                              
    connection = connections                                                                                                                                            
    num = input(f'Enter number of connections (1-5, default {connection}):')                                                                                            
    if num.isnumeric():                                                                                                                                                 
        num = int (num)                                                                                                                                                 
        if 1 <= num <=5:                                                                                                                                                
            connection = num                                                                                                                                            
# hvor mange tråder klienten skal ha threading. parallel er tråder                                                                                                      
#creates parallel connections to connect to the server and send data - it must be 1 and the max value should be 5 - default:1                                           
def num():                                                                                                                                                              
    print('hei')                                                                                                                                                        
# hvor lenge testen skal vare hvor mye data som skal sendes                                                                                                             
#transfer number of bytes specfied by -n flag, it should be either in B, KB or MB                                                                                       
                                                                                                                                                                        
                                                                                                                                                                        
parser = argparse.ArgumentParser(description="positional arguments", epilog="end of help")                                                                              
                                                                                                                                                                        
                                                                                                                                                                        
#arguments with short name and long name                                                                                                                                
#NOTE: you must access the value with args.longname, e.g., args.num1                                                                                                    
parser.add_argument('-p', '--port', type=check_port, default= '8080')                                                                                                   
                                                                                                                                                                        
#how to use boolean values here                                                                                                                                         
parser.add_argument('-s', '--server', action='store_true')                                                                                                              
                                                                                                                                                                        
#use append                                                                                                                                                             
                                                                                                                                                                        
#offer list of options: you must select from the choices                                                                                                                
                                                                                                                                                                        
parser.add_argument('-b', '--bind', type=int, default='10.0.0.2')                                                                                                       
                                                                                                                                                                        
parser.add_argument('-f', '--format', type=str, default="MB", choices=('MB,KB,B,mb,kb,b'))                                                                              
                                                                                                                                                                        
parser.add_argument('-c', '--client', action='store_true')                                                                                                              
                                                                                                                                                                        
parser.add_argument('-I', '--serverip', type=str)                                                                                                                       
                                                                                                                                                                        
parser.add_argument('-t', '--time', type=int)                                                                                                                           
                                                                                                                                                                        
parser.add_argument('-i', '--interval',type=int)                                                                                                                        
                                                                                                                                                                        
parser.add_argument('-P', '--parallel', type=int)                                                                                                                       
                                                                                                                                                                        
parser.add_argument('-n','--num',type=str)                                                                                                                              
                                                                                                                                                                        
args = parser.parse_args()                                                                                                                                              
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
#ports                                                                                                                                                                  
                                                                                                                                                                        
def handleClient(connection, addr):                                                                                                                                     
    data = 0                                                                                                                                                            
    startTime = time.time()                                                                                                                                             
                                                                                                                                                                        
    while True:                                                                                                                                                         
        bytes = connection.recv(1000).decode()                                                                                                                          
        data += len(bytes)                                                                                                                                              
        if bytes[-3:] == 'bye':                                                                                                                                         
            data -= 3                                                                                                                                                   
            break                                                                                                                                                       
    endTime = time.time()                                                                                                                                               
    connection.send('bye'.encode())                                                                                                                                     
                                                                                                                                                                        
                                                                                                                                                                        
    send_data = format(data, args.format)                                                                                                                               
    data /= 1_000_000                                                                                                                                                   
                                                                                                                                                                        
    rate = data * 8 #conv to megabit                                                                                                                                    
    rate /= endTime - startTime                                                                                                                                         
                                                                                                                                                                        
    print('ID\t\t\tInterval\tReceived\tRate\n')                                                                                                                         
    print(addr[0],':',addr[1],'\t0.0 -','%.2f'%(endTime-startTime),'\t',int(send_data),'MB\t','%.2f'%rate)                                                              
                                                                                                                                                                        
    connection.close()                                                                                                                                                  
                                                                                                                                                                        
                                                                                                                                                                        
def server():                                                                                                                                                           
                                                                                                                                                                        
    serverSocket = socket(AF_INET,SOCK_STREAM)                                                                                                                          
    server_ip= "127.0.0.1"                                                                                                                                              
    serverPort = 8088                                                                                                                                                   
                                                                                                                                                                        
                                                                                                                                                                        
    #This code tries to bind with a given port and retries until an open port is found                                                                                  
                                                                                                                                                                        
    try:                                                                                                                                                                
        serverSocket.bind((server_ip, serverPort)) # Assigns IP and port to the created socket                                                                          
    except OSError:                                                                                                                                                     
        print('failed to bind')                                                                                                                                         
        sys.exit()                                                                                                                                                      
                                                                                                                                                                        
                                                                                                                                                                        
    serverSocket.listen(10)                                                                                                                                             
    print('--------------------------------------------- A simpelperf client connection to server ',server_ip, 'port',serverPort,'\-------------------------------------')
    while True:                                                                                                                                                         
        connectionSocket, addr = serverSocket.accept()  # accept a connection                                                                                           
                                                                                                                                                                        
        print('Client connected with server_IP port ', addr)                                                                                                            
        thread.start_new_thread(handleClient, (connectionSocket,addr))                                                                                                  
    serverSocket.close()                                                                                                                                                
                                                                                                                                                                        
def newCon(server_ip,port,client_sd):                                                                                                                                   
    sendData = 0                                                                                                                                                        
    data = '0' * 1000                                                                                                                                                   
    startTime = time.time()                                                                                                                                             
    endTime = time.time() + 25                                                                                                                                          
                                                                                                                                                                        
    while time.time() < endTime:                                                                                                                                        
        client_sd.send(data.encode())                                                                                                                                   
        sendData += 1000                                                                                                                                                
                                                                                                                                                                        
    client_sd.send('bye'.encode()) #sender melding til server                                                                                                           
                                                                                                                                                                        
    send_data = format(sendData, args.format)                                                                                                                           
    sendData /= 1_000_000                                                                                                                                               
                                                                                                                                                                        
    rate = sendData * 8 #conv to megabit                                                                                                                                
    rate /= endTime - startTime                                                                                                                                         
                                                                                                                                                                        
    print('ID\t\t\tInterval\tSent\tBandwith\n')                                                                                                                         
    print(server_ip,':',port,'\t0.0 -',endTime-startTime,'\t',int(send_data),'MB\t','%.2f'%rate)                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
def client():                                                                                                                                                           
    client_sd = socket(AF_INET, SOCK_STREAM)                                                                                                                            
    server_ip = "127.0.0.1"                                                                                                                                             
    port = 8088                                                                                                                                                         
                                                                                                                                                                        
                                                                                                                                                                        
    print('--------------------------------------------- A simpleperf server is listening on port',port,'\---------------------------------------------')               
    try:                                                                                                                                                                
        client_sd.connect((server_ip, port))                                                                                                                            
    except:                                                                                                                                                             
        print('failed to connect server')                                                                                                                               
        sys.exit()                                                                                                                                                      
                                                                                                                                                                        
    print('Client connected with server_Ip port', port, '\n')                                                                                                           
                                                                                                                                                                        
    newCon(server_ip,port,client_sd)                                                                                                                                    
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
if args.client and not args.server:                                                                                                                                     
    print('the server is on', args.server)                                                                                                                              
    client()                                                                                                                                                            
                                                                                                                                                                        
                                                                                                                                                                        
#checking if the server flag is set                                                                                                                                     
if args.server and not args.client:                                                                                                                                     
    print('the server is on ', args.server)                                                                                                                             
    server()                                                                                                                                                            
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        
# When you run in server mode, simpleperf will receive TCP packets and track                                                                                            
# how much data was received during from the connected clients; it will calculate                                                                                       
# and display the bandwidth based on how much data was received and how much                                                                                            
# time elapsed during the connection. A server should read data in chunks of 1000                                                                                       
# bytes. For the sake of simplcity, assume 1 KB = 1000 Bytes, and 1 MB = 1000                                                                                           
# KB.    
# message.txt
# 47 KB                                                                                                                                                               
