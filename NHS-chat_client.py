# chat_client.py

import sys, socket, select
 
def chat_client():
    if(len(sys.argv) < 4) :
        print ('Usage : python chat_client.py hostname port one_username')
        sys.exit()
    print ("\n\n<<<<<<<=======Welcome to Nasrat Chat Server =======>>>>>>\nSimple messages are broadcasted to everyone in the chat room\n@username: <yourmessage> to send msg for a specific person\n\n")
    host = sys.argv[1]
    port = int(sys.argv[2])
    username= sys.argv[3]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print ('Unable to connect')
        sys.exit()
     
    print ('Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:            
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096).decode()
                if not data :
                    print ('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send((username+"~"+msg).encode()) # send username + message with delimeter

                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())

