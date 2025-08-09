"""
Reusable UI components for the chat application.
"""

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from typing import Optional


class MessageCard(MDCard):
    """A card component for displaying chat messages."""
    
    def __init__(self, username: str, content: str, is_own_message: bool = False, 
                 theme_cls=None, chat_width: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.content = content
        self.is_own_message = is_own_message
        self.theme_cls = theme_cls
        self.chat_width = chat_width or dp(400)
        
        self.setup_card()
    
    def setup_card(self):
        """Setup the message card appearance and content."""
        self.size_hint_x = 0.7
        self.size_hint_y = None
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        
        # Set background color for own messages
        if self.is_own_message and self.theme_cls:
            try:
                self.md_bg_color = self.theme_cls.primary_color
            except AttributeError:
                # Fallback if primary_color is not available
                self.md_bg_color = (0.2, 0.4, 0.8, 1.0)  # Default blue
        
        # Create message text
        if self.is_own_message:
            msg_text = f"[b][color=00ffff]You:[/color][/b] {self.content}"
        else:
            msg_text = f"[b][color=ffff00]{self.username}:[/color][/b] {self.content}"
        
        # Calculate text width for wrapping
        text_width = self.chat_width * 0.7 - dp(30)
        
        msg_label = MDLabel(
            text=msg_text,
            size_hint_y=None,
            text_size=(text_width, None),
            valign="top",
            theme_text_color="Primary",
            font_style="Body",
            markup=True
        )
        
        # Bind texture_size to height for proper text wrapping
        msg_label.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        
        self.add_widget(msg_label)


class MessageContainer(MDBoxLayout):
    """Container for message cards with proper alignment."""
    
    def __init__(self, message_card: MessageCard, is_own_message: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.spacing = dp(10)
        self.padding = [dp(0), dp(5), dp(0), dp(5)]
        
        if is_own_message:
            # Add spacer to push message to the right
            spacer = MDLabel(size_hint_x=0.3)
            self.add_widget(spacer)
            self.add_widget(message_card)
        else:
            # Align messages from others to the left
            self.add_widget(message_card)


class UserListItem(MDBoxLayout):
    """A list item component for displaying online users."""
    
    def __init__(self, username: str, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.setup_user_item()
    
    def setup_user_item(self):
        """Setup the user list item."""
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(30)
        
        user_label = MDLabel(
            text=self.username,
            theme_text_color="Primary",
            font_style="Body",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.add_widget(user_label)


class UserInfoCard(MDCard):
    """Card component for displaying user information."""
    
    def __init__(self, username: str = "Not Connected", status: str = "Offline", **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.status = status
        self.setup_card()
    
    def setup_card(self):
        """Setup the user info card."""
        self.size_hint_y = None
        self.height = dp(100)
        self.padding = dp(15)
        self.orientation = "vertical"
        
        self.user_label = MDLabel(
            text=f"User: {self.username}" if self.username != "Not Connected" else self.username,
            theme_text_color="Primary",
            font_style="Title"
        )
        
        self.status_label = MDLabel(
            text=f"Status: {self.status}",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.add_widget(self.user_label)
        self.add_widget(self.status_label)
    
    def update_user_info(self, username: str, status: str):
        """Update user information."""
        self.username = username
        self.status = status
        self.user_label.text = f"User: {username}"
        self.status_label.text = f"Status: {status}"


class OnlineUsersCard(MDCard):
    """Card component for displaying online users list."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_card()
    
    def setup_card(self):
        """Setup the online users card."""
        self.padding = dp(15)
        self.orientation = "vertical"
        
        # Header
        online_label = MDLabel(
            text="Online Users",
            theme_text_color="Primary",
            font_style="Title",
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(online_label)
        
        # Scrollable users list
        from kivymd.uix.scrollview import MDScrollView
        self.users_scrollview = MDScrollView()
        self.users_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            adaptive_height=True,
            spacing=dp(5)
        )
        self.users_scrollview.add_widget(self.users_layout)
        self.add_widget(self.users_scrollview)
    
    def update_users_list(self, users_list: list):
        """Update the online users list."""
        self.users_layout.clear_widgets()
        for user in users_list:
            user_item = UserListItem(user)
            self.users_layout.add_widget(user_item)


class ChatHeader(MDBoxLayout):
    """Header component for the chat area."""
    
    def __init__(self, title: str = "General Chat", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.setup_header()
    
    def setup_header(self):
        """Setup the chat header."""
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        
        chat_title = MDLabel(
            text=self.title,
            theme_text_color="Primary",
            font_style="Title",
            role="large",
            size_hint_y=None,
            height=dp(40),
            halign="center"
        )
        
        self.add_widget(chat_title)


class MessageInputCard(MDCard):
    """Card component for message input area."""
    
    def __init__(self, send_callback=None, file_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.send_callback = send_callback
        self.file_callback = file_callback
        self.setup_input_card()
    
    def setup_input_card(self):
        """Setup the message input card."""
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.button import MDButton
        
        self.size_hint_y = None
        self.height = dp(70)
        self.padding = [dp(15), dp(10), dp(15), dp(10)]
        
        input_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10)
        )
        
        self.message_input = MDTextField(
            mode="outlined",
            hint_text="Type your message here...",
            size_hint_x=0.6,
            multiline=False
        )
        
        self.send_button = MDButton(
            size_hint_x=0.2,
            on_release=self.on_send_pressed
        )
        send_label = MDLabel(text="Send", halign="center")
        self.send_button.add_widget(send_label)
        
        self.file_button = MDButton(
            size_hint_x=0.2,
            on_release=self.on_file_pressed
        )
        file_label = MDLabel(text="File", halign="center")
        self.file_button.add_widget(file_label)
        
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(self.send_button)
        input_layout.add_widget(self.file_button)
        
        self.add_widget(input_layout)
        
        # Initially disable buttons
        self.set_enabled(False)
    
    def on_send_pressed(self, instance):
        """Handle send button press."""
        if self.send_callback:
            message = self.message_input.text.strip()
            if message:
                self.send_callback(message)
                self.message_input.text = ""
                self.message_input.focus = True
    
    def on_file_pressed(self, instance):
        """Handle file button press."""
        if self.file_callback:
            self.file_callback()
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the input components."""
        self.message_input.disabled = not enabled
        self.send_button.disabled = not enabled
        self.file_button.disabled = not enabled
    
    def get_message_text(self) -> str:
        """Get the current message text."""
        return self.message_input.text.strip()
    
    def clear_message(self):
        """Clear the message input."""
        self.message_input.text = ""
        self.message_input.focus = True