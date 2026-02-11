import socket
import threading
import json
from datetime import datetime
import os

class ChatServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.history = []
        self.usernames = set()
        self.max_history = 50
        self.lock = threading.Lock()
        self.load_history()
    
    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Servidor iniciado en {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Nueva conexión: {address}")
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\nCerrando servidor...")
            self.shutdown()
    
    def handle_client(self, client_socket, address):
        username = None
        try:
            client_socket.send("USUARIO: ".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()
            
            with self.lock:
                if username in self.usernames or not username:
                    client_socket.send("ERROR: Usuario inválido o en uso\n".encode('utf-8'))
                    client_socket.close()
                    return
                
                self.usernames.add(username)
                self.clients[client_socket] = {'username': username}
            
            welcome_msg = f"\nBienvenido {username}!\nEscribe /help para comandos\n"
            client_socket.send(welcome_msg.encode('utf-8'))
            self.broadcast(f"{username} se unió al chat", exclude=client_socket)
            self.send_history(client_socket)
            
            while True:
                message = client_socket.recv(1024).decode('utf-8').strip()
                if not message:
                    break
                
                if message.startswith('/'):
                    self.handle_command(client_socket, message)
                else:
                    self.handle_message(client_socket, message)
        
        except Exception as e:
            print(f"Error con {username or address}: {e}")
        finally:
            self.disconnect_client(client_socket, username)
    
    def handle_command(self, client_socket, command):
        parts = command.split(maxsplit=2)
        cmd = parts[0].lower()
        username = self.clients[client_socket]['username']
        
        if cmd == '/help':
            help_text = """
Comandos:
/help                  - Ayuda
/users                 - Ver usuarios conectados
/whisper <user> <msg>  - Mensaje privado
/quit                  - Desconectar
"""
            client_socket.send(help_text.encode('utf-8'))
        
        elif cmd == '/users':
            with self.lock:
                users_list = [info['username'] for info in self.clients.values()]
            
            users_text = f"\nUsuarios conectados ({len(users_list)}):\n"
            users_text += "\n".join(f"  {u}" for u in users_list) + "\n"
            client_socket.send(users_text.encode('utf-8'))
        
        elif cmd == '/whisper':
            if len(parts) < 3:
                client_socket.send("Uso: /whisper <usuario> <mensaje>\n".encode('utf-8'))
                return
            
            target_user, private_msg = parts[1], parts[2]
            target_socket = None
            
            with self.lock:
                for sock, info in self.clients.items():
                    if info['username'] == target_user:
                        target_socket = sock
                        break
            
            if target_socket:
                timestamp = datetime.now().strftime("%H:%M")
                msg = f"[{timestamp}] {username} (privado): {private_msg}\n"
                target_socket.send(msg.encode('utf-8'))
                client_socket.send(f"Mensaje enviado a {target_user}\n".encode('utf-8'))
            else:
                client_socket.send(f"Usuario '{target_user}' no encontrado\n".encode('utf-8'))
        
        elif cmd == '/quit':
            client_socket.send("Hasta pronto!\n".encode('utf-8'))
            client_socket.close()
        else:
            client_socket.send(f"Comando desconocido: {cmd}\n".encode('utf-8'))
    
    def handle_message(self, client_socket, message):
        username = self.clients[client_socket]['username']
        timestamp = datetime.now().strftime("%H:%M")
        formatted_msg = f"[{timestamp}] {username}: {message}"
        
        with self.lock:
            self.history.append(formatted_msg)
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
        
        self.broadcast(formatted_msg)
        self.save_history()
    
    def broadcast(self, message, exclude=None):
        with self.lock:
            for client in self.clients.keys():
                if client != exclude:
                    try:
                        client.send(f"{message}\n".encode('utf-8'))
                    except:
                        pass
    
    def send_history(self, client_socket):
        with self.lock:
            if self.history:
                history_msg = "\nHistorial:\n" + "\n".join(self.history[-20:]) + "\n"
                client_socket.send(history_msg.encode('utf-8'))
    
    def disconnect_client(self, client_socket, username):
        with self.lock:
            if client_socket in self.clients:
                del self.clients[client_socket]
                if username:
                    self.usernames.discard(username)
                    self.broadcast(f"{username} se desconectó")
        
        try:
            client_socket.close()
        except:
            pass
        
        if username:
            print(f"{username} desconectado")
    
    def save_history(self):
        try:
            with open('chat_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando historial: {e}")
    
    def load_history(self):
        if os.path.exists('chat_history.json'):
            try:
                with open('chat_history.json', 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Error cargando historial: {e}")
    
    def shutdown(self):
        self.save_history()
        with self.lock:
            for client in list(self.clients.keys()):
                try:
                    client.send("Servidor cerrando...\n".encode('utf-8'))
                    client.close()
                except:
                    pass
        self.server_socket.close()
        print("Servidor cerrado")

if __name__ == "__main__":
    server = ChatServer()
    server.start()
