import socket
import threading

HOST = 'localhost'
PORT = 9000

def recibir_mensajes():
    while True:
        mensaje = cliente.recv(1024).decode()
        print(mensaje)

nombre = input("Cuál es tu nombre: ")       
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))
cliente.send(nombre.encode())

hilo_recibir = threading.Thread(target=recibir_mensajes)
hilo_recibir.start()

while True:
    mensaje = input("Mensaje: ")
    cliente.send(mensaje.encode())


cliente.sendall(b"Mundo!")
respuesta = cliente.recv(1024)
print(f"Repuesta: {respuesta}")

cliente.close()

