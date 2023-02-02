import socket
import struct
import sys
from threading import Thread, Lock
addr = None
address_lock = Lock()


def receive(sock):
    # Receive/respond loop
    global addr
    while True:
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)
        address_lock.acquire()
        addr = address
        address_lock.release()

        if not data:
            break

        print(f'received {len(data)} bytes from {address}')
        print(data)
    sock.close()


def send(sock):
    global addr
    while True:
        msg = input('>>')
        if not msg or not addr:
            print("No msg or address to send to")
            break
        sock.sendto(bytes(msg.encode()), addr)
    sock.close()


def main():

    multicast_group = '224.3.29.71'
    server_address = ('', 10000)

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the server address
    sock.bind(server_address)

    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    t1 = Thread(target=receive, args=(sock,))
    t2 = Thread(target=send, args=(sock,))
    t1.start()

    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
