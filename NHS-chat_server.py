# chat_server.py
 
import sys, socket, select,datetime, os

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 14000
PORT = 9008
database = []
logdir="chat_log/" #storage dir for all chatlogs
if not os.path.exists(logdir):
    os.makedirs(logdir)

noww = datetime.datetime.now()
chatlogname=logdir+str(noww.year)+"-"+str(noww.month)+"-"+str(noww.day)
#add username and thier id to db
def adduser(username,userid):
    global database
    exist=0
    for ar in database:
        if ar[0] == username:
            exist=1
    if not exist:
        database.append((username , userid)) #normal addition

def searchreceiver(username): # return userid by providing username
    for ar in database:
        if ar [0]== username:
            return ar[1]
def searchname(userid): # find name by providing userid
    for ar in database:
        if ar[1] == userid:
            return ar[0]


def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
    server_ip =socket.gethostbyname(socket.gethostname())
    print ("Chat server started on port " + str(PORT))
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                new_client, addr = server_socket.accept()
                SOCKET_LIST.append(new_client) #add connection to list of connections
                print ("Client (%s, %s) connected" % addr)
                broadcast(server_socket, new_client,0, "[%s:%s] entered our chatting room\n" % addr) #broadcast to all 0 means to all
            
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER).decode()
                    if data:
                        sender,payload=data.split("~") #split sender and message
                        receiver="all"
                        if payload[0] =="@": #if message is sent to specific person - split the reciever and the message
                            strindex=payload.find(" ") # first word is the @username - this find the index to first space
                            receiver=payload[:strindex].replace("@","") # take the whole word up to first space and remove @
                            payload=payload[strindex:] # get the message without the @username
                        adduser(sender,sock.getpeername()[1]) # add user to db
                        target = open(str(chatlogname), 'a') # open file for append
                        target.write(str(noww)+"="+data)# write data and the time at the beggening of it
                        target.close()
                        if receiver=="all": # send to all except the sender
                            broadcast(server_socket, sock,0, "\r" + '[' + sender + '] ' + payload)
                        else: #send to specific person
                            singlecast(server_socket, sock,receiver, "\r" + '[' + sender + '] ' + payload)
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, 0,"Client (%s, %s) went offline\n" % addr)

                # exception
                except:
                    broadcast(server_socket, sock,1,"\n<<<<<<<<===============BUZZZZZZZ==============>>>>>>>>\n======>>>>>>>"+str(searchname(sock.getpeername()[1]))+"  left the chat:<<<<<<<=======\n")
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock,to_sender_also, message):
    for socket in SOCKET_LIST:
        # send the message only to peer and also itself if to_sender_also is true
        if socket != server_socket and( ( socket == sock and to_sender_also == 1) or socket != sock):
            try:
                socket.send(message.encode())
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


def singlecast(server_socket, sock, receiver,message):
    for socket in SOCKET_LIST:

        # send the message only to peer
        if socket != server_socket and socket.getpeername()[1] ==searchreceiver(receiver):
            try:
                socket.send(message.encode())
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


if __name__ == "__main__":

    sys.exit(chat_server())
         
