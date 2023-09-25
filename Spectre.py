import socket


HOST = '0.0.0.0'
PORT = 514
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"{HOST} listening on port {PORT}")

    while True:
        data = s.recv(512)
        print(data)