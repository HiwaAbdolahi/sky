import socket
import argparse
import time
import threading


def run_server(args):
    # Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    bind_ip = args.bind if args.bind else "0.0.0.0"
    bind_port = args.port if args.port else 8088

    server_socket.bind((bind_ip, bind_port))
    server_socket.listen(5)

    print(f"A simpleperf server is listening on port {bind_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"A simpleperf client with {client_address} is connected")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, args.format))
        client_thread.start()

def handle_client(client_socket, result_format):
    client_addr = client_socket.getpeername()
    start_time = time.time()
    total_data_received = 0

    while True:
        data = client_socket.recv(1000)
        total_data_received += len(data)

        if data.decode('utf-8') == "BYE":
            end_time = time.time()
            client_socket.sendall(b"ACK: BYE")
            break

    client_socket.close()

    elapsed_time = end_time - start_time
    transfer, rate = calculate_bandwidth(total_data_received, elapsed_time, result_format)

    print(f"ID: {client_addr[0]}:{client_addr[1]} Interval: {elapsed_time:.1f} s Transfer: {transfer} {result_format} Rate: {rate} Mbps")


def calculate_bandwidth(total_data_received, elapsed_time, result_format):
    
    # Convert total_data_received to the specified format
    if result_format == "B":
        transfer = total_data_received
    elif result_format == "KB":
        transfer = total_data_received / 1000
    elif result_format == "MB":
        transfer = total_data_received / (1000 * 1000)
    else:
        raise ValueError("Invalid format specified")

    # Calculate transfer rate in Mbps
    rate = (total_data_received * 8) / (1000 * 1000 * elapsed_time)

    return round(transfer), round(rate, 2)
    pass




def run_client(args):
    # Set up client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = args.serverip
    server_port = args.port if args.port else 8088

    client_socket.connect((server_ip, server_port))

    print(f"A simpleperf client connecting to server {server_ip}, port {server_port}")

    start_time = time.time()
    total_data_sent = 0
    elapsed_time = 0

    if args.time:
        duration = args.time
    else:
        duration = 25

    while elapsed_time < duration:
        data = b'0' * 1000
        client_socket.sendall(data)
        total_data_sent += len(data)
        elapsed_time = time.time() - start_time

    client_socket.sendall(b"BYE")

    # Wait for server acknowledgement
    data = client_socket.recv(1000)
    if data.decode('utf-8') == "ACK: BYE":
        end_time = time.time()

    # Store client address before closing the socket
    client_address = client_socket.getsockname()

    client_socket.close()

    elapsed_time = end_time - start_time
    transfer, rate = calculate_bandwidth(total_data_sent, elapsed_time, args.format)

    print(f"ID: {client_address[0]}:{client_address[1]} Interval: {elapsed_time:.1f} s Transfer: {transfer} {args.format} Rate: {rate} Mbps")


import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simpleperf - A simplified version of iPerf")

    # Add argument definitions to the parser
    parser.add_argument('-s', '--server', action='store_true', help='Enable server mode')
    parser.add_argument('-c', '--client', action='store_true', help='Enable client mode')
    parser.add_argument('-b', '--bind', type=str, help='Server IP address to bind')
    parser.add_argument('-p', '--port', type=int, help='Server port to bind (default: 8088)')
    parser.add_argument('-f', '--format', type=str, choices=['B', 'KB', 'MB'], default='MB', help='Format of the summary of results (B, KB, MB; default: MB)')
    parser.add_argument('-I', '--serverip', type=str, help='IP address of the server')
    parser.add_argument('-t', '--time', type=int, help='Total duration in seconds for which data should be generated and sent to the server (default: 25)')
    parser.add_argument('-i', '--interval', type=int, help='Print statistics per specified interval (in seconds)')
    parser.add_argument('-P', '--parallel', type=int, choices=range(1, 6), metavar='[1-5]', default=1, help='Number of parallel connections to the server (default: 1)')
    parser.add_argument('-n', '--num', type=str, help='Transfer specified number of bytes (in B, KB, or MB)')

    return parser.parse_args()




def main():
    args = parse_arguments()

    if args.server:
        run_server(args)
    elif args.client:
        run_client(args)
    else:
        print("Error: you must run either in server or client mode")
        exit(1)

if __name__ == "__main__":
    main()
