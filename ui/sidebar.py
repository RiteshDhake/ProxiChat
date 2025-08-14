"""
Enhanced sidebar component with modern design and animations.
This file replaces your existing sidebar.py
"""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.divider import MDDivider
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from typing import List, Optional
import time


class EnhancedSidebar(MDBoxLayout):
    """Modern sidebar with enhanced styling and animations."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_users: List[str] = []
        self.current_username: Optional[str] = None
        self.current_status: str = "Offline"
        self.setup_sidebar()
    
    def setup_sidebar(self):
        """Setup the modern sidebar layout."""
        self.orientation = "vertical"
        self.size_hint_x = 0.32
        self.spacing = dp(20)
        self.padding = [dp(20), dp(20), dp(16), dp(20)]
        
        # Gradient background
        with self.canvas.before:
            Color(0.06, 0.06, 0.09, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Create enhanced components
        self.user_info_section = self.create_user_info_section()
        self.add_widget(self.user_info_section)
        
        self.online_users_section = self.create_online_users_section()
        self.add_widget(self.online_users_section)
    
    def update_bg(self, *args):
        """Update background rectangle."""
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
    
    def create_user_info_section(self) -> MDCard:
        """Create enhanced user information section."""
        user_card = MDCard(
            size_hint_y=None,
            height=dp(140),
            padding=dp(24),
            orientation="vertical",
            radius=[dp(16)],
            elevation=4,
            md_bg_color=[0.1, 0.1, 0.15, 0.95],
            spacing=dp(12)
        )
        
        # User header with avatar and info
        user_header = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(16),
            size_hint_y=None,
            height=dp(50)
        )
        
        # Enhanced avatar
        self.user_avatar = MDCard(
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            radius=[dp(25)],
            md_bg_color=[0.2, 0.2, 0.25, 1.0]
        )
        
        self.avatar_label = MDLabel(
            text="?",
            halign="center",
            valign="middle",
            font_size=sp(24),
            bold=True,
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]
        )
        self.user_avatar.add_widget(self.avatar_label)
        
        # User details
        user_details = MDBoxLayout(
            orientation="vertical",
            spacing=dp(4)
        )
        
        self.username_label = MDLabel(
            text="Not Connected",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(18),
            bold=True
        )
        
        # Status with animated indicator
        status_container = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(20)
        )
        
        self.status_dot = MDCard(
            size_hint=(None, None),
            size=(dp(8), dp(8)),
            radius=[dp(4)],
            # theme_md_bg_color="Custom",
            # md_bg_color=[0.5, 0.5, 0.5, 1]
        )
        
        self.status_text = MDLabel(
            text="Offline",
            theme_text_color="Custom",
            text_color=[0.7, 0.7, 0.7, 1],
            font_size=sp(14)
        )
        
        status_container.add_widget(self.status_dot)
        status_container.add_widget(self.status_text)
        
        user_details.add_widget(self.username_label)
        user_details.add_widget(status_container)
        
        user_header.add_widget(self.user_avatar)
        user_header.add_widget(user_details)
        
        user_card.add_widget(user_header)
        
        # Elegant divider
        divider = MDDivider(
            color=[0.3, 0.3, 0.35, 0.5],
            size_hint_y=None,
            height=dp(1)
        )
        user_card.add_widget(divider)
        
        # Connection info
        self.connection_info = MDLabel(
            text="Ready to connect",
            theme_text_color="Custom",
            text_color=[0.5, 0.5, 0.6, 1],
            font_size=sp(12),
            halign="center"
        )
        user_card.add_widget(self.connection_info)
        
        return user_card
    
    def create_online_users_section(self) -> MDCard:
        """Create enhanced online users section."""
        users_card = MDCard(
            padding=dp(20),
            orientation="vertical",
            radius=[dp(16)],
            elevation=4,
            md_bg_color=[0.1, 0.1, 0.15, 0.95],
            spacing=dp(16)
        )
        
        # Header with modern design
        header_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(32),
            spacing=dp(12)
        )
        
        # Animated online indicator
        self.online_indicator = MDCard(
            size_hint=(None, None),
            size=(dp(12), dp(12)),
            radius=[dp(6)],
            md_bg_color=[0, 1, 0, 1]
        )
        
        # Start pulsing animation
        self.start_online_indicator_animation()
        
        users_title = MDLabel(
            text="Online Users",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(18),
            bold=True
        )
        
        # Count badge
        self.users_count_badge = MDCard(
            size_hint=(None, None),
            size=(dp(28), dp(20)),
            radius=[dp(10)],
            md_bg_color=[0.2, 0.6, 1.0, 1.0]
        )
        
        self.count_text = MDLabel(
            text="0",
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(12),
            bold=True
        )
        self.users_count_badge.add_widget(self.count_text)
        
        header_layout.add_widget(self.online_indicator)
        header_layout.add_widget(users_title)
        header_layout.add_widget(MDLabel())  # Spacer
        header_layout.add_widget(self.users_count_badge)
        
        users_card.add_widget(header_layout)
        
        # Elegant divider
        divider = MDDivider(
            color=[0.3, 0.3, 0.35, 0.5],
            size_hint_y=None,
            height=dp(1)
        )
        users_card.add_widget(divider)
        
        # Enhanced scrollable users list
        self.users_scroll = MDScrollView(
            do_scroll_x=False,
            scroll_type=['bars'],
            bar_width=dp(4),
            bar_color=[0.3, 0.3, 0.4, 0.6],
            bar_inactive_color=[0.2, 0.2, 0.25, 0.3]
        )
        
        self.users_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            adaptive_height=True,
            spacing=dp(8),
            padding=[dp(8), dp(8), dp(8), dp(8)]
        )
        
        # Add empty state placeholder
        self.add_empty_state_placeholder()
        
        self.users_scroll.add_widget(self.users_layout)
        users_card.add_widget(self.users_scroll)
        
        return users_card
    
    def start_online_indicator_animation(self):
        """Start pulsing animation for online indicator."""
        def pulse_indicator(dt):
            pulse = Animation(opacity=0.7, duration=1.0, t='in_out_sine')
            pulse += Animation(opacity=1.0, duration=1.0, t='in_out_sine')
            pulse.start(self.online_indicator)
            Clock.schedule_once(pulse_indicator, 2.0)
        
        Clock.schedule_once(pulse_indicator, 0.5)
    
    def add_empty_state_placeholder(self):
        """Add placeholder when no users are online."""
        self.empty_placeholder = MDBoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(80),
            padding=[dp(16), dp(16), dp(16), dp(16)]
        )
        
        empty_icon = MDLabel(
            text="👥",
            font_size=sp(32),
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        
        empty_text = MDLabel(
            text="No users online",
            theme_text_color="Custom",
            text_color=[0.5, 0.5, 0.6, 1],
            font_size=sp(14),
            halign="center",
            size_hint_y=None,
            height=dp(20)
        )
        
        empty_subtext = MDLabel(
            text="Users will appear here when they connect",
            theme_text_color="Custom",
            text_color=[0.4, 0.4, 0.5, 1],
            font_size=sp(11),
            halign="center",
            size_hint_y=None,
            height=dp(16)
        )
        
        self.empty_placeholder.add_widget(empty_icon)
        self.empty_placeholder.add_widget(empty_text)
        self.empty_placeholder.add_widget(empty_subtext)
        
        self.users_layout.add_widget(self.empty_placeholder)
    
    def remove_empty_state_placeholder(self):
        """Remove empty state placeholder with animation."""
        if hasattr(self, 'empty_placeholder') and self.empty_placeholder.parent:
            fade_out = Animation(opacity=0, duration=0.3)
            fade_out.bind(
                on_complete=lambda *x: self.users_layout.remove_widget(self.empty_placeholder)
            )
            fade_out.start(self.empty_placeholder)
    
    def update_user_info(self, username: str, status: str = "Online"):
        """Update current user information with animation."""
        self.current_username = username
        self.current_status = status
        
        # Update avatar
        self.avatar_label.text = username[0].upper() if username and username != "Not Connected" else "?"
        
        if username != "Not Connected":
            self.user_avatar.md_bg_color = [0.2, 0.6, 1.0, 1.0]
            # Bounce animation for avatar (now using opacity)
            bounce = Animation(opacity=0.5, duration=0.2)
            bounce += Animation(opacity=1.0, duration=0.2)
            bounce.start(self.user_avatar)
        else:
            self.user_avatar.md_bg_color = [0.2, 0.2, 0.25, 1.0]
        
        # Update labels
        self.username_label.text = username
        self.status_text.text = status
        
        # Update status dot with animation
        if status == "Online":
            self.status_dot.md_bg_color = [0, 1, 0, 1]
            self.status_text.text_color = [0, 1, 0, 1]
            self.connection_info.text = f"Connected since {time.strftime('%H:%M')}"
            
            # Pulse animation for status dot (now using opacity)
            pulse = Animation(opacity=0.5, duration=0.3)
            pulse += Animation(opacity=1.0, duration=0.3)
            pulse.start(self.status_dot)
        else:
            self.status_dot.md_bg_color = [0.5, 0.5, 0.5, 1]
            self.status_text.text_color = [0.7, 0.7, 0.7, 1]
            self.connection_info.text = "Ready to connect"
    
    def add_active_user(self, username: str):
        """Add user to active list with staggered animation."""
        if username not in self.active_users:
            self.active_users.append(username)
            self.update_users_display()
    
    def remove_active_user(self, username: str):
        """Remove user from active list with fade animation."""
        if username in self.active_users:
            self.active_users.remove(username)
            self.update_users_display()
    
    def update_users_display(self):
        """Update users display with enhanced animations."""
        # Remove empty placeholder if users exist
        if self.active_users and hasattr(self, 'empty_placeholder'):
            self.remove_empty_state_placeholder()
        
        # Clear existing users
        for child in self.users_layout.children[:]:
            if child != getattr(self, 'empty_placeholder', None):
                fade_out = Animation(opacity=0, x=child.x - dp(30), duration=0.2)
                fade_out.bind(
                    on_complete=lambda anim, widget=child: self.users_layout.remove_widget(widget)
                )
                fade_out.start(child)
        
        # Update count with bounce animation
        count = len(self.active_users)
        self.count_text.text = str(count)
        
        if count > 0:
            bounce = Animation(opacity=0.5, duration=0.2)
            bounce += Animation(opacity=1.0, duration=0.2)
            bounce.start(self.users_count_badge)
        
        # Add users with staggered entrance
        Clock.schedule_once(lambda dt: self._add_users_with_animation(), 0.3)
        
        # Add empty state if no users
        if not self.active_users:
            Clock.schedule_once(lambda dt: self.add_empty_state_placeholder(), 0.4)
    
    def _add_users_with_animation(self):
            
        for i, user in enumerate(self.active_users):
                user_item = self.create_enhanced_user_item(user)
                self.users_layout.add_widget(user_item)
                
                # Set the initial state before the animation
                user_item.opacity = 0
                
                # Start the fade-in animation
                entrance_anim = Animation(
                    opacity=1,
                    duration=0.4,
                    # delay=i * 0.1,  # Staggered delay for each user
                    t='out_cubic'
                )
                entrance_anim.start(user_item)
    
    def create_enhanced_user_item(self, username: str) -> MDBoxLayout:
        """Create modern user item with enhanced styling."""
        user_container = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(45),
            spacing=dp(12),
            padding=[dp(12), dp(6), dp(12), dp(6)]
        )
        
        # Hover effect background
        hover_bg = MDCard(
            md_bg_color=[0, 0, 0, 0],
            radius=[dp(8)],
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        user_container.add_widget(hover_bg)
        
        # User avatar with initial
        avatar = MDCard(
            size_hint=(None, None),
            size=(dp(32), dp(32)),
            radius=[dp(16)],
            md_bg_color=[0.3, 0.3, 0.4, 1.0]
        )
        
        avatar_text = MDLabel(
            text=username[0].upper(),
            halign="center",
            valign="middle",
            font_size=sp(6),
            bold=True,
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]
        )
        avatar.add_widget(avatar_text)
        
        # Username label
        user_label = MDLabel(
            text=username,
            theme_text_color="Custom",
            text_color=[0.9, 0.9, 0.9, 1],
            font_size=sp(15)
        )
        
        # Online status indicator
        status_layout = MDBoxLayout(
            size_hint_x=None,
            width=dp(20)
        )
        
        online_dot = MDCard(
            size_hint=(None, None),
            size=(dp(8), dp(8)),
            radius=[dp(4)],
            md_bg_color=[0, 1, 0, 1],
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        # Animate online dot
        pulse = Animation(opacity=0.5, duration=1.0, t='in_out_sine')
        pulse += Animation(opacity=1.0, duration=1.0, t='in_out_sine')
        pulse.repeat = True
        pulse.start(online_dot)
        
        status_layout.add_widget(online_dot)
        
        # Content layout
        content_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12)
        )
        content_layout.add_widget(avatar)
        content_layout.add_widget(user_label)
        content_layout.add_widget(MDLabel())  # Spacer
        content_layout.add_widget(status_layout)
        
        user_container.add_widget(content_layout)
        
        return user_container
    
    def clear_users_list(self):
        """Clear all users with fade animation."""
        self.active_users.clear()
        
        # Fade out all user items
        for child in self.users_layout.children[:]:
            if child != getattr(self, 'empty_placeholder', None):
                fade_out = Animation(opacity=0, duration=0.3)
                fade_out.bind(
                    on_complete=lambda anim, widget=child: self.users_layout.remove_widget(widget)
                )
                fade_out.start(child)
        
        # Update count
        self.count_text.text = "0"
        
        # Add empty placeholder after delay
        Clock.schedule_once(lambda dt: self.add_empty_state_placeholder(), 0.4)
    
    def get_active_users(self) -> List[str]:
        """Get list of active users."""
        return self.active_users.copy()
    
    def get_user_count(self) -> int:
        """Get number of active users."""
        return len(self.active_users)
    
    def set_user_offline(self):
        """Set current user as offline."""
        if self.current_username and self.current_username != "Not Connected":
            self.update_user_info(self.current_username, "Offline")
    
    def set_user_online(self, username: str):
        """Set current user as online."""
        self.update_user_info(username, "Online")
    
    def reset_sidebar(self):
        """Reset sidebar to initial state with animation."""
        # Fade out animation
        fade_out = Animation(opacity=0.5, duration=0.3)
        fade_out.bind(
            on_complete=lambda *x: self._complete_reset()
        )
        fade_out.start(self.user_info_section)
        
    def _complete_reset(self):
        """Complete the reset process."""
        self.update_user_info("Not Connected", "Offline")
        self.clear_users_list()
        self.current_username = None
        
        # Fade back in
        fade_in = Animation(opacity=1, duration=0.3)
        fade_in.start(self.user_info_section)
    
    def animate_user_activity(self, username: str):
        """Animate when a user sends a message."""
        # Find the user item and animate it
        for child in self.users_layout.children:
            if hasattr(child, 'username') and child.username == username:
                activity_anim = Animation(
                        opacity=0.8,
                        duration=0.2,
                        t='in_out_sine'
                    ) + Animation(
                        opacity=1,
                        duration=0.2,
                        t='in_out_sine'
                    )
                activity_anim.start(child)
                break
    
    def update_connection_time(self):
        """Update connection time display."""
        if self.current_status == "Online" and self.current_username:
            self.connection_info.text = f"Connected since {time.strftime('%H:%M')}"


class UserInfoCard(MDCard):
    """Enhanced user info card component."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_card()
    
    def setup_card(self):
        """Setup the enhanced user info card."""
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = dp(20)
        self.orientation = "vertical"
        self.radius = [dp(15)]
        self.elevation = 3
        self.md_bg_color = [0.1, 0.1, 0.12, 1.0]
        self.spacing = dp(8)
        
        # Add subtle border glow
        with self.canvas.after:
            Color(0.2, 0.6, 1.0, 0.2)
            self.border_line = Line(
                rounded_rectangle=[
                    self.x, self.y, self.width, self.height, dp(15)
                ],
                width=1
            )
        
        self.bind(pos=self.update_border, size=self.update_border)
    
    def update_border(self, *args):
        """Update border line position."""
        if hasattr(self, 'border_line'):
            self.border_line.rounded_rectangle = [
                self.x, self.y, self.width, self.height, dp(15)
            ]


class OnlineUsersCard(MDCard):
    """Enhanced online users card component."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_card()
    
    def setup_card(self):
        """Setup the enhanced online users card."""
        self.padding = dp(20)
        self.orientation = "vertical"
        self.radius = [dp(15)]
        self.elevation = 3
        self.md_bg_color = [0.1, 0.1, 0.12, 1.0]
        self.spacing = dp(12)
        
        # Add subtle border glow
        with self.canvas.after:
            Color(0.2, 0.6, 1.0, 0.2)
            self.border_line = Line(
                rounded_rectangle=[
                    self.x, self.y, self.width, self.height, dp(15)
                ],
                width=1
            )
        
        self.bind(pos=self.update_border, size=self.update_border)
    
    def update_border(self, *args):
        """Update border line position."""
        if hasattr(self, 'border_line'):
            self.border_line.rounded_rectangle = [
                self.x, self.y, self.width, self.height, dp(15)
            ]


# Replace the existing Sidebar class
# Sidebar = EnhancedSidebar