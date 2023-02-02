import socket
import struct
import sys

message = 'Thanks For Joining The Chat Room'
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
# sock.settimeout(15)

try:

    # Send data to the multicast group
    print(f'sending {message}')
    if sent := sock.sendto(bytes(message.encode()), multicast_group):
        print("already send welcome Message")

    # Look for responses from all recipients
    while True:
        print('waiting to receive')
        try:
            data, server = sock.recvfrom(1024)
        except socket.timeout:
            print('timed out, no more responses')
            break
        else:
            print(f'received "{data}" from {server}')
            sock.sendto(bytes(data), multicast_group)

finally:
    print('closing socket')
    sock.close()
