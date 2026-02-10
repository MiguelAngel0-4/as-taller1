import socket
import http.server

HOST = 'localhost'
PORT = 9000

class Servidor(http.server.SimpleHTTPRequestHandlermple):
    pass

Servidor = http.server.HTTPServer((HOST, PORT), Servidor)
Servidor.serve_forever()

