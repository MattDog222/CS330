from webserver.constants import CRLF


def response_header(version="HTTP/1.1", status="200 OK", headers=None):
    if headers is None:
        headers = []
    header = f"{version} {status}{CRLF}"
    for h in headers:
        header += (h + CRLF)
    header += (CRLF * 2)
    return header


def http_response(connection_socket, header, body):
    connection_socket.send(header.encode())
    connection_socket.send(body.encode())
    connection_socket.close()