This is a simple chat app which uses socket's multicast to send message to different connected clients in the multicast group.The
client also uses threads for sending and receiving messages

To run,first run the client(s), so that it may receive first the address of the server sending the message first so that it may reuse the address in sending operatons