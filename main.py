"""
Fixed main application file - ready to use with the organized UI components.
"""

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock
import socket
import threading
import os

# Import your UI components
from ui.chat_interface import ChatInterface


class ChatApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = None
        self.username = None
        self.active_users = []
        self.chat_interface = None
        
        # Network settings
        self.PORT = 1234
        
    def build(self):
        # Set window properties - FIXED: Set minimum size properly
        Window.size = (1000, 700)
        Window.minimum_width = 800
        Window.minimum_height = 600
        
        # Configure theme
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        
        # Create chat interface - FIXED: No theme assignment in constructor
        self.chat_interface = ChatInterface()
        
        # FIXED: Set theme after creation
        self.chat_interface.set_theme(self.theme_cls)
        
        # Set up callbacks
        self.chat_interface.set_callbacks(
            send_message_callback=self.send_message,
            send_file_callback=self.send_file_data,
            connect_callback=self.connect_to_server
        )
        
        # Show login dialog
        self.chat_interface.show_login_dialog()
        
        return self.chat_interface
    
    def connect_to_server(self, username: str, host: str) -> bool:
        """Connect to the chat server."""
        try:
            # Create new socket
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, self.PORT))
            
            # Store username and send to server
            self.username = username
            self.client.sendall(self.username.encode())
            
            # Start listening thread
            threading.Thread(target=self.listen_for_messages, daemon=True).start()
            
            return True
            
        except Exception as e:
            print(f"Connection error: {e}")
            if self.client:
                try:
                    self.client.close()
                except:
                    pass
                self.client = None
            return False
    
    def listen_for_messages(self):
        """Listen for incoming messages from server."""
        while True:
            try:
                # Receive message header
                message_header = self.client.recv(1024).decode('utf-8')
                if not message_header:
                    break
                
                # Handle file transfer
                if message_header == "sending_file":
                    Clock.schedule_once(lambda dt: self.receive_file())
                else:
                    # Handle regular chat message
                    try:
                        username, content = message_header.split("~", 1)
                        Clock.schedule_once(
                            lambda dt: self.chat_interface.display_message(username, content)
                        )
                    except ValueError:
                        # Handle malformed messages
                        print(f"Malformed message: {message_header}")
                    
            except Exception as e:
                print(f"Error receiving message: {e}")
                Clock.schedule_once(
                    lambda dt: self.chat_interface.show_error(f"Connection lost: {str(e)}")
                )
                break
    
    def send_message(self, message: str):
        """Send a chat message to the server."""
        if self.client and self.username:
            try:
                full_message = f"{self.username}~{message}"
                self.client.sendall(full_message.encode('utf-8'))
            except Exception as e:
                self.chat_interface.show_error(f"Failed to send message: {str(e)}")
    
    def send_file_data(self, file_path: str):
        """Send file data to the server."""
        if not self.client:
            self.chat_interface.show_error("Not connected to server")
            return
            
        try:
            # Signal file transfer
            self.client.send("sending_file".encode('utf-8'))
            
            # Send file data
            with open(file_path, 'rb') as file:
                data = file.read()
                self.client.sendall(data)
                self.client.send(b"<END>")
                
            self.chat_interface.show_success(f"File sent: {os.path.basename(file_path)}")
            
        except Exception as e:
            self.chat_interface.show_error(f"Failed to send file: {str(e)}")
    
    def receive_file(self):
        """Receive file data from server."""
        try:
            file_bytes = b""
            while True:
                data = self.client.recv(1024)
                file_bytes += data
                if b"<END>" in file_bytes:
                    file_bytes = file_bytes.replace(b"<END>", b"")
                    break
            
            # Save received file
            with open("Recv_file.txt", "wb") as file:
                file.write(file_bytes)
            
            self.chat_interface.on_file_received("Recv_file.txt")
            
        except Exception as e:
            self.chat_interface.show_error(f"Failed to receive file: {str(e)}")
    
    def on_stop(self):
        """Cleanup when app is closing."""
        if self.client:
            try:
                self.client.close()
            except:
                pass


if __name__ == '__main__':
    ChatApp().run()