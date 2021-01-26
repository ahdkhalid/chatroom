# chatroom

A simple chat room developed long time ago in python. 
Server hosts the chatroom
Multiple clients can connect to server and can send messages to chat room and they can also send messages indivitually. 

## Usage
Run the server: 
```
python3 NHS_chat_server.py
```
Server will output the port address

client:
Client should choose a unique username for him/herself
python3 NHS_chat_client.py <server_ip> <port> <your_username>

e.g:
```
python3 NHS_chat_client.py 127.0.0.1 9008 ahdkhalid
```
Clients can start chatting in a shared room: 
To send indivitual msges, use @username:<your message>


The chatroom may have bugs. Will be updated soon. 
