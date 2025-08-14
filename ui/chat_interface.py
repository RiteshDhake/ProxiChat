"""
Updated version of chat_interface.py with proper EnhancedSidebar integration.
Key changes:
1. Remove duplicate sidebar creation methods
2. Properly use EnhancedSidebar from sidebar.py
3. Connect all sidebar methods correctly
4. Fix user management functionality
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText,MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldLeadingIcon,
    MDTextFieldHintText,
    MDTextFieldMaxLengthText,
)
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.divider import MDDivider
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line,Scale,Rotate
from typing import Optional, Callable, List
from kivy.properties import NumericProperty
from kivy.uix.image import Image

import os
import time

# Import your enhanced components
from .components import MessageCard, MessageContainer, ChatHeader, MessageInputCard
from .login_dialog import LoginDialogManager
from .sidebar import EnhancedSidebar


class ModernChatInterface(MDScreen):
    """Modern chat interface with enhanced visual design."""
    logo_scale_value = NumericProperty(1.0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username: Optional[str] = None
        self.app_theme_cls = None
        self.send_message_callback: Optional[Callable[[str], None]] = None
        self.send_file_callback: Optional[Callable[[str], None]] = None
        self.connect_callback: Optional[Callable[[str, str], bool]] = None
        self._active_users: List[str] = []
        self.app_logo = None
        self.logo_scale = None
        
        # Set dark theme background
        self.md_bg_color = [0.03, 0.03, 0.05, 1.0]
        
        # Initialize file manager
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_file,
            preview=True,
        )
        
        self.setup_interface()
    
    def setup_interface(self):
        """Setup the modern interface layout."""
        # Main container
        self.main_layout = MDBoxLayout(orientation="vertical")
        self.add_widget(self.main_layout)
        
        # Enhanced app bar
        self.create_modern_app_bar()
        
        # Main content with improved layout
        self.create_modern_content()
        
        # Initialize login dialog
        self.login_manager = LoginDialogManager(self, self.on_connect_requested)
    
    def create_modern_app_bar(self):
        """Create modern app bar with status indicators."""
        # App bar container
        app_bar_container = MDCard(
            size_hint_y=None,
            height=dp(75),
            radius=[0, 0, 0, 0],
            md_bg_color=[0.08, 0.08, 0.12, 1.0],
            elevation=6
        )
        
        # App bar layout
        app_bar_layout = MDBoxLayout(
            orientation="horizontal",
            padding=[dp(24), dp(16), dp(24), dp(16)],
            spacing=dp(20)
        )
        
        # Left side - Logo and title
        left_section = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(16),
            size_hint_x=0.6
        )
        
        self.app_logo = Image(
                source="/Users/riteshdhake/Documents/Chatting_app/chatting_code/logo.png",
                size_hint=(None, None),
                size=(dp(45), dp(45)),
                allow_stretch=True,
                keep_ratio=True
            )
        
        # Title section
        title_section = MDBoxLayout(
            orientation="vertical",
            spacing=dp(2)
        )
        
        app_title = MDLabel(
            text="Chattr",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(26),
            bold=True
        )
        
        app_subtitle = MDLabel(
            text="Modern Desktop Chat",
            theme_text_color="Custom",
            text_color=[0.6, 0.6, 0.7, 1],
            font_size=sp(13)
        )
        
        title_section.add_widget(app_title)
        title_section.add_widget(app_subtitle)
        
        left_section.add_widget(self.app_logo)
        left_section.add_widget(title_section)
        
        # Right side - Status and info
        right_section = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(16),
            size_hint_x=0.4,
        )
        
        # Connection status
        status_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_x=None,
            width=dp(120)
        )
        
        self.status_indicator = MDCard(
            size_hint=(None, None),
            size=(dp(10), dp(10)),
            radius=[dp(5)],
            md_bg_color=[0.5, 0.5, 0.5, 1],  # Gray when disconnected
            pos_hint={"center_y": 0.5}
        )
        
        self.status_label = MDLabel(
            text="Offline",
            theme_text_color="Custom",
            text_color=[0.6, 0.6, 0.6, 1],
            font_size=sp(12),
            halign="center"
        )
        
        status_layout.add_widget(self.status_indicator)
        status_layout.add_widget(self.status_label)
        
        # User count indicator
        self.user_count_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(6),
            size_hint_x=None,
            width=dp(80)
        )
        
        users_icon = MDIconButton(
            icon = "account-group",
            size_hint_x=None,
            width=dp(20),
        )
        
        self.user_count_label = MDLabel(
            text="0",
            theme_text_color="Custom",
            text_color=[0.6, 0.6, 0.6, 1],
            font_size=sp(14),
            bold=True
        )
        
        self.user_count_layout.add_widget(users_icon)
        self.user_count_layout.add_widget(self.user_count_label)
        
        right_section.add_widget(status_layout)
        right_section.add_widget(self.user_count_layout)
        
        app_bar_layout.add_widget(left_section)
        app_bar_layout.add_widget(right_section)
        
        app_bar_container.add_widget(app_bar_layout)
        self.main_layout.add_widget(app_bar_container)
        
        self.setup_logo_transform()
        # Start the logo animation after the widget is fully built
        Clock.schedule_once(lambda dt: self.start_logo_animation(), 0.5)
    

    def setup_logo_transform(self):
        """Setup for logo opacity animation."""
        # No special setup needed for opacity animation
        # The logo widget already has opacity property
        pass

    def start_logo_animation(self):
        """Start logo pulsing animation using opacity."""
        if self.app_logo:
            # Animate the opacity property of the logo widget
            pulse = Animation(opacity=0.6, duration=1, t='in_out_sine') + \
                    Animation(opacity=1.0, duration=1, t='in_out_sine')
            pulse.repeat = True
            # Start the animation on the logo widget itself
            pulse.start(self.app_logo)

    def update_logo_transform(self, *args):
        """No longer needed for opacity-based animation."""
        # This method is no longer required since we're not using scale transforms
        pass    
    
    def create_modern_content(self):
        """Create modern content layout."""
        content_container = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, 1),
            spacing=dp(2)
        )
        self.main_layout.add_widget(content_container)
        
        # Use Enhanced sidebar from sidebar.py
        self.sidebar = EnhancedSidebar()
        content_container.add_widget(self.sidebar)
        
        # Separator line
        separator = MDCard(
            size_hint_x=None,
            width=dp(1),
            md_bg_color=[0.2, 0.2, 0.25, 0.5]
        )
        content_container.add_widget(separator)
        
        # Enhanced chat area
        self.chat_area = self.create_modern_chat_area()
        content_container.add_widget(self.chat_area)
    
    def create_modern_chat_area(self) -> MDBoxLayout:
        """Create modern chat area with improved styling."""
        chat_area = MDBoxLayout(
            orientation="vertical",
            size_hint_x=0.68,
            spacing=dp(0)
        )
        
        # Chat container
        chat_container = MDCard(
            md_bg_color=[0.05, 0.05, 0.08, 1.0],
            radius=[0, 0, 0, 0],
            elevation=2
        )
        
        chat_layout = MDBoxLayout(orientation="vertical")
        
        # Enhanced chat header
        self.chat_header = self.create_enhanced_chat_header()
        chat_layout.add_widget(self.chat_header)
        
        # Messages area
        self.create_modern_messages_area(chat_layout)
        
        # Input area
        self.create_modern_input_area(chat_layout)
        
        chat_container.add_widget(chat_layout)
        chat_area.add_widget(chat_container)
        
        return chat_area
    
    def create_enhanced_chat_header(self) -> MDCard:
        """Create enhanced chat header with modern styling."""
        header_card = MDCard(
            size_hint_y=None,
            height=dp(70),
            radius=[0, 0, 0, 0],
            md_bg_color=[0.08, 0.08, 0.12, 1.0],
            elevation=2
        )
        
        header_layout = MDBoxLayout(
            orientation="horizontal",
            padding=[dp(24), dp(16), dp(24), dp(16)],
            spacing=dp(16)
        )
        
        # Chat icon and title
        chat_icon = MDIconButton(
            icon = "chat",
            style = "tonal",
            font_size=sp(28),
            size_hint_x=None,
            width=dp(40)
        )
        
        title_section = MDBoxLayout(
            orientation="vertical",
            spacing=dp(2)
        )
        
        chat_title = MDLabel(
            text="General Chat",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(20),
            bold=True
        )
        
        title_section.add_widget(chat_title)
        
        # Right side info
        info_section = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_x=None,
            width=dp(100)
        )
        
        # Active indicator
        active_indicator = MDCard(
            size_hint=(None, None),
            size=(dp(6), dp(6)),
            radius=[dp(3)],
            md_bg_color=[0, 1, 0, 1]
        )
        
        active_label = MDLabel(
            text="Active",
            theme_text_color="Custom",
            text_color=[0, 1, 0, 1],
            font_size=sp(12),
            bold=True
        )
        
        info_section.add_widget(active_indicator)
        info_section.add_widget(active_label)
        
        chat_icon.disabled = True
        chat_icon.disabled_color="white"
        header_layout.add_widget(chat_icon)
        header_layout.add_widget(title_section)
        header_layout.add_widget(MDLabel())  # Spacer
        header_layout.add_widget(info_section)
        
        header_card.add_widget(header_layout)
        return header_card
    
    def create_modern_messages_area(self, parent_layout: MDBoxLayout):
        """Create modern messages area with enhanced scrolling."""
        # Messages background
        messages_container = MDCard(
            md_bg_color=[0.03, 0.03, 0.06, 1.0],
            radius=[0, 0, 0, 0],
            size_hint=(1, 1)
        )
        
        # Enhanced scroll view
        self.chat_scroll = MDScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=['bars', 'content'],
            bar_width=dp(6),
            bar_color=[0.2, 0.6, 1.0, 0.7],
            bar_inactive_color=[0.3, 0.3, 0.4, 0.4]
        )
        
        # Messages layout with better spacing
        self.chat_messages_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            adaptive_height=True,
            padding=[dp(20), dp(20), dp(20), dp(20)]
        )
        
        # Add welcome placeholder
        self.add_welcome_placeholder()
        
        self.chat_scroll.add_widget(self.chat_messages_layout)
        messages_container.add_widget(self.chat_scroll)
        parent_layout.add_widget(messages_container)
    
    def add_welcome_placeholder(self):
        """Add welcome placeholder when chat is empty."""
        placeholder_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            size_hint_y=None,
            height=dp(200),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        # Welcome icon
        welcome_icon = MDLabel(
            text="🚀",
            font_size=sp(64),
            halign="center",
            size_hint_y=None,
            height=dp(80)
        )
        
        # Welcome text
        welcome_text = MDLabel(
            text="Welcome to Chattr!",
            theme_text_color="Custom",
            text_color=[0.8, 0.8, 0.8, 1],
            font_size=sp(24),
            bold=True,
            halign="center",
            size_hint_y=None,
            height=dp(32)
        )
        
        # Subtitle
        welcome_subtitle = MDLabel(
            text="Connect to start chatting with others",
            theme_text_color="Custom",
            text_color=[0.5, 0.5, 0.6, 1],
            font_size=sp(14),
            halign="center",
            size_hint_y=None,
            height=dp(20)
        )
        
        placeholder_layout.add_widget(welcome_icon)
        placeholder_layout.add_widget(welcome_text)
        placeholder_layout.add_widget(welcome_subtitle)
        
        self.welcome_placeholder = placeholder_layout
        self.chat_messages_layout.add_widget(placeholder_layout)
    
    def create_modern_input_area(self, parent_layout: MDBoxLayout):
        """Create modern message input area."""
        input_container = MDCard(
            size_hint_y=None,
            height=dp(90),
            radius=[0, 0, 0, 0],
            md_bg_color=[0.08, 0.08, 0.12, 1.0],
            elevation=6
        )
        
        input_layout = MDBoxLayout(
            orientation="horizontal",
            padding=[dp(24), dp(20), dp(24), dp(20)],
            spacing=dp(16)
        )
        
        # Enhanced text input
        self.message_input = MDTextField(
            MDTextFieldHintText(
                text="Enter Your Message Here",
                text_color_normal=[0.6, 0.6, 0.6, 1],
                text_color_focus=[0.8, 0.8, 0.8, 1],
            ),
            mode="outlined",
            line_color_normal=[0.3, 0.3, 0.4, 1],
            line_color_focus=[0.2, 0.6, 1.0, 1],
            text_color_normal=[1, 1, 1, 1],
            text_color_focus=[1, 1, 1, 1],
            fill_color_normal=[0.08, 0.08, 0.1, 1],
            fill_color_focus=[0.1, 0.1, 0.12, 1]
        )
        
        # Enhanced buttons with better styling
        self.file_button = MDButton(
            MDButtonIcon(
                icon="paperclip",
                theme_icon_color="Custom",
                icon_color=[1, 1, 1, 1]
            ),
            
            size_hint_x=None,
            width=dp(60),
            height=dp(50),
            theme_bg_color="Custom",
            md_bg_color=[0.15, 0.15, 0.2, 1],
            on_release=self.on_send_file
        )
        
        
        
        self.send_button = MDButton(
            MDButtonIcon(
                icon="send",
                theme_icon_color="Custom",
                icon_color=[1, 1, 1, 1],
                pos_hint={"center_x": 0.5, "center_y": 0.5},
            ),
            size_hint_x=None,
            width=dp(80),
            height=dp(50),
            theme_bg_color="Custom",
            md_bg_color=[0.2, 0.6, 1.0, 1],

            radius=[dp(25)],
            on_release=self.on_send_message_btn
        )
        
        
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(self.send_button)
        input_layout.add_widget(self.file_button)
        
        input_container.add_widget(input_layout)
        parent_layout.add_widget(input_container)
        
        # Initially disable
        self.set_input_enabled(False)
        
        # Bind Enter key
        self.message_input.bind(on_text_validate=self.on_enter_pressed)
    
    # Enhanced callback methods
    def set_callbacks(self, send_message_callback: Callable[[str], None],
                     send_file_callback: Callable[[str], None],
                     connect_callback: Callable[[str, str], bool]):
        """Set callback functions."""
        self.send_message_callback = send_message_callback
        self.send_file_callback = send_file_callback
        self.connect_callback = connect_callback
    
    def show_login_dialog(self, default_username: str = "", default_host: str = "192.168.0.125"):
        """Show enhanced login dialog."""
        self.login_manager.show_login(default_username, default_host)
    
    def on_connect_requested(self, username: str, host: str) -> bool:
        """Handle connection with enhanced visual feedback."""
        if self.connect_callback:
            success = self.connect_callback(username, host)
            if success:
                self.username = username
                self.update_connection_status(True)
                # Use sidebar's update_user_info method
                self.sidebar.update_user_info(username, "Online")
                self.set_input_enabled(True)
                self.remove_welcome_placeholder()
                self.add_enhanced_system_message("Connected to server successfully!", "success")
                self.animate_successful_connection()
            else:
                self.add_enhanced_system_message(" Failed to connect to server", "error")
            return success
        return False
    
    def update_connection_status(self, connected: bool):
        """Update connection status with animations."""
        if connected:
            # Update app bar status
            self.status_indicator.md_bg_color = [0, 1, 0, 1]
            self.status_label.text = "Online"
            self.status_label.text_color = [0, 1, 0, 1]
            
            # Pulse animation (now uses opacity)
            pulse = Animation(opacity=0.5, duration=0.3)
            pulse += Animation(opacity=1, duration=0.3)
            pulse.start(self.status_indicator)
            
        else:
            self.status_indicator.md_bg_color = [0.5, 0.5, 0.5, 1]
            self.status_label.text = "Offline"
            self.status_label.text_color = [0.6, 0.6, 0.6, 1]
    
    def animate_successful_connection(self):
        """Animate successful connection."""
        # Chat area slide in
        original_x = self.chat_area.x
        self.chat_area.x = original_x + dp(100)
        self.chat_area.opacity = 0.5
        
        slide_anim = Animation(
            x=original_x,
            opacity=1,
            duration=0.6,
            t='out_back'
        )
        slide_anim.start(self.chat_area)
        # Get the original position of the logo
        original_pos = self.app_logo.pos
        
        # Wiggle animation (moves slightly left and right)
        wiggle_anim = Animation(x=original_pos[0] - dp(5), duration=0.1)
        wiggle_anim += Animation(x=original_pos[0] + dp(5), duration=0.1)
        wiggle_anim += Animation(x=original_pos[0] - dp(3), duration=0.1)
        wiggle_anim += Animation(x=original_pos[0] + dp(3), duration=0.1)
        wiggle_anim += Animation(x=original_pos[0], duration=0.1)
        
        # Opacity pulse
        pulse_anim = Animation(opacity=0.5, duration=0.2)
        pulse_anim += Animation(opacity=1.0, duration=0.2)
        pulse_anim += Animation(opacity=0.7, duration=0.2)
        pulse_anim += Animation(opacity=1.0, duration=0.2)
        
        # Start both animations
        wiggle_anim.start(self.app_logo)
        pulse_anim.start(self.app_logo)
    
    def remove_welcome_placeholder(self):
        """Remove welcome placeholder with fade animation."""
        if hasattr(self, 'welcome_placeholder') and self.welcome_placeholder.parent:
            fade_out = Animation(opacity=0, duration=0.5)
            fade_out.bind(
                on_complete=lambda *x: self.chat_messages_layout.remove_widget(self.welcome_placeholder)
            )
            fade_out.start(self.welcome_placeholder)
    
    def set_input_enabled(self, enabled: bool):
        """Enable/disable input with visual feedback."""
        self.message_input.disabled = not enabled
        self.send_button.disabled = not enabled
        self.file_button.disabled = not enabled
        
        if enabled:
            self.message_input.fill_color_normal = [0.12, 0.12, 0.16, 1]
            self.send_button.md_bg_color = [0.2, 0.6, 1.0, 1]
            self.file_button.md_bg_color = [0.15, 0.15, 0.2, 1]
            
            # Gentle glow animation
            glow = Animation(
                line_color_focus=[0.3, 0.7, 1.0, 1],
                duration=0.3
            )
            glow.start(self.message_input)
        else:
            self.message_input.fill_color_normal = [0.08, 0.08, 0.1, 1]
            self.send_button.md_bg_color = [0.2, 0.2, 0.25, 1]
            self.file_button.md_bg_color = [0.2, 0.2, 0.25, 1]
    
    def on_enter_pressed(self, instance):
        """Handle Enter key press."""
        if not self.send_button.disabled:
            self.on_send_message_btn(None)
    
    def on_send_message_btn(self, instance):
        """Handle send button with enhanced animation."""
        message = self.message_input.text.strip()
        if message and self.send_message_callback:
            # Button press animation
            press_anim = Animation(opacity=0.5, duration=0.1)
            press_anim += Animation(opacity=1, duration=0.1)
            press_anim.start(self.send_button)
            
            self.send_message_callback(message)
            self.message_input.text = ""
            self.message_input.focus = True
    
    def on_send_message(self, message: str):
        """Handle sending message."""
        if self.send_message_callback:
            self.send_message_callback(message)
    
    def on_send_file(self, instance=None):
        """Handle file sending."""
        # Button animation
        if instance:
            press_anim = Animation(opacity=0.5, duration=0.1)
            press_anim += Animation(opacity=1, duration=0.1)
            press_anim.start(self.file_button)
        
        self.show_file_manager()
    
    def display_message(self, username: str, content: str):
        """Display message with error handling."""
        try:
            is_own_message = username == self.username
            
            # Ensure theme_cls is not None
            theme_cls = self.app_theme_cls if hasattr(self, 'app_theme_cls') else self.theme_cls
            
            message_card = MessageCard(
                username=username,
                content=content,
                is_own_message=is_own_message,
                chat_width=getattr(self.chat_messages_layout, 'width', 400)
            )
            
            container = MessageContainer(message_card, is_own_message)
            self.chat_messages_layout.add_widget(container)
            Clock.schedule_once(lambda dt: self.smooth_scroll_to_bottom(), 0.15)
            
            # Animate user activity in sidebar
            if username != self.username:
                self.sidebar.animate_user_activity(username)
            
        except Exception as e:
            print(f"Message display error: {e}")
    
    def add_enhanced_system_message(self, message: str, msg_type: str = "info"):
        color_map = {
            "info": [0.2, 0.6, 1.0, 0.9],
            "success": [0.2, 0.8, 0.2, 0.9],
            "error": [1.0, 0.3, 0.3, 0.9],
            "warning": [1.0, 0.7, 0.2, 0.9]
        }
        
        system_card = MDCard(
            size_hint=(0.7, None),
            height=dp(45),
            pos_hint={"center_x": 0.5},
            padding=[dp(20), dp(12), dp(20), dp(12)],
            radius=[dp(22)],
            theme_bg_color="Custom",
            md_bg_color=color_map.get(msg_type, [0.5, 0.5, 0.5, 0.9]),
            elevation=2
        )
        
        msg_label = MDLabel(
            text=message,
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(14),
            bold=True
        )
        
        system_card.add_widget(msg_label)
        
        # Container for proper spacing
        container = MDBoxLayout(
            size_hint_y=None,
            height=dp(55),
            padding=[dp(0), dp(8), dp(0), dp(8)]
        )
        container.add_widget(system_card)
        
        self.chat_messages_layout.add_widget(container)
        
        # Entrance animation
        system_card.opacity = 0
        
        entrance_anim = Animation(
            opacity=1,
            duration=0.4,
            t='out_cubic'
        )
        entrance_anim.start(system_card)
        
        Clock.schedule_once(lambda dt: self.smooth_scroll_to_bottom(), 0.1)
    
    def add_active_user(self, username: str):
        """Add user to active list - USES SIDEBAR METHOD."""
        if username not in self._active_users:
            self._active_users.append(username)
            self.sidebar.add_active_user(username)
            self.update_app_bar_user_count()
    
    def remove_active_user(self, username: str):
        """Remove user from active list - USES SIDEBAR METHOD."""
        if username in self._active_users:
            self._active_users.remove(username)
            self.sidebar.remove_active_user(username)
            self.update_app_bar_user_count()
    
    def update_app_bar_user_count(self):
        """Update the user count in the app bar."""
        count = len(self._active_users)
        self.user_count_label.text = str(count)
        
        if count > 0:
            self.user_count_label.text_color = [0, 1, 0, 1]  # Green when users online
        else:
            self.user_count_label.text_color = [0.6, 0.6, 0.6, 1]  # Gray when no users
    
    def smooth_scroll_to_bottom(self):
        """Smooth animated scroll to bottom."""
        if self.chat_messages_layout.children:
            scroll_anim = Animation(
                scroll_y=0,
                duration=0.3,
                t='out_cubic'
            )
            scroll_anim.start(self.chat_scroll)
    
    def show_file_manager(self):
        """Show file manager."""
        self.file_manager.show(os.path.expanduser("~"))
    
    def exit_file_manager(self, *args):
        """Exit file manager."""
        self.file_manager.close()
    
    def select_file(self, path: str):
        """Handle file selection."""
        self.exit_file_manager()
        filename = os.path.basename(path)
        self.add_enhanced_system_message(f"📎 Sending file: {filename}", "info")
        
        if self.send_file_callback:
            self.send_file_callback(path)
    
    def disconnect_cleanup(self):
        """Enhanced disconnect cleanup."""
        self.set_input_enabled(False)
        self.update_connection_status(False)
        # Use sidebar method to reset user info
        self.sidebar.reset_sidebar()
        self._active_users.clear()
        self.update_app_bar_user_count()
        self.username = None
        self.add_enhanced_system_message("🔌 Disconnected from server", "warning")
    
    def on_file_received(self, filename: str):
        """Handle file received."""
        self.add_enhanced_system_message(f"📥 File received: {filename}", "success")
    
    def user_joined(self, username: str):
        """Handle user joined with animation - USES SIDEBAR METHOD."""
        print(f"DEBUG: User joined called with username: {username}")  # Debug print
        self.add_enhanced_system_message(f" {username} joined the chat", "info")
        self.add_active_user(username)  # This calls sidebar.add_active_user()
        print(f"DEBUG: Active users after join: {self._active_users}")  # Debug print
    
    def user_left(self, username: str):
        """Handle user left with animation - USES SIDEBAR METHOD."""
        print(f"DEBUG: User left called with username: {username}")  # Debug print
        self.add_enhanced_system_message(f" {username} left the chat", "warning")
        self.remove_active_user(username)  # This calls sidebar.remove_active_user()
        print(f"DEBUG: Active users after leave: {self._active_users}")  # Debug print
    
    def update_user_list(self, users: List[str]):
        """Update the entire user list - USES SIDEBAR METHOD."""
        print(f"DEBUG: Updating user list with: {users}")  # Debug print
        self._active_users = users.copy()
        
        # Clear sidebar and repopulate
        self.sidebar.clear_users_list()
        for user in users:
            self.sidebar.add_active_user(user)
        
        self.update_app_bar_user_count()
    
    def set_active_users(self, users: List[str]):
        """Set the active users list - USES SIDEBAR METHOD."""
        print(f"DEBUG: Setting active users to: {users}")  # Debug print
        self._active_users = users.copy()
        
        # Update sidebar's internal list and display
        self.sidebar.active_users = users.copy()
        self.sidebar.update_users_display()
        
        self.update_app_bar_user_count()
    
    # Utility methods
    def get_current_username(self) -> Optional[str]:
        return self.username
    
    def is_connected(self) -> bool:
        return self.username is not None
    
    def get_online_users(self) -> List[str]:
        return self._active_users.copy()
    
    def get_online_user_count(self) -> int:
        return len(self._active_users)
    
    def clear_chat(self):
        """Clear chat with fade animation."""
        for child in self.chat_messages_layout.children[:]:
            fade_anim = Animation(opacity=0, duration=0.3)
            fade_anim.bind(
                on_complete=lambda fade_anim, widget=child: self.chat_messages_layout.remove_widget(widget)
            )
            fade_anim.start(child)
    
    def focus_message_input(self):
        """Focus message input."""
        if hasattr(self, 'message_input'):
            self.message_input.focus = True
    
    # New methods to properly integrate with EnhancedSidebar
    def update_sidebar_user_info(self, username: str, status: str = "Online"):
        """Update sidebar user information."""
        self.sidebar.update_user_info(username, status)
    
    def get_sidebar_user_count(self) -> int:
        """Get user count from sidebar."""
        return self.sidebar.get_user_count()
    
    def get_sidebar_users(self) -> List[str]:
        """Get users list from sidebar."""
        return self.sidebar.get_active_users()
    
    def animate_sidebar_user_activity(self, username: str):
        """Animate user activity in sidebar."""
        self.sidebar.animate_user_activity(username)
    
    def set_sidebar_user_offline(self):
        """Set current user as offline in sidebar."""
        if self.username:
            self.sidebar.set_user_offline()
    
    def set_sidebar_user_online(self, username: str):
        """Set current user as online in sidebar."""
        self.sidebar.set_user_online(username)
    
    def update_sidebar_connection_time(self):
        """Update connection time in sidebar."""
        self.sidebar.update_connection_time()


# Color scheme constants for consistent theming
class ModernTheme:
    """Modern dark theme color scheme."""
    
    # Background colors
    MAIN_BG = [0.03, 0.03, 0.05, 1.0]
    SIDEBAR_BG = [0.06, 0.06, 0.09, 1.0]
    CHAT_BG = [0.05, 0.05, 0.08, 1.0]
    CARD_BG = [0.1, 0.1, 0.15, 1.0]
    INPUT_BG = [0.12, 0.12, 0.16, 1.0]
    
    # Accent colors
    PRIMARY = [0.2, 0.6, 1.0, 1.0]
    SUCCESS = [0.2, 0.8, 0.2, 1.0]
    ERROR = [1.0, 0.3, 0.3, 1.0]
    WARNING = [1.0, 0.7, 0.2, 1.0]
    
    # Text colors
    TEXT_PRIMARY = [1, 1, 1, 1]
    TEXT_SECONDARY = [0.8, 0.8, 0.8, 1]
    TEXT_TERTIARY = [0.6, 0.6, 0.7, 1]
    TEXT_DISABLED = [0.4, 0.4, 0.4, 1]
    
    # Border colors
    BORDER_NORMAL = [0.3, 0.3, 0.4, 1]
    BORDER_FOCUS = [0.2, 0.6, 1.0, 1]
    BORDER_ERROR = [1.0, 0.3, 0.3, 1]


# Usage example and integration guide
"""
ENHANCED INTEGRATION GUIDE:

KEY CHANGES MADE:
================

1. REMOVED DUPLICATE METHODS:
   - Removed create_modern_sidebar() method
   - Removed create_user_info_section() method  
   - Removed create_online_users_section() method
   - Removed update_users_display() method
   - Removed create_enhanced_user_item() method
   - All user management now handled by EnhancedSidebar

2. PROPER SIDEBAR INTEGRATION:
   - Direct instantiation: self.sidebar = EnhancedSidebar()
   - All user operations route through sidebar methods
   - Sidebar maintains its own user list and display

3. FIXED USER MANAGEMENT:
   - add_active_user() -> calls self.sidebar.add_active_user()
   - remove_active_user() -> calls self.sidebar.remove_active_user()
   - user_joined() -> calls add_active_user() which routes to sidebar
   - user_left() -> calls remove_active_user() which routes to sidebar
   - set_active_users() -> updates both local list and sidebar

4. NEW UTILITY METHODS:
   - update_sidebar_user_info()
   - get_sidebar_user_count()
   - get_sidebar_users()
   - animate_sidebar_user_activity()
   - set_sidebar_user_offline()
   - set_sidebar_user_online()
   - update_sidebar_connection_time()

5. ENHANCED FEATURES:
   - App bar user count syncs with sidebar
   - Connection status updates both app bar and sidebar
   - User activity animations work through sidebar
   - Proper cleanup on disconnect

HOW TO USE:
===========

1. Replace your chat_interface.py with this enhanced version
2. Make sure sidebar.py is in the same directory
3. Your server event handlers should call:

   ```python
   # When user joins
   chat_interface.user_joined(username)
   
   # When user leaves  
   chat_interface.user_left(username)
   
   # To set complete user list
   chat_interface.set_active_users(user_list)
   
   # To update user info
   chat_interface.update_sidebar_user_info(username, "Online")
   ```

4. The sidebar will automatically handle:
   - User list animations
   - Count updates
   - Empty state displays
   - User activity animations
   - Connection status displays

DEBUGGING:
==========

The code includes debug prints. Check console output to verify:
- user_joined() is called with correct username
- user_left() is called with correct username  
- Active users list is updated correctly
- Sidebar methods are being called

If users still don't appear, ensure your server code calls these methods
when handling client connections/disconnections.

BENEFITS:
=========

- Clean separation of concerns
- No code duplication
- Proper encapsulation
- Enhanced animations and visual feedback
- Consistent state management
- Easy to maintain and extend
"""