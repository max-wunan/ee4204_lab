import os
import socket
import sys
import time
import argparse

# This program takes 3 arguments: IP address, path of the large file to be sent, size of data unit
# To run the program: python3 client -i localhost -p ./input.txt -s 1024

def main():
    # Create an argument parser to parse the 3 arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip","-i", required=True, help="Host IP address", type=str)
    parser.add_argument("--path","-p", required=True, help="Path of file to be sent", type=str)
    parser.add_argument("--size","-s", required=True, help="Size of data unit", type=int)
    args = parser.parse_args()

    # Initialized a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = args.ip
    port = 5000
    addr = (host, port)
    # ser_addr = (host, 4204)
    # print("Starting up on {} on port number {}".format(host, port))
    # client.bind(addr)

    # Read from the large file chunks by chunks and store in a list
    data_units = []
    with open(args.path, 'r') as f:
        while True:
            data = f.read(args.size)
            if not data:
                break
            data_units.append(data)
        f.close()
    print("Finished reading from file.")

    # Initialize batch size and send the data
    batch_size = 2
    curr_ind = 0
    initial_time = time.time()
    while curr_ind <= len(data_units):
        #send_data(args, client, addr, data_units, batch_size, curr_ind)
        i = 0
        while i < batch_size:
            # When all the data has been sent, pad the current batch with "EndOfMessage" string
            if curr_ind + i >= len(data_units):
                msg = "EndOfMessage".encode("utf-8")
            else:  
                msg = data_units[curr_ind+i].encode("utf-8")
            client.sendto(msg, addr)
            i += 1
        # Wait for ACK after sending the batch of DU
        print("Sent a batch of {} DUs to the server".format(batch_size))
        data, addr = client.recvfrom(1024)
        data = data.decode("utf-8")
        if data == "ACK":
            print("Received ACK from server.")
        curr_ind += batch_size
    print("Message transmitting completed.")
    final_time = time.time()
    transfer_time = final_time - initial_time
    data_size = len(data_units) * args.size
    throughput = data_size / float(transfer_time)
    print('Sent {} bytes in {:.2f} seconds ({:.2f} Mbps)'.format(data_size, transfer_time, throughput / 1e6))
    exit(0)


if __name__ == "__main__":
    main()

