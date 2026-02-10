import socket
import threading

HOST = 'localhost'
PORT = 9000

clientes = []

def atender_cliente(cliente, nombre):
    while True:
        try:
            mensaje = cliente.recv(1024)
            if not mensaje:
                break
            print(f"{nombre}: {mensaje.decode()}")
            broadcast(mensaje, cliente)

        except ConnectionResetError:
            clientes.remove(cliente)
            cliente.close()
            break
def broadcast(mensaje, emisor):
    for cliente in clientes:
        if cliente != emisor:
            cliente.send(mensaje.encode())
    
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print("el servidor 'Chat' está esperando conexiones ...")

while True:
    cliente, direccion = servidor.accept()
    print(f"cliente conectado desde la IP: {direccion}")
    nombre = cliente.recv(1024).decode()
    clientes.append(cliente)
    broadcast(f"{nombre} se ha unido al 'Chat'", cliente)
    hilo_cliente = threading.Thread(target=atender_cliente, args=(cliente, nombre))
    hilo_cliente.start()

cliente.close()

