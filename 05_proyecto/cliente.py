import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
    
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"Conectado al servidor {self.host}:{self.port}")
            
            prompt = self.socket.recv(1024).decode('utf-8')
            print(prompt, end='')
            
            username = input().strip()
            self.socket.send(username.encode('utf-8'))
            
            response = self.socket.recv(1024).decode('utf-8')
            print(response)
            
            if "ERROR" in response:
                self.socket.close()
                return False
            
            self.running = True
            return True
            
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
    
    def receive_messages(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                
                if not message:
                    print("\nConexión cerrada por el servidor")
                    self.running = False
                    break
                
                print(message, end='')
                
            except Exception as e:
                if self.running:
                    print(f"\nError recibiendo mensaje: {e}")
                break
    
    def send_messages(self):
        print("\nPuedes empezar a chatear (escribe /help para comandos)\n")
        
        while self.running:
            try:
                message = input()
                
                if not self.running:
                    break
                
                if message.strip():
                    self.socket.send(message.encode('utf-8'))
                    
                    if message.strip() == '/quit':
                        self.running = False
                        break
                        
            except KeyboardInterrupt:
                print("\nDesconectando...")
                self.running = False
                break
            except Exception as e:
                print(f"\nError enviando mensaje: {e}")
                self.running = False
                break
    
    def start(self):
        if not self.connect():
            return
        
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        try:
            self.send_messages()
        except KeyboardInterrupt:
            print("\nDesconectando...")
        finally:
            self.close()
    
    def close(self):
        self.running = False
        try:
            self.socket.close()
        except:
            pass
        print("Desconectado del servidor")

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5555
    
    client = ChatClient(host, port)
    client.start()