"""
Enhanced main application file integrating the modern UI components.
This shows how to integrate all the enhanced UI components into your main app.
"""

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
import socket
import threading
import os
from kivy.core.text import LabelBase
import platform


# Import enhanced UI components
from ui import (
    ModernChatInterface,
    ModernColors,
    Typography,
    SystemMessages,
    ErrorMessages,
    Features,
    validate_username,
    validate_ip_address,
    validate_message
)


class EnhancedChatApp(MDApp):
    """Enhanced chat application with modern UI."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Chattr - Modern Desktop Chat"
        self.socket = None
        self.connected = False
        self.username = None
        self.host = None
        self.receive_thread = None
        
    def build(self):
        """Build the enhanced application."""
        # Configure app theme
        self.setup_theme()
        
        # Configure window
        self.setup_window()
        
        # Create screen manager
        self.screen_manager = MDScreenManager()
        
        # Create and configure chat interface
        self.chat_interface = ModernChatInterface(name="chat")
        self.chat_interface.set_callbacks(
            send_message_callback=self.send_message,
            send_file_callback=self.send_file,
            connect_callback=self.connect_to_server
        )
        
        self.screen_manager.add_widget(self.chat_interface)
        self.setup_emoji_support()
        # Show login dialog on startup
        Clock.schedule_once(
            lambda dt: self.chat_interface.show_login_dialog("User", "192.168.0.125"), 
            0.5
        )
        
        return self.screen_manager
    def setup_emoji_support(self):
        
        system = platform.system()
        
        if system == "Windows":
            # Try to register emoji fonts on Windows
            try:
                # Windows 10/11 emoji font
                LabelBase.register(
                    name="emoji",
                    fn_regular="C:/Windows/Fonts/seguiemj.ttf"
                )
                return "emoji"
            except:
                try:
                    # Fallback to Segoe UI Symbol
                    LabelBase.register(
                        name="symbols",
                        fn_regular="C:/Windows/Fonts/seguisym.ttf"
                    )
                    return "symbols"
                except:
                    return None
        
        elif system == "Darwin":  # macOS
            try:
                LabelBase.register(
                    name="emoji",
                    fn_regular="/System/Library/Fonts/Apple Color Emoji.ttc"
                )
                return "emoji"
            except:
                return None
        
        elif system == "Linux":
            # Try common Linux emoji fonts
            emoji_fonts = [
                "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/TTF/NotoColorEmoji.ttf"
            ]
            
            for font_path in emoji_fonts:
                try:
                    import os
                    if os.path.exists(font_path):
                        LabelBase.register(name="emoji", fn_regular=font_path)
                        return "emoji"
                except:
                    continue
            return None
        
        return None

    def setup_theme(self):
        """Configure modern app theme."""
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "LightBlue"
        
        # Set theme for chat interface
        if hasattr(self, 'chat_interface'):
            self.chat_interface.app_theme_cls = self.theme_cls
    
    def setup_window(self):
        """Configure window properties."""
        Window.size = (1200, 800)
        Window.minimum_width = 900
        Window.minimum_height = 650
        Window.clearcolor = ModernColors.MAIN_BACKGROUND
        
        # Bind window events
        Window.bind(on_request_close=self.on_window_close)
    
    def connect_to_server(self, username: str, host: str) -> bool:
        """Enhanced connection with validation and feedback."""
        # Validate inputs
        username_valid, username_error = validate_username(username)
        if not username_valid:
            self.chat_interface.add_enhanced_system_message(username_error, "error")
            return False
        
        ip_valid, ip_error = validate_ip_address(host)
        if not ip_valid:
            self.chat_interface.add_enhanced_system_message(ip_error, "error")
            return False
        
        # Attempt connection
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10.0)  # 10 second timeout
            
            # Connect to server
            self.socket.connect((host, 1234))
            
            # Send username
            self.socket.send(username.encode('utf-8'))
            
            # Store connection info
            self.username = username
            self.host = host
            self.connected = True
            
            # Start receiving thread
            self.start_receive_thread()
            
            return True
            
        except socket.timeout:
            self.chat_interface.add_enhanced_system_message(
                ErrorMessages.CONNECTION_TIMEOUT, "error"
            )
            self.cleanup_connection()
            return False
            
        except ConnectionRefusedError:
            self.chat_interface.add_enhanced_system_message(
                ErrorMessages.CONNECTION_REFUSED, "error"
            )
            self.cleanup_connection()
            return False
            
        except Exception as e:
            self.chat_interface.add_enhanced_system_message(
                f"Connection error: {str(e)}", "error"
            )
            self.cleanup_connection()
            return False
    
    def start_receive_thread(self):
        """Start enhanced message receiving thread."""
        if self.receive_thread and self.receive_thread.is_alive():
            return
        
        self.receive_thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )
        self.receive_thread.start()
    
    def receive_messages(self):
        """Enhanced message receiving with better error handling."""
        while self.connected and self.socket:
            try:
                # Receive message
                message = self.socket.recv(1024).decode('utf-8')
                
                if not message:
                    # Server closed connection
                    Clock.schedule_once(lambda dt: self.handle_disconnection(), 0)
                    break
                
                # Handle different message types
                Clock.schedule_once(
                    lambda dt, msg=message: self.process_received_message(msg), 
                    0
                )
                
            except socket.timeout:
                continue
                
            except ConnectionResetError:
                Clock.schedule_once(lambda dt: self.handle_connection_reset(), 0)
                break
                
            except Exception as e:
                print(f"Receive error: {e}")
                Clock.schedule_once(lambda dt: self.handle_receive_error(str(e)), 0)
                break
    
    def process_received_message(self, message: str):
        """Process received message with enhanced parsing."""
        try:
            if message.startswith("USER_JOINED:"):
                username = message.split(":", 1)[1]
                self.chat_interface.user_joined(username)
                
            elif message.startswith("USER_LEFT:"):
                username = message.split(":", 1)[1]
                self.chat_interface.user_left(username)
                
            elif message.startswith("FILE_RECEIVED:"):
                filename = message.split(":", 1)[1]
                self.chat_interface.add_enhanced_system_message(
                    SystemMessages.FILE_RECEIVED.format(filename=filename), 
                    "success"
                )
                
            elif ":" in message:
                # Regular chat message
                username, content = message.split(":", 1)
                self.chat_interface.display_message(username, content)
                
            else:
                # System message
                self.chat_interface.add_enhanced_system_message(message, "info")
                
        except Exception as e:
            print(f"Message processing error: {e}")
            self.chat_interface.add_enhanced_system_message(
                "Error processing message", "error"
            )
    
    def send_message(self, message: str):
        """Enhanced message sending with validation."""
        if not self.connected or not self.socket:
            self.chat_interface.add_enhanced_system_message(
                ErrorMessages.NOT_CONNECTED, "error"
            )
            return
        
        # Validate message
        is_valid, error_msg = validate_message(message)
        if not is_valid:
            self.chat_interface.add_enhanced_system_message(error_msg, "error")
            return 
        
        try:
            # Send message
            self.socket.send(message.encode('utf-8'))
            
            # Display own message immediately
            self.chat_interface.display_message(self.username, message)
            
        except Exception as e:
            print(f"Send error: {e}")
            self.chat_interface.add_enhanced_system_message(
                ErrorMessages.SEND_FAILED, "error"
            )
            self.handle_send_error()
    
    def send_file(self, file_path: str):
        """Enhanced file sending with progress feedback."""
        if not self.connected or not self.socket:
            self.chat_interface.add_enhanced_system_message(
                ErrorMessages.NOT_CONNECTED, "error"
            )
            return
        
        if not Features.ENABLE_FILE_SHARING:
            self.chat_interface.add_enhanced_system_message(
                "File sharing is currently disabled", "warning"
            )
            return
        
        try:
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            # Check file size (50MB limit)
            if file_size > 50 * 1024 * 1024:
                self.chat_interface.add_enhanced_system_message(
                    ErrorMessages.FILE_TOO_LARGE.format(max_size=50), "error"
                )
                return
            
            # Show sending status
            self.chat_interface.add_enhanced_system_message(
                SystemMessages.FILE_SENDING.format(filename=filename), "info"
            )
            
            # Send file signal
            self.socket.send("sending_file".encode('utf-8'))
            
            # Send filename
            self.socket.send(filename.encode('utf-8'))
            
            # Send file content
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(4096)
                    if not data:
                        break
                    self.socket.send(data)
            
            # Send end marker
            self.socket.send(b"<END>")
            
            # Success message
            self.chat_interface.add_enhanced_system_message(
                SystemMessages.FILE_SENT.format(filename=filename), "success"
            )
            
        except FileNotFoundError:
            self.chat_interface.add_enhanced_system_message(
                ErrorMessages.FILE_NOT_FOUND, "error"
            )
        except PermissionError:
            self.chat_interface.add_enhanced_system_message(
                ErrorMessages.FILE_PERMISSION_ERROR, "error"
            )
        except Exception as e:
            print(f"File send error: {e}")
            self.chat_interface.add_enhanced_system_message(
                ErrorMessages.FILE_SEND_FAILED, "error"
            )
    
    def handle_disconnection(self):
        """Handle server disconnection with enhanced feedback."""
        self.connected = False
        self.cleanup_connection()
        self.chat_interface.disconnect_cleanup()
        
        if Features.ENABLE_AUTO_RECONNECT:
            self.schedule_reconnection()
    
    def handle_connection_reset(self):
        """Handle connection reset by server."""
        self.chat_interface.add_enhanced_system_message(
            "Connection reset by server", "warning"
        )
        self.handle_disconnection()
    
    def handle_receive_error(self, error_msg: str):
        """Handle receive error with user feedback."""
        self.chat_interface.add_enhanced_system_message(
            f"Network error: {error_msg}", "error"
        )
        self.handle_disconnection()
    
    def handle_send_error(self):
        """Handle send error and attempt recovery."""
        if self.connected:
            self.chat_interface.add_enhanced_system_message(
                "Message failed to send - connection may be unstable", "warning"
            )
    
    def schedule_reconnection(self):
        """Schedule automatic reconnection attempt."""
        if not Features.ENABLE_AUTO_RECONNECT:
            return
        
        self.chat_interface.add_enhanced_system_message(
            "Attempting to reconnect in 3 seconds...", "info"
        )
        
        Clock.schedule_once(
            lambda dt: self.attempt_reconnection(), 
            3.0
        )
    
    def attempt_reconnection(self):
        """Attempt to reconnect to server."""
        if self.username and self.host:
            self.chat_interface.add_enhanced_system_message(
                "Reconnecting...", "info"
            )
            
            success = self.connect_to_server(self.username, self.host)
            if success:
                self.chat_interface.add_enhanced_system_message(
                    SystemMessages.RECONNECTED, "success"
                )
            else:
                # Schedule another attempt
                Clock.schedule_once(
                    lambda dt: self.schedule_reconnection(), 
                    2.0
                )
    
    def cleanup_connection(self):
        """Enhanced connection cleanup."""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        
        self.connected = False
        
        # Wait for receive thread to finish
        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread.join(timeout=1.0)
    
    def on_window_close(self, *args):
        """Handle window close with proper cleanup."""
        # Send disconnect message if connected
        if self.connected and self.socket:
            try:
                self.socket.send("DISCONNECT".encode('utf-8'))
            except:
                pass
        
        # Clean up connection
        self.cleanup_connection()
        
        # Save user preferences (if implemented)
        self.save_user_preferences()
        
        return False  # Allow window to close
    
    def save_user_preferences(self):
        """Save user preferences for next session."""
        try:
            import json
            preferences = {
                "last_username": self.username or "",
                "last_host": self.host or "192.168.0.125",
                "theme": "dark",
                "features": {
                    "animations": Features.ENABLE_ANIMATIONS,
                    "file_sharing": Features.ENABLE_FILE_SHARING
                }
            }
            
            with open("chat_preferences.json", "w") as f:
                json.dump(preferences, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save preferences: {e}")
    
    def load_user_preferences(self) -> dict:
        """Load user preferences from previous session."""
        try:
            import json
            with open("chat_preferences.json", "r") as f:
                return json.load(f)
        except:
            return {
                "last_username": "",
                "last_host": "192.168.0.125",
                "theme": "dark",
                "features": {}
            }
    
    def on_start(self):
        """Enhanced startup with preference loading."""
        # Load preferences
        prefs = self.load_user_preferences()
        
        # Apply preferences to chat interface
        if prefs.get("last_username") or prefs.get("last_host"):
            Clock.schedule_once(
                lambda dt: self.chat_interface.show_login_dialog(
                    prefs.get("last_username", ""),
                    prefs.get("last_host", "192.168.0.125")
                ),
                1.0
            )
    
    def on_stop(self):
        """Enhanced cleanup on app stop."""
        self.cleanup_connection()


# ============================================================================
# ENHANCED SERVER IMPLEMENTATION (Optional)
# ============================================================================

class EnhancedChatServer:
    """Enhanced chat server with modern features."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 1234):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = {}
        self.running = False
    
    def start_server(self):
        """Start enhanced server with better error handling."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(10)
            
            self.running = True
            print(f"🚀 Enhanced Chat Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    print(f"👤 New connection from {address}")
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error:
                    if self.running:
                        print("Server socket error")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.cleanup_server()
    
    def handle_client(self, client_socket, address):
        """Enhanced client handling with modern features."""
        username = None
        
        try:
            # Receive username
            username = client_socket.recv(1024).decode('utf-8')
            if not username:
                return
            
            # Store client
            self.clients[username] = client_socket
            
            # Notify all clients of new user
            self.broadcast_message(f"USER_JOINED:{username}", exclude=username)
            
            print(f"✅ {username} joined from {address}")
            
            # Handle messages from this client
            while self.running:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    
                    if not message:
                        break
                    
                    if message == "DISCONNECT":
                        break
                    elif message == "sending_file":
                        self.handle_file_transfer(client_socket, username)
                    else:
                        # Broadcast regular message
                        full_message = f"{username}:{message}"
                        self.broadcast_message(full_message, exclude=username)
                        print(f"💬 {username}: {message}")
                
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    print(f"🔌 {username} disconnected unexpectedly")
                    break
                except Exception as e:
                    print(f"Client handling error: {e}")
                    break
        
        except Exception as e:
            print(f"Client setup error: {e}")
        
        finally:
            # Clean up client
            if username:
                self.cleanup_client(username, client_socket)
    
    def handle_file_transfer(self, client_socket, sender_username):
        """Enhanced file transfer handling."""
        try:
            # Receive filename
            filename = client_socket.recv(1024).decode('utf-8')
            print(f"📁 Receiving file '{filename}' from {sender_username}")
            
            # Create received files directory
            recv_dir = "received_files"
            os.makedirs(recv_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(recv_dir, f"{sender_username}_{filename}")
            
            with open(file_path, 'wb') as file:
                while True:
                    data = client_socket.recv(4096)
                    if data.endswith(b"<END>"):
                        file.write(data[:-5])  # Remove <END> marker
                        break
                    file.write(data)
            
            # Notify all clients
            file_message = f"FILE_RECEIVED:{filename}"
            self.broadcast_message(file_message)
            
            print(f"✅ File '{filename}' saved successfully")
            
        except Exception as e:
            print(f"File transfer error: {e}")
    
    def broadcast_message(self, message: str, exclude: str = None):
        """Enhanced message broadcasting."""
        disconnected_clients = []
        
        for username, client_socket in self.clients.items():
            if exclude and username == exclude:
                continue
            
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                disconnected_clients.append(username)
        
        # Clean up disconnected clients
        for username in disconnected_clients:
            if username in self.clients:
                self.cleanup_client(username, self.clients[username])
    
    def cleanup_client(self, username: str, client_socket):
        """Enhanced client cleanup."""
        try:
            client_socket.close()
        except:
            pass
        
        if username in self.clients:
            del self.clients[username]
        
        # Notify remaining clients
        self.broadcast_message(f"USER_LEFT:{username}")
        print(f"🚪 {username} left the chat")
    
    def cleanup_server(self):
        """Enhanced server cleanup."""
        self.running = False
        
        # Close all client connections
        for username, client_socket in list(self.clients.items()):
            self.cleanup_client(username, client_socket)
        
        # Close server socket
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        
        print("🛑 Chat server stopped")


# ============================================================================
# APPLICATION LAUNCHER
# ============================================================================

def run_chat_app():
    """Launch the enhanced chat application."""
    app = EnhancedChatApp()
    app.run()


def run_chat_server():
    """Launch the enhanced chat server."""
    server = EnhancedChatServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown requested")
        server.cleanup_server()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        run_chat_server()
    else:
        run_chat_app()


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
USAGE EXAMPLES:

1. Run the chat application (client):
   ```bash
   python main.py
   ```

2. Run the chat server:
   ```bash
   python main.py server
   ```

3. Customize the interface programmatically:
   ```python
   from ui import ModernChatInterface, ModernColors
   
   app = EnhancedChatApp()
   
   # Customize colors
   app.chat_interface.main_layout.md_bg_color = ModernColors.MAIN_BACKGROUND
   
   # Add custom callbacks
   def custom_message_handler(message):
       print(f"Custom handler: {message}")
   
   app.chat_interface.set_callbacks(
       send_message_callback=custom_message_handler,
       send_file_callback=app.send_file,
       connect_callback=app.connect_to_server
   )
   
   app.run()
   ```

4. Advanced server configuration:
   ```python
   server = EnhancedChatServer(host="0.0.0.0", port=8080)
   server.start_server()
   ```

FEATURES INCLUDED:
✅ Modern dark theme with glassmorphism effects
✅ Smooth animations and transitions
✅ Enhanced user feedback and status indicators
✅ Improved error handling and validation
✅ File sharing with progress feedback
✅ Auto-reconnection capabilities
✅ User preferences persistence
✅ Professional typography and spacing
✅ Responsive design elements
✅ Enhanced accessibility features

REQUIREMENTS:
- KivyMD 1.1.1+
- Kivy 2.1.0+
- Python 3.8+
"""