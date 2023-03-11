from socket import *
from webserver.constants import *
from webserver.request_mapper import *
from webserver.utils import *
import sys


mapper = RequestMapper()

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((HOST_NAME, PORT_NUMBER))
serverSocket.listen(BACKLOG_SIZE)
while True:
    try:
        print('Awaiting your HTTP request senpai...')
        connectionSocket, addr = serverSocket.accept()
        try:
            http_request = connectionSocket.recv(BUFFER_SIZE).decode().split()

            http_method = http_request[0]
            if http_method != "GET":
                continue
            server_path = http_request[1][1:]
            http_version = http_request[2]

            content_type = "text/html"
            if server_path.endswith("css"):
                content_type = "text/css"
            elif server_path.endswith("js"):
                content_type = "text/javascript"

            header = response_header(http_version, headers=[f'Content-Type: {content_type}'])
            body = mapper.get_page(server_path)

            http_response(connectionSocket, header, body)
        except PageNotFoundException:
            header = response_header(status="404 Not Found", headers=['Content-Type: text/html'])
            body = mapper.get_error_page(404)
            http_response(connectionSocket, header, body)
        except Exception as e:
            header = response_header(status="500 Internal Server Error", headers=['Content-Type: text/html'])
            body = mapper.get_error_page(500)
            http_response(connectionSocket, header, body)
    except Exception:
        continue
