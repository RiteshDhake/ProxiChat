"""
Login dialog component for the chat application.
"""

from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldLeadingIcon,
    MDTextFieldHintText,
    MDTextFieldMaxLengthText,
)
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.metrics import dp
from typing import Callable, Optional


class LoginDialog(MDFloatLayout):
    """Login dialog for connecting to the chat server."""
    
    def __init__(self, connect_callback: Callable[[str, str], None], **kwargs):
        super().__init__(**kwargs)
        self.connect_callback = connect_callback
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the login dialog UI."""
        self.size_hint = (1, 1)
        self.md_bg_color = (0, 0, 0, 0.7)  # Semi-transparent overlay
        
        # Create login card
        self.login_card = self.create_login_card()
        self.add_widget(self.login_card)
    
    def create_login_card(self) -> MDCard:
        """Create the main login card."""
        login_card = MDCard(
            size_hint=(None, None),
            size=(dp(400), dp(350)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            padding=dp(30),
            orientation="vertical",
            spacing=dp(20)
        )
        
        # Add title
        title_label = self.create_title_label()
        login_card.add_widget(title_label)
        
        # Add input fields
        self.username_input = self.create_username_input()
        self.ip_input = self.create_ip_input()
        login_card.add_widget(self.username_input)
        login_card.add_widget(self.ip_input)
        
        # Add connect button
        connect_button_container = self.create_connect_button()
        login_card.add_widget(connect_button_container)
        
        return login_card
    
    def create_title_label(self) -> MDLabel:
        """Create the dialog title label."""
        return MDLabel(
            text="Join Chat Server",
            theme_text_color="Primary",
            font_style="Title",
            role="large",
            size_hint_y=None,
            height=dp(40),
            halign="center"
        )
    
    def create_username_input(self) -> MDTextField:
        """Create the username input field."""
        return MDTextField(
            MDTextFieldLeadingIcon(
                icon="account",
                theme_icon_color="Custom",
                icon_color_focus="#CBC3E3",
            ),
            MDTextFieldHintText(
                text="Username",
                text_color_normal="darkgrey",
            ),
            MDTextFieldMaxLengthText(
                max_text_length=128,
            ),
        )
    
    def create_ip_input(self) -> MDTextField:
        """Create the IP address input field."""
        return MDTextField(
            MDTextFieldLeadingIcon(
                icon="ip",
                theme_icon_color="Custom",
                icon_color_focus="#CBC3E3",
            ),
            MDTextFieldHintText(
                text="Server IP address",
                text_color_normal="darkgrey",
            ),
            MDTextFieldMaxLengthText(
                max_text_length=15,
            ),
        )
    
    def create_connect_button(self) -> MDAnchorLayout:
        """Create the connect button with proper layout."""
        connect_button = MDButton(
            MDButtonIcon(
                icon="transit-connection-variant",
            ),
            MDButtonText(
                text="Connect",
            ),
            style="filled",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.on_connect_pressed
        )
        
        # Wrap button in anchor layout for proper positioning
        anchor_layout = MDAnchorLayout(
            anchor_x="center",
            size_hint_y=None,
            height=dp(50)
        )
        anchor_layout.add_widget(connect_button)
        
        return anchor_layout
    
    def on_connect_pressed(self, instance):
        """Handle connect button press."""
        username = self.get_username()
        host = self.get_host()
        
        if self.validate_inputs(username, host):
            self.connect_callback(username, host)
    
    def get_username(self) -> str:
        """Get the entered username."""
        return self.username_input.text.strip()
    
    def get_host(self) -> str:
        """Get the entered host IP."""
        return self.ip_input.text.strip()
    
    def validate_inputs(self, username: str, host: str) -> bool:
        """Validate the input fields."""
        if not username:
            self.show_error("Please enter a username")
            return False
        
        if not host:
            self.show_error("Please enter a server IP address")
            return False
        
        # Basic IP validation (you can make this more robust)
        if not self.is_valid_ip_format(host):
            self.show_error("Please enter a valid IP address")
            return False
        
        return True
    
    def is_valid_ip_format(self, ip: str) -> bool:
        """Basic IP format validation."""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        
        try:
            for part in parts:
                num = int(part)
                if not 0 <= num <= 255:
                    return False
            return True
        except ValueError:
            return False
    
    def show_error(self, message: str):
        """Show error message to user."""
        # You can implement this with a snackbar or dialog
        print(f"Login Error: {message}")  # Placeholder
    
    def clear_inputs(self):
        """Clear all input fields."""
        self.username_input.text = ""
        self.ip_input.text = ""
    
    def set_default_values(self, username: str = "", host: str = "127.0.0.1"):
        """Set default values for the input fields."""
        if username:
            self.username_input.text = username
        if host:
            self.ip_input.text = host
    
    def focus_username_input(self):
        """Focus on the username input field."""
        self.username_input.focus = True


class LoginDialogManager:
    """Manager class for handling login dialog operations."""
    
    def __init__(self, parent_screen, connect_callback: Callable[[str, str], None]):
        self.parent_screen = parent_screen
        self.connect_callback = connect_callback
        self.dialog: Optional[LoginDialog] = None
    
    def show_login(self, default_username: str = "", default_host: str = "192.168.0.125"):
        """Show the login dialog."""
        if self.dialog is None:
            self.dialog = LoginDialog(self.on_connect_requested)
            self.dialog.set_default_values(default_username, default_host)
        
        self.parent_screen.add_widget(self.dialog)
        #self.dialog.focus_username_input()
    
    def hide_login(self):
        """Hide the login dialog."""
        if self.dialog and self.dialog.parent:
            self.parent_screen.remove_widget(self.dialog)
    
    def on_connect_requested(self, username: str, host: str):
        """Handle connection request from dialog."""
        # Call the actual connect callback
        success = self.connect_callback(username, host)
        
        # Hide dialog on successful connection
        if success:
            self.hide_login()
    
    def cleanup(self):
        """Cleanup resources."""
        self.hide_login()
        self.dialog = None