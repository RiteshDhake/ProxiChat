"""
Main chat interface component.
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.filemanager import MDFileManager
from kivy.metrics import dp
from kivy.clock import Clock
from typing import Optional, Callable, List
import os

from .components import MessageCard, MessageContainer, ChatHeader, MessageInputCard
from .sidebar import Sidebar
from .login_dialog import LoginDialogManager


class ChatInterface(MDScreen):
    """Main chat interface screen."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username: Optional[str] = None
        self.app_theme_cls = None  # Store theme reference separately
        self.send_message_callback: Optional[Callable[[str], None]] = None
        self.send_file_callback: Optional[Callable[[str], None]] = None
        self.connect_callback: Optional[Callable[[str, str], bool]] = None
        
        # Initialize file manager
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_file,
            preview=True,
        )
        
        self.setup_interface()
    
    def setup_interface(self):
        """Setup the main chat interface."""
        # Main layout
        self.main_layout = MDBoxLayout(orientation="vertical")
        self.add_widget(self.main_layout)
        
        # Create app bar
        self.create_app_bar()
        
        # Create main content area
        self.create_main_content()
        
        # Initialize login dialog manager
        self.login_manager = LoginDialogManager(self, self.on_connect_requested)
    
    def create_app_bar(self):
        """Create the top application bar."""
        self.app_bar = MDTopAppBar()
        self.app_bar.title = "Chattr - Desktop Chat Application"
        self.app_bar.elevation = 4
        self.main_layout.add_widget(self.app_bar)
    
    def create_main_content(self):
        """Create the main content area with sidebar and chat."""
        content_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, 1)
        )
        self.main_layout.add_widget(content_layout)
        
        # Create sidebar
        self.sidebar = Sidebar()
        content_layout.add_widget(self.sidebar)
        
        # Create chat area
        self.chat_area = self.create_chat_area()
        content_layout.add_widget(self.chat_area)
    
    def create_chat_area(self) -> MDBoxLayout:
        """Create the main chat area."""
        chat_area = MDBoxLayout(
            orientation="vertical",
            size_hint_x=0.75,  # 75% of screen width
            padding=[dp(0), dp(0), dp(0), dp(0)]
        )
        
        # Create messages container
        messages_card = self.create_messages_card()
        chat_area.add_widget(messages_card)
        
        return chat_area
    
    def create_messages_card(self) -> MDCard:
        """Create the messages container card."""
        messages_card = MDCard(
            orientation="vertical",
            padding=dp(0),
            size_hint=(1, 1)
        )
        
        # Chat header
        chat_header = ChatHeader("General Chat")
        messages_card.add_widget(chat_header)
        
        # Messages scroll area
        self.create_messages_scroll_area(messages_card)
        
        # Message input area
        self.create_message_input(messages_card)
        
        return messages_card
    
    def create_messages_scroll_area(self, parent_card: MDCard):
        """Create the scrollable messages area."""
        self.chat_scroll = MDScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True
        )
        
        self.chat_messages_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_y=None,
            adaptive_height=True,
            padding=[dp(15), dp(5), dp(15), dp(5)]
        )
        
        self.chat_scroll.add_widget(self.chat_messages_layout)
        parent_card.add_widget(self.chat_scroll)
    
    def create_message_input(self, parent_card: MDCard):
        """Create the message input area."""
        self.message_input_card = MessageInputCard(
            send_callback=self.on_send_message,
            file_callback=self.on_send_file
        )
        parent_card.add_widget(self.message_input_card)
    
    def set_callbacks(self, send_message_callback: Callable[[str], None],
                     send_file_callback: Callable[[str], None],
                     connect_callback: Callable[[str, str], bool]):
        """Set the callback functions for various actions."""
        self.send_message_callback = send_message_callback
        self.send_file_callback = send_file_callback
        self.connect_callback = connect_callback
    
    def set_theme(self, theme_cls):
        """Set the theme class for styling."""
        self.app_theme_cls = theme_cls
    
    def show_login_dialog(self, default_username: str = "", default_host: str = "192.168.0.125"):
        """Show the login dialog."""
        self.login_manager.show_login(default_username, default_host)
    
    def on_connect_requested(self, username: str, host: str) -> bool:
        """Handle connection request from login dialog."""
        if self.connect_callback:
            success = self.connect_callback(username, host)
            if success:
                self.username = username
                self.sidebar.set_user_online(username)
                self.enable_chat()
                self.add_system_message("Connected to server", "success")
            else:
                self.add_system_message("Connection failed", "error")
            return success
        return False
    
    def enable_chat(self):
        """Enable the chat interface after successful connection."""
        self.message_input_card.set_enabled(True)
    
    def disable_chat(self):
        """Disable the chat interface."""
        self.message_input_card.set_enabled(False)
        self.sidebar.set_user_offline()
    
    def on_send_message(self, message: str):
        """Handle sending a chat message."""
        if self.send_message_callback:
            self.send_message_callback(message)
    
    def on_send_file(self):
        """Handle file selection for sending."""
        self.show_file_manager()
    
    def display_message(self, username: str, content: str):
        """Display a chat message in the interface."""
        # Add user to active users list
        self.sidebar.add_active_user(username)
        
        # Determine if this is the current user's message
        is_own_message = username == self.username
        
        # Create message card
        message_card = MessageCard(
            username=username,
            content=content,
            is_own_message=is_own_message,
            theme_cls=self.app_theme_cls,
            chat_width=self.chat_messages_layout.width
        )
        
        # Create message container with proper alignment
        message_container = MessageContainer(message_card, is_own_message)
        
        # Add to chat layout
        self.chat_messages_layout.add_widget(message_container)
        
        # Scroll to bottom
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)
    
    def add_system_message(self, message: str, msg_type: str = "info"):
        """Add a system message (connection status, errors, etc.)."""
        color_map = {
            "info": "00ff00",    # Green
            "success": "00ff00",  # Green
            "error": "ff0000",    # Red
            "warning": "ffff00"   # Yellow
        }
        
        color = color_map.get(msg_type, "ffffff")  # Default to white
        formatted_message = f"[i][color={color}]{message}[/color][/i]"
        
        msg_label = MDLabel(
            text=formatted_message,
            size_hint_y=None,
            text_size=(self.chat_scroll.width * 0.7 - dp(30), None),
            valign="top",
            theme_text_color="Primary",
            font_style="Body",
            markup=True
        )
        
        # Bind texture_size to height for proper text wrapping
        msg_label.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        
        self.chat_messages_layout.add_widget(msg_label)
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)
    
    def scroll_to_bottom(self):
        """Scroll chat to the bottom to show latest messages."""
        if self.chat_messages_layout.children:
            self.chat_scroll.scroll_to(self.chat_messages_layout.children[0])
    
    def show_file_manager(self):
        """Show the file manager for file selection."""
        self.file_manager.show(os.path.expanduser("~"))
    
    def exit_file_manager(self, *args):
        """Exit the file manager."""
        self.file_manager.close()
    
    def select_file(self, path: str):
        """Handle file selection from file manager."""
        self.exit_file_manager()
        self.add_system_message(f"Sending file: {os.path.basename(path)}", "info")
        
        if self.send_file_callback:
            self.send_file_callback(path)
    
    def show_error(self, error_message: str):
        """Show an error message to the user."""
        self.add_system_message(error_message, "error")
    
    def show_success(self, success_message: str):
        """Show a success message to the user."""
        self.add_system_message(success_message, "success")
    
    def clear_chat(self):
        """Clear all chat messages."""
        self.chat_messages_layout.clear_widgets()
    
    def get_online_users(self) -> List[str]:
        """Get the list of online users."""
        return self.sidebar.get_active_users()
    
    def get_online_user_count(self) -> int:
        """Get the number of online users."""
        return self.sidebar.get_user_count()
    
    def update_user_status(self, username: str, status: str):
        """Update the current user's status."""
        self.sidebar.update_user_info(username, status)
    
    def disconnect_cleanup(self):
        """Cleanup when disconnecting from server."""
        self.disable_chat()
        self.sidebar.reset_sidebar()
        self.username = None
        self.add_system_message("Disconnected from server", "warning")
    
    def on_file_received(self, filename: str):
        """Handle file received notification."""
        self.add_system_message(f"File received: {filename}", "success")
    
    def get_current_username(self) -> Optional[str]:
        """Get the current username."""
        return self.username
    
    def is_connected(self) -> bool:
        """Check if currently connected to server."""
        return self.username is not None
    
    def focus_message_input(self):
        """Focus on the message input field."""
        if hasattr(self.message_input_card, 'message_input'):
            self.message_input_card.message_input.focus = True