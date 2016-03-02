import socket

cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = socket.gethostbyname(socket.gethostname())

port = 11111

cli.connect((ip, port))

server_reply = cli.recv(65535)

print server_reply

cli.close()
