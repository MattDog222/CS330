from socket import *
import base64
import ssl

CRLF = "\r\n"
msg = "I love refactoring!"


# Send command to email server and print response
def send_command(command):
    global clientSocket
    clientSocket.send(command.encode())
    server_response = clientSocket.recv(1024).decode()
    print(command, end="")
    print(server_response)


# IMPORTANT: port change for SSL
# https://stackoverflow.com/questions/57715289/how-to-fix-ssl-sslerror-ssl-wrong-version-number-wrong-version-number-ssl
mailserver = ("smtp.gmail.com", 465)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket = ssl.wrap_socket(clientSocket)
clientSocket.connect(mailserver)
response = clientSocket.recv(1024).decode()
print(f"Connection: {response}")
if response[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
HELO = 'HELO Alice\r\n'
send_command(HELO)

# Authentication using base64
# For Gmail, it is recommended to create an "app password"
username = "wilder.mdog@gmail.com"
password = "16 character app password" # Redacted
base64_str = ("\x00" + username + "\x00" + password).encode()
base64_str = base64.b64encode(base64_str)
authMsg = "AUTH PLAIN ".encode() + base64_str + CRLF.encode()
clientSocket.send(authMsg)
recv_auth = clientSocket.recv(1024)
print("AUTHENTICATION")
print(recv_auth.decode())

#############################
# IMPORTANT
# 555 5.5.2 Syntax error
# FIX := https://blog.yimingliu.com/2008/11/26/email-servers-and-mail-from-syntax/
##############################
MAIL_FROM = f"MAIL FROM: <{username}>{CRLF}"
send_command(MAIL_FROM)

RCPT_TO = f"RCPT TO: <{username}>{CRLF}"
send_command(RCPT_TO)

DATA = f"DATA{CRLF}"
send_command(DATA)

# Send message data. # Message ends with a single period.
MESSAGE = f"Subject: plz give me an A{CRLF*2}{msg}{CRLF}.{CRLF}"
send_command(MESSAGE)

# Send QUIT command and get server response.
QUIT = f"QUIT{CRLF}"
send_command(QUIT)

clientSocket.close()
