import argparse
import socket
import struct
import os

class DRTPSocket:
    def __init__(self, ip, port, reliable_method, bind_socket=False):
        self.ip = ip
        self.port = port
        self.reliable_method = reliable_method
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if bind_socket:
            self.sock.bind((ip, port))

    def send_packet(self, packet, dest_ip, dest_port):
        self.sock.sendto(packet, (dest_ip, dest_port))

    def receive_packet(self, buffer_size=4096):
        packet, addr = self.sock.recvfrom(buffer_size)
        return packet, addr

    def close(self):
        self.sock.close()


def establish_connection(drtp_socket, dest_ip, dest_port):
    # Set timeout for the socket
    drtp_socket.sock.settimeout(1)

    # Step 1: Client sends SYN packet
    if dest_ip != "":
        syn_packet = create_packet(0, 0, 'S', 0)
        drtp_socket.send_packet(syn_packet, dest_ip, dest_port)
        print("SYN sent")

    # Step 2: Server receives SYN packet and sends SYN-ACK packet
    while True:
        try:
            packet, addr = drtp_socket.receive_packet()
            seq, ack, flags, _ = parse_packet(packet)
            if flags == 'S':
                syn_ack_packet = create_packet(ack + 1, seq + 1, 'SA', 0)
                drtp_socket.send_packet(syn_ack_packet, addr[0], addr[1])
                print("SYN-ACK sent")
                break
        except socket.timeout:
            if dest_ip != "":
                drtp_socket.send_packet(syn_packet, dest_ip, dest_port)
                print("SYN resent")

    # Step 3: Client receives SYN-ACK packet and sends ACK packet
    while dest_ip != "":
        try:
            packet, addr = drtp_socket.receive_packet()
            seq, ack, flags, _ = parse_packet(packet)
            if flags == 'SA':
                ack_packet = create_packet(ack, seq, 'A', 0)
                drtp_socket.send_packet(ack_packet, dest_ip, dest_port)
                print("ACK sent")
                break
        except socket.timeout:
            drtp_socket.send_packet(syn_packet, dest_ip, dest_port)
            print("SYN resent")


def close_connection(drtp_socket):
    # Set timeout for the socket
    drtp_socket.sock.settimeout(1)

    # Step 1: Client sends FIN packet
    if drtp_socket.dest_ip != "":
        fin_packet = create_packet(0, 0, 'F', 0)
        drtp_socket.send_packet(fin_packet, drtp_socket.dest_ip, drtp_socket.dest_port)
        print("FIN sent")

    # Step 2: Server receives FIN packet and sends ACK packet
    while True:
        try:
            packet, addr = drtp_socket.receive_packet()
            seq, ack, flags, _ = parse_packet(packet)
            if flags == 'F':
                ack_packet = create_packet(ack + 1, seq + 1, 'A', 0)
                drtp_socket.send_packet(ack_packet, addr[0], addr[1])
                print("ACK sent")
                break
        except socket.timeout:
            if drtp_socket.dest_ip != "":
                drtp_socket.send_packet(fin_packet, drtp_socket.dest_ip, drtp_socket.dest_port)
                print("FIN resent")

    # Close the socket
    drtp_socket.sock.close()


def send_file(drtp_socket, file_path, dest_ip, dest_port):
    # Read the file and break it into chunks
    with open(file_path, "rb") as file:
        file_data = file.read()
    chunks = [file_data[i:i+1460] for i in range(0, len(file_data), 1460)]

    # Send the chunks using the specified reliable transport protocol
    seq = 0
    for chunk in chunks:
        while True:
            # Send the packet
            packet = drtp_socket.create_packet(seq, 0, 'D', 0, chunk)
            drtp_socket.send_packet(packet, dest_ip, dest_port)

            # Wait for the ACK
            try:
                ack_packet, _ = drtp_socket.receive_packet()
                ack_seq, _, flags, _ = drtp_socket.parse_packet(ack_packet)
                if flags == 'A' and ack_seq == seq + 1:
                    break  # ACK received, move to the next chunk
            except socket.timeout:
                pass  # Timeout, resend the packet

        seq += 1

    print("File transfer complete")

def create_packet(seq_num, ack_num, flags, payload):
    """
    Create a DRTP packet with the given parameters.
    seq_num: Sequence number
    ack_num: Acknowledgment number
    flags: Flags string, which can include 'S' (SYN), 'A' (ACK), and 'F' (FIN)
    payload: Data payload
    """
    seq_num = struct.pack(">I", seq_num)
    ack_num = struct.pack(">I", ack_num)
    flag_str = "".join(sorted(flags.upper()))
    flag_bytes = flag_str.encode("utf-8")

    # Convert payload to bytes if it's an integer
    if isinstance(payload, int):
        payload = struct.pack(">I", payload)

    packet = seq_num + ack_num + flag_bytes + payload
    return packet

def parse_packet(packet):
    """
    Parse a DRTP packet and extract the sequence number, acknowledgment number, flags, and payload.
    packet: DRTP packet
    """
    seq_num = struct.unpack(">I", packet[:4])[0]
    ack_num = struct.unpack(">I", packet[4:8])[0]
    flags = packet[8:11].decode("utf-8")
    payload = packet[11:]

    return seq_num, ack_num, flags, payload


def receive_file(drtp_socket, output_file_path):
    chunks = []
    expected_seq = 0

    while True:
        try:
            packet, _ = drtp_socket.receive_packet()
            seq, _, flags, _, data = drtp_socket.parse_packet(packet)

            if flags == 'F':
                # FIN flag received, end of file transfer
                break

            if seq == expected_seq:
                # Correct sequence number, append the data chunk
                chunks.append(data)
                expected_seq += 1

            # Send the ACK for the received sequence number
            ack_packet = drtp_socket.create_packet(0, expected_seq, 'A', 0, b'')
            drtp_socket.send_packet(ack_packet, drtp_socket.dest_ip, drtp_socket.dest_port)
        except socket.timeout:
            pass  # Timeout, wait for the next packet

    # Assemble the received chunks and write them to the output file
    file_data = b''.join(chunks)
    with open(output_file_path, "wb") as output_file:
        output_file.write(file_data)

    print("File received and saved to", output_file_path)


def client(args):
    drtp_socket = DRTPSocket(args.ip, args.port, args.reliable_method, bind_socket=True)
    establish_connection(drtp_socket, args.ip, args.port)
    send_file(drtp_socket, args.file, args.ip, args.port)
    close_connection(drtp_socket)

def server(args):
    print("Hei from server")
    drtp_socket = DRTPSocket(args.ip, args.port, args.reliable_method, bind_socket=False)
    establish_connection(drtp_socket, "", args.port)
    output_file_path = os.path.splitext(args.file)[0] + "-recv" + os.path.splitext(args.file)[1]
    
    while True:
        packet, addr = drtp_socket.receive_packet()
        seq, ack, flags, payload = parse_packet(packet)
        print("Received packet with flags:", flags)  # Add this line
        if 'S' in flags:
            print("Received SYN packet")  # Add this line
            ack_packet = create_packet(seq_num=seq + 1, ack_num=seq + 1, flags='SA', payload=b'')
            drtp_socket.send_packet(ack_packet, addr[0], addr[1])
            break
        
    receive_file(drtp_socket, output_file_path)
    close_connection(drtp_socket)



def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="DRTP File Transfer Application")
    parser.add_argument("-c", "--client", action="store_true", help="Run as client")
    parser.add_argument("-s", "--server", action="store_true", help="Run as server")
    parser.add_argument("-i", "--ip", type=str, help="IP address")
    parser.add_argument("-p", "--port", type=int, help="Port number")
    parser.add_argument("-f", "--file", type=str, help="File to transfer (for client)")
    parser.add_argument("-r", "--reliable_method", choices=["stop_and_wait", "gbn", "sr"], help="Reliability method")
    parser.add_argument("-t", "--test_case", type=str, help="Test case")
    
    args = parser.parse_args()

    # Validate command line arguments
    if not (args.client or args.server):
        print("Error: Must specify either client or server mode.")
        exit(1)

    if args.client and args.server:
        print("Error: Cannot run as both client and server.")
        exit(1)

    if args.client and not args.file:
        print("Error: Must specify a file to transfer when running as client.")
        exit(1)

    if args.client:
        client(args)
    else:
        server(args)

if __name__ == "__main__":
    main()
