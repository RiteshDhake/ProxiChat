"""
Beautified UI components for the chat application with modern styling.
"""

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon, MDTextFieldHintText
from kivymd.uix.divider import MDDivider
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock
from typing import Optional
import time
from .constants import CHAT_AREA_WIDTH_RATIO, DEFAULT_PADDING

class MessageCard(MDCard):
    """Enhanced message card with modern styling and animations."""
    
    def __init__(self, username: str, content: str, is_own_message: bool = False, 
                  chat_width: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.content = content
        self.is_own_message = is_own_message

        self.chat_width = chat_width or dp(400)
        
        self.setup_card()
        self.animate_entrance()
    
    def setup_card(self):
        """Setup enhanced message card with modern styling."""
        self.size_hint_x = 0.75
        self.size_hint_y = None
        self.padding = [dp(16), dp(12), dp(16), dp(12)]
        self.radius = [dp(15), dp(15), dp(15), dp(5)] if not self.is_own_message else [dp(15), dp(15), dp(5), dp(15)]
        self.elevation = 2
        self.theme_bg_color = "Custom"
        
        # Enhanced color scheme
        if self.is_own_message:
            self.md_bg_color = [0.2, 0.6, 1.0, 1.0]  # Modern blue
        else:
            self.md_bg_color = [0.15, 0.15, 0.17, 1.0]  # Dark card background
        
        # Create message layout
        message_layout = MDBoxLayout(orientation="vertical", spacing=dp(4))
        
        # Username and timestamp header
        if not self.is_own_message:
            header_layout = MDBoxLayout(
                orientation="horizontal", 
                size_hint_y=None, 
                height=dp(20),
                spacing=dp(8)
            )
            
            username_label = MDLabel(
                text=f"[b][color=#FFD700]{self.username}[/color][/b]",
                font_size=sp(13),
                markup=True,
                size_hint_x=None,
                valign = "top",
                width=dp(100),
                theme_text_color="Custom",
                text_color=[1, 1, 1, 0.9]
            )
            
            timestamp_label = MDLabel(
                text=f"[color=#888888]{time.strftime('%H:%M')}[/color]",
                font_size=sp(11),
                markup=True,
                valign = "top",
                halign="right",
                theme_text_color="Custom",
                text_color=[0.5, 0.5, 0.5, 1]
            )
            
            header_layout.add_widget(username_label)
            header_layout.add_widget(timestamp_label)
            message_layout.add_widget(header_layout)
        
        # Message content
        text_width = self.chat_width * 0.75 - dp(32)
        
        if self.is_own_message:
            msg_text = self.content
            text_color = [1, 1, 1, 1]  # White text for own messages
        else:
            msg_text = self.content
            text_color = [0.9, 0.9, 0.9, 1]  # Light gray text for others
        
        msg_label = MDLabel(
           text=msg_text,
    size_hint_y=None,
    text_size=(text_width, None),
    valign="top",  # start at top
    halign="left",
    theme_text_color="Custom",
    text_color=text_color,
    font_size=sp(14),
    line_height=1.2
        )
        
        msg_label.bind(texture_size=lambda instance, size: setattr(instance, 'height', size[1]))
        message_layout.add_widget(msg_label)
        
        # Add timestamp for own messages at bottom
        if self.is_own_message:
            timestamp_label = MDLabel(
                text=f"[color=#CCCCCC]{time.strftime('%H:%M')}[/color]",
                font_size=sp(5),
                markup=True,
                halign="right",
                valign = "bottom",
                size_hint_y=None,
                height=dp(16),
                theme_text_color="Custom",
                text_color=[0.8, 0.8, 0.8, 1]
            )
            message_layout.add_widget(timestamp_label)
        
        self.add_widget(message_layout)
        message_layout.bind(minimum_height=lambda instance, value: setattr(self, 'height', value + dp(24)))  
    
    def animate_entrance(self):
        """Add entrance animation to message cards."""
        self.opacity = 0
        self.y -= dp(20)
        
        anim = Animation(opacity=1, y=self.y + dp(20), duration=0.3, t='out_cubic')
        anim.start(self)


class MessageContainer(MDBoxLayout):
    """Enhanced container for message cards with better alignment."""
    
    def __init__(self, message_card: MessageCard, is_own_message: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.spacing = dp(8)
        self.padding = [dp(12), dp(6), dp(12), dp(6)]
        
        if is_own_message:
            # Right align own messages
            spacer = MDLabel(size_hint_x=0.25)
            self.add_widget(spacer)
            self.add_widget(message_card)
        else:
            # Left align others' messages
            self.add_widget(message_card)
            spacer = MDLabel(size_hint_x=0.25)
            self.add_widget(spacer)


class UserInfoCard(MDCard):
    """Enhanced user info card with modern design."""
    
    def __init__(self, username: str = "Not Connected", status: str = "Offline", **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.status = status
        self.setup_card()
    
    def setup_card(self):
        """Setup enhanced user info card."""
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = dp(20)
        self.orientation = "vertical"
        self.radius = [dp(15)]
        self.elevation = 3
        self.md_bg_color = [0.1, 0.1, 0.12, 1.0]  # Dark background
        
        # User avatar placeholder (could be replaced with actual image)
        avatar_layout = MDBoxLayout(
            size_hint_y=None,
            height=dp(40),
            orientation="horizontal",
            spacing=dp(12)
        )
        
        avatar_placeholder = MDCard(
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            radius=[dp(20)],
            md_bg_color=[0.3, 0.3, 0.35, 1.0]
        )
        
        # Add user initial
        if self.username and self.username != "Not Connected":
            initial_label = MDLabel(
                text=self.username[0].upper(),
                halign="center",
                valign="middle",
                font_size=sp(18),
                bold=True,
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1]
            )
            avatar_placeholder.add_widget(initial_label)
        
        # User info layout
        user_info_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(2)
        )
        
        self.user_label = MDLabel(
            text=self.username if self.username != "Not Connected" else "Not Connected",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(16),
            bold=True
        )
        
        # Status with colored indicator
        status_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(20)
        )
        
        # Status dot
        self.status_dot = MDCard(
            size_hint=(None, None),
            size=(dp(8), dp(8)),
            radius=[dp(4)],
            md_bg_color=[0, 1, 0, 1] if self.status == "Online" else [0.5, 0.5, 0.5, 1]
        )
        
        self.status_label = MDLabel(
            text=self.status,
            theme_text_color="Custom",
            text_color=[0.8, 0.8, 0.8, 1],
            font_size=sp(13)
        )
        
        status_layout.add_widget(self.status_dot)
        status_layout.add_widget(self.status_label)
        
        user_info_layout.add_widget(self.user_label)
        user_info_layout.add_widget(status_layout)
        
        avatar_layout.add_widget(avatar_placeholder)
        avatar_layout.add_widget(user_info_layout)
        
        self.add_widget(avatar_layout)
    
    def update_user_info(self, username: str, status: str):
        """Update user information with animation."""
        self.username = username
        self.status = status
        
        # Animate status change
        if status == "Online":
            self.status_dot.md_bg_color = [0, 1, 0, 1]
        else:
            self.status_dot.md_bg_color = [0.5, 0.5, 0.5, 1]
        
        self.user_label.text = username if username != "Not Connected" else "Not Connected"
        self.status_label.text = status


class OnlineUsersCard(MDCard):
    """Enhanced online users card with modern styling."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_card()
    
    def setup_card(self):
        """Setup enhanced online users card."""
        self.padding = dp(20)
        self.orientation = "vertical"
        self.radius = [dp(15)]
        self.elevation = 3
        self.md_bg_color = [0.1, 0.1, 0.12, 1.0]
        self.spacing = dp(12)
        
        # Header with icon and count
        header_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(30),
            spacing=dp(8)
        )
        
        online_icon = MDLabel(
            text="●",
            font_size=sp(16),
            theme_text_color="Custom",
            text_color=[0, 1, 0, 1],
            size_hint_x=None,
            width=dp(20)
        )
        
        self.online_label = MDLabel(
            text="Online Users",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(16),
            bold=True
        )
        
        self.count_label = MDLabel(
            text="(0)",
            theme_text_color="Custom",
            text_color=[0.6, 0.6, 0.6, 1],
            font_size=sp(14),
            halign="right"
        )
        
        header_layout.add_widget(online_icon)
        header_layout.add_widget(self.online_label)
        header_layout.add_widget(self.count_label)
        
        self.add_widget(header_layout)
        
        # Divider
        divider = MDDivider(color=[0.3, 0.3, 0.35, 1])
        self.add_widget(divider)
        
        # Scrollable users list
        from kivymd.uix.scrollview import MDScrollView
        self.users_scrollview = MDScrollView(
            do_scroll_x=False
        )
        
        self.users_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            adaptive_height=True,
            spacing=dp(6)
        )
        
        self.users_scrollview.add_widget(self.users_layout)
        self.add_widget(self.users_scrollview)
    
    def update_users_list(self, users_list: list):
        """Update users list with enhanced user items."""
        self.users_layout.clear_widgets()
        
        for i, user in enumerate(users_list):
            user_item = EnhancedUserListItem(user)
            self.users_layout.add_widget(user_item)
            
            # Animate user items
            user_item.opacity = 0
            anim = Animation(
                opacity=1, 
                duration=0.2,
                delay=i * 0.05,  # Stagger animation
                t='out_cubic'
            )
            anim.start(user_item)
        
        # Update count
        self.count_label.text = f"({len(users_list)})"


class EnhancedUserListItem(MDBoxLayout):
    """Enhanced user list item with modern styling."""
    
    def __init__(self, username: str, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.setup_user_item()
    
    def setup_user_item(self):
        """Setup enhanced user item."""
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(40)
        self.spacing = dp(12)
        self.padding = [dp(8), dp(6), dp(8), dp(6)]
        
        # Add hover effect with card background
        self.card_bg = MDCard(
            md_bg_color=[0, 0, 0, 0],  # Transparent initially
            radius=[dp(8)],
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        # User avatar
        avatar = MDCard(
            size_hint=(None, None),
            size=(dp(28), dp(28)),
            radius=[dp(14)],
            md_bg_color=[0.3, 0.3, 0.35, 1.0]
        )
        
        initial_label = MDLabel(
            text=self.username[0].upper(),
            halign="center",
            valign="middle",
            font_size=sp(12),
            bold=True,
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]
        )
        avatar.add_widget(initial_label)
        
        # Username
        user_label = MDLabel(
            text=self.username,
            theme_text_color="Custom",
            text_color=[0.9, 0.9, 0.9, 1],
            font_size=sp(14)
        )
        
        # Online indicator
        online_dot = MDCard(
            size_hint=(None, None),
            size=(dp(6), dp(6)),
            radius=[dp(3)],
            md_bg_color=[0, 1, 0, 1]
        )
        
        # Layout
        content_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12)
        )
        
        content_layout.add_widget(avatar)
        content_layout.add_widget(user_label)
        
        spacer_layout = MDBoxLayout()
        spacer_layout.add_widget(MDLabel())  # Spacer
        spacer_layout.add_widget(online_dot)
        
        content_layout.add_widget(spacer_layout)
        
        self.add_widget(self.card_bg)
        self.add_widget(content_layout)


class ChatHeader(MDBoxLayout):
    """Enhanced chat header with modern styling."""
    
    def __init__(self, title: str = "General Chat", **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.setup_header()
    
    def setup_header(self):
        """Setup enhanced chat header."""
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(24), dp(16), dp(24), dp(16)]
        self.spacing = dp(16)
        
        # Chat icon
        chat_icon = MDLabel(
            text="💬",
            font_size=sp(24),
            size_hint_x=None,
            width=dp(40)
        )
        
        # Title and subtitle
        title_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(2)
        )
        
        chat_title = MDLabel(
            text=self.title,
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(20),
            bold=True
        )
        
        subtitle = MDLabel(
            text="Share your thoughts with everyone",
            theme_text_color="Custom",
            text_color=[0.6, 0.6, 0.6, 1],
            font_size=sp(12)
        )
        
        title_layout.add_widget(chat_title)
        title_layout.add_widget(subtitle)
        
        self.add_widget(chat_icon)
        self.add_widget(title_layout)
        
        # Add background gradient effect
        self.canvas.before.clear()
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.08, 0.08, 0.1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
    
    def update_bg(self, *args):
        """Update background rectangle."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class MessageInputCard(MDCard):
    """Enhanced message input card with modern styling."""
    
    def __init__(self, send_callback=None, file_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.send_callback = send_callback
        self.file_callback = file_callback
        self.setup_input_card()
    
    def setup_input_card(self):
        """Setup enhanced message input card."""
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = [dp(20), dp(16), dp(20), dp(16)]
        self.radius = [dp(0)]
        self.md_bg_color = [0.08, 0.08, 0.1, 1.0]
        self.elevation = 4
        
        input_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12)
        )
        
        # Enhanced text input
        self.message_input = MDTextField(
            MDTextFieldHintText(
                text="Type your message here...",
                text_color_normal=[0.6, 0.6, 0.6, 1],
            ),
            mode="filled",
            size_hint_x=0.75,
            multiline=False,
            fill_color_normal=[0.15, 0.15, 0.17, 1],
            fill_color_focus=[0.2, 0.2, 0.22, 1],
            line_color_normal=[0.3, 0.3, 0.35, 1],
            line_color_focus=[0.2, 0.6, 1.0, 1],
            text_color_normal=[1, 1, 1, 1],
            text_color_focus=[1, 1, 1, 1],
            cursor_color=[0.2, 0.6, 1.0, 1]
        )
        
        # Enhanced buttons
        self.send_button = MDButton(
            MDButtonIcon(icon="send", theme_icon_color="Custom", icon_color=[1, 1, 1, 1]),
            MDButtonText(text="Send", theme_text_color="Custom", text_color=[1, 1, 1, 1]),
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=[0.2, 0.6, 1.0, 1],
            size_hint_x=0.125,
            on_release=self.on_send_pressed
        )
        
        self.file_button = MDButton(
            MDButtonIcon(icon="attachment", theme_icon_color="Custom", icon_color=[1, 1, 1, 1]),
            MDButtonText(text="File", theme_text_color="Custom", text_color=[1, 1, 1, 1]),
            style="outlined",
            theme_bg_color="Custom",
            md_bg_color=[0, 0, 0, 0],
            line_color=[0.3, 0.3, 0.35, 1],
            size_hint_x=0.125,
            on_release=self.on_file_pressed
        )
        
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(self.file_button)
        input_layout.add_widget(self.send_button)
        
        self.add_widget(input_layout)
        
        # Initially disable buttons
        self.set_enabled(False)
        
        # Add keyboard shortcut for Enter key
        self.message_input.bind(on_text_validate=self.on_enter_pressed)
    
    def on_enter_pressed(self, instance):
        """Handle Enter key press."""
        if not self.send_button.disabled:
            self.on_send_pressed(None)
    
    def on_send_pressed(self, instance):
        if self.send_callback:
            message = self.message_input.text.strip()
            if message:
                # Button press animation using opacity
                anim = Animation(opacity=0.7, duration=0.1)
                anim += Animation(opacity=1, duration=0.1)
                anim.start(self.send_button)
                
                self.send_callback(message)
                self.message_input.text = ""
                self.message_input.focus = True
    
    def on_file_pressed(self, instance):
        if self.file_callback:
            # Opacity-based button press animation
            anim = Animation(opacity=0.7, duration=0.1)
            anim += Animation(opacity=1, duration=0.1)
            anim.start(self.file_button)
            
            self.file_callback()
    
    def set_enabled(self, enabled: bool):
        """Enable/disable input with visual feedback."""
        self.message_input.disabled = not enabled
        self.send_button.disabled = not enabled
        self.file_button.disabled = not enabled
        
        # Visual feedback
        if enabled:
            self.message_input.fill_color_normal = [0.15, 0.15, 0.17, 1]
            self.send_button.md_bg_color = [0.2, 0.6, 1.0, 1]
        else:
            self.message_input.fill_color_normal = [0.1, 0.1, 0.12, 1]
            self.send_button.md_bg_color = [0.3, 0.3, 0.35, 1]
    
    def get_message_text(self) -> str:
        """Get current message text."""
        return self.message_input.text.strip()
    
    def clear_message(self):
        """Clear message input."""
        self.message_input.text = ""
        self.message_input.focus = True


class SystemMessageCard(MDCard):
    """System message card for connection status, etc."""
    
    def __init__(self, message: str, msg_type: str = "info", **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.msg_type = msg_type
        self.setup_card()
    
    def setup_card(self):
        """FIXED: Setup system message card."""
        color_map = {
            "info": [0.2, 0.6, 1.0, 0.8],
            "success": [0.2, 0.8, 0.2, 0.8],
            "error": [1.0, 0.3, 0.3, 0.8],
            "warning": [1.0, 0.8, 0.2, 0.8]
        }
        
        self.size_hint = (0.6, None)
        self.height = dp(40)
        self.pos_hint = {"center_x": 0.5}
        self.padding = [dp(16), dp(8), dp(16), dp(8)]
        self.radius = [dp(20)]
        self.md_bg_color = color_map.get(self.msg_type, [0.5, 0.5, 0.5, 0.8])
        self.elevation = 1
        
        msg_label = MDLabel(
            text=self.message,
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(13),
            bold=True
        )
        
        self.add_widget(msg_label)
        
        
        self.opacity = 0
        
        
        # Use position-based animation instead
        original_y = self.y
        self.y -= dp(10)  # Start slightly above
        
        anim = Animation(
            opacity=1,
            y=original_y,
            duration=0.4,
            t='out_elastic'
        )
        anim.start(self)
