import os
import socket
import sys
import time
import argparse

# This program takes 3 arguments: IP address, path of the large file received to be saved, size of data unit
# To run the program: python3 server -i localhost -p ./output.txt -s 1024

def main():
    # Create an argument parser to parse the 3 arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip","-i", required=True, help="Host IP address", type=str)
    parser.add_argument("--path","-p", required=True, help="Path of file to be saved", type=str)
    parser.add_argument("--size","-s", required=True, help="Size of data unit", type=int)
    args = parser.parse_args()

    # Initialized a server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = args.ip
    port = 4204
    addr = (host, port)
    print("Starting up on {} on port number {}".format(host, port))
    server.bind(addr)

    # Initialize batch size to receive data
    data_units = []
    batch_size = 1
    curr_ind = 0
    # Receiving data from client
    while True:
        recv_data(args, server, addr, data_units, batch_size, curr_ind)
        # check if the last message received is "EndOfMessage"
        if data_units[-1] == "EndOfMessage":
            break
        curr_ind += batch_size
        batch_size += 1
    
    # Write received data into the output file
    with open(args.path, 'a') as f:
        for du in data_units:
            f.write(du)
        print("Message written to {}.".format(args.path))
        f.close()
    
    exit(0)

def recv_data(args, server, addr, data_units, batch_size, curr_ind):
    i = 0
    while i < batch_size:
        data, addr = server.recvfrom(args.size)
        data = data.decode("utf-8")
        data_units[curr_ind+i] = data
        i += 1
    # Send ACK after receiving the whole batch
    print("Received {} DUs from the client".format(batch_size))
    msg = "ACK".encode("utf-8")
    server.sendto(msg, addr)
    print("ACK sent to client after receiving {} DUs".format(batch_size))


if __name__ == "__main__":
    main()