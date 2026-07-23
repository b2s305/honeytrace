import socket
import threading
import paramiko

from config.config import HOST, PORT, HOST_KEY
from ssh.auth import HoneyTraceSSHServer


host_key = paramiko.RSAKey(filename=HOST_KEY)


def handle_client(client_socket, client_address):

    print(f"\n[+] New Connection from {client_address[0]}:{client_address[1]}")

    transport = paramiko.Transport(client_socket)
    transport.add_server_key(host_key)

    server = HoneyTraceSSHServer(client_address[0])

    try:
        transport.start_server(server=server)

        channel = transport.accept(20)

        if channel is None:
            print("Authentication failed.")
            return

        channel.close()

    except Exception as e:
        print("SSH Error:", e)

    finally:
        transport.close()


def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))

    server_socket.listen(100)

    print("=" * 60)
    print("🍯 HoneyTrace SSH Honeypot Started")
    print(f"Listening on {HOST}:{PORT}")
    print("=" * 60)

    while True:

        client_socket, client_address = server_socket.accept()

        threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True
        ).start()