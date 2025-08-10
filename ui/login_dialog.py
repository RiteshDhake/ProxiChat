"""
Enhanced login dialog with modern design and animations.
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
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line
from typing import Callable, Optional
from kivy.uix.image import Image



class EnhancedLoginDialog(MDFloatLayout):
    """Modern login dialog with glassmorphism effect and animations."""
    
    def __init__(self, connect_callback: Callable[[str, str], None], **kwargs):
        super().__init__(**kwargs)
        self.connect_callback = connect_callback
        self.setup_dialog()
        self.animate_entrance()
        self.opacity =0
    
    def setup_dialog(self):
        """Setup enhanced login dialog with modern styling."""
        self.size_hint = (1, 1)
        
        # Animated background overlay
        with self.canvas.before:
            Color(0, 0, 0, 0)  # Start transparent
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # Main login card with glassmorphism effect
        self.login_card = self.create_enhanced_login_card()
        self.add_widget(self.login_card)
    
    def create_enhanced_login_card(self) -> MDCard:
        """Create modern login card with glassmorphism styling."""
        login_card = MDCard(
            size_hint=(None, None),
            size=(dp(420), dp(480)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            padding=dp(32),
            orientation="vertical",
            spacing=dp(24),
            radius=[dp(20),dp(20),dp(20),dp(20)],
            elevation=8,
            style = "outlined",
            theme_bg_color="Custom",
            md_bg_color=[0.1, 0.1, 0.15, 0.95]  # Semi-transparent dark
        )
        
        # Add subtle border effect
        # with login_card.canvas.after:
        #     Color(0.3, 0.3, 0.4, 0.3)
        #     login_card.border_line = Line(
        #         rounded_rectangle=[
        #             login_card.x, login_card.y, 
        #             login_card.width, login_card.height, 
        #             dp(20)
        #         ],
        #         width=1
        #     )
        
        login_card.bind(pos=self.update_card_border, size=self.update_card_border)
        
        # Animated title section
        title_section = self.create_title_section()
        login_card.add_widget(title_section)
        
        # Input fields section
        inputs_section = self.create_inputs_section()
        login_card.add_widget(inputs_section)
        
        # Connect button section
        button_section = self.create_button_section()
        login_card.add_widget(button_section)
        
        return login_card
    
    def create_title_section(self) -> MDBoxLayout:
        """Create animated title section."""
        title_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(100),
            spacing=dp(8)
        )
        
        # App logo/icon
        logo_label = Image(
            source="/Users/riteshdhake/Documents/Chatting_app/chatting_code/logo.png",
                size_hint=(None, None),
                size=(dp(45), dp(45)),
                allow_stretch=True,
                keep_ratio=True,
                pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        # Main title
        title_label = MDLabel(
            text="Join Chat Server",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size=sp(24),
            bold=True,
            halign="center",
            size_hint_y=None,
            height=dp(32)
        )
        
        # Subtitle
        subtitle_label = MDLabel(
            text="Connect with friends and colleagues",
            theme_text_color="Custom",
            text_color=[0.7, 0.7, 0.7, 1],
            font_size=sp(14),
            halign="center",
            size_hint_y=None,
            height=dp(20)
        )
        
        title_layout.add_widget(logo_label)
        title_layout.add_widget(title_label)
        title_layout.add_widget(subtitle_label)
        
        return title_layout
    
    def create_inputs_section(self) -> MDBoxLayout:
        """Create enhanced input fields section."""
        inputs_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            size_hint_y=None,
            height=dp(160)
        )
        
        # Username input with enhanced styling
        self.username_input = MDTextField(
            MDTextFieldLeadingIcon(
                icon="account-circle",
                theme_icon_color="Custom",
                icon_color=[0.2, 0.6, 1.0, 1],
                icon_color_focus=[0.3, 0.7, 1.0, 1],
            ),
            MDTextFieldHintText(
                text="Enter your username",
                text_color_normal=[0.6, 0.6, 0.6, 1],
                text_color_focus=[0.8, 0.8, 0.8, 1],
            ),
            MDTextFieldMaxLengthText(
                max_text_length=128,
            ),
            mode="outlined",
            line_color_normal=[0.3, 0.3, 0.4, 1],
            line_color_focus=[0.2, 0.6, 1.0, 1],
            text_color_normal=[1, 1, 1, 1],
            text_color_focus=[1, 1, 1, 1],
            fill_color_normal=[0.08, 0.08, 0.1, 1],
            fill_color_focus=[0.1, 0.1, 0.12, 1]
        )
        
        # IP address input with enhanced styling
        self.ip_input = MDTextField(
            MDTextFieldLeadingIcon(
                icon="server-network",
                theme_icon_color="Custom",
                icon_color=[0.2, 0.6, 1.0, 1],
                icon_color_focus=[0.3, 0.7, 1.0, 1],
            ),
            MDTextFieldHintText(
                text="Server IP address (e.g., 192.168.1.100)",
                text_color_normal=[0.6, 0.6, 0.6, 1],
                text_color_focus=[0.8, 0.8, 0.8, 1],
            ),
            MDTextFieldMaxLengthText(
                max_text_length=15,
            ),
            mode="outlined",
            line_color_normal=[0.3, 0.3, 0.4, 1],
            line_color_focus=[0.2, 0.6, 1.0, 1],
            text_color_normal=[1, 1, 1, 1],
            text_color_focus=[1, 1, 1, 1],
            fill_color_normal=[0.08, 0.08, 0.1, 1],
            fill_color_focus=[0.1, 0.1, 0.12, 1]
        )
        
        inputs_layout.add_widget(self.username_input)
        inputs_layout.add_widget(self.ip_input)
        
        return inputs_layout
    
    def create_button_section(self) -> MDBoxLayout:
        """Create enhanced button section."""
        button_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(16),
            size_hint_y=None,
            height=dp(80)
        )
        
        # Enhanced connect button
        self.connect_button = MDButton(
            MDButtonIcon(
                icon="wifi",
                theme_icon_color="Custom",
                icon_color=[1, 1, 1, 1]
            ),
            MDButtonText(
                text="Connect to Server",
                theme_text_color="Custom",
                text_color=[1, 1, 1, 1],
                font_size=sp(16),
                bold=True
            ),
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=[0.2, 0.6, 1.0, 1],
            size_hint_y=None,
            height=dp(50),
            on_release=self.on_connect_pressed
        )
        
        # Loading indicator (hidden initially)
        self.loading_label = MDLabel(
            text="Connecting...",
            halign="center",
            theme_text_color="Custom",
            text_color=[0.2, 0.6, 1.0, 1],
            font_size=sp(14),
            size_hint_y=None,
            height=dp(0),
            opacity=0
        )
        
        button_layout.add_widget(self.connect_button)
        button_layout.add_widget(self.loading_label)
        
        return button_layout
    
    def animate_entrance(self):
        """FIXED: Animate dialog entrance with modern effects."""
        # Fix: Don't animate canvas directly
        self.opacity = 0  # Start transparent
        
        # Simple fade-in animation for the entire dialog
        dialog_anim = Animation(opacity=1, duration=0.3)
        dialog_anim.start(self)
        
        # Card entrance animation - safe approach
        if hasattr(self, 'login_card'):
            original_y = self.login_card.y
            self.login_card.y -= dp(50)
            self.login_card.opacity = 0
            
            card_anim = Animation(
                y=original_y,
                opacity=1,
                duration=0.4,
                t='out_back'
            )
            card_anim.start(self.login_card)

    
    def update_bg(self, *args):
        """Update background rectangle."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def update_card_border(self, *args):
        """Update card border line."""
        if hasattr(self.login_card, 'border_line'):
            self.login_card.border_line.rounded_rectangle = [
                self.login_card.x, self.login_card.y,
                self.login_card.width, self.login_card.height,
                dp(20)
            ]
    
    def on_connect_pressed(self, instance):
        """Handle connect button with enhanced feedback."""
        username = self.get_username()
        host = self.get_host()
        
        if self.validate_inputs(username, host):
            self.show_connecting_state()
            
            # Delay to show loading state
            Clock.schedule_once(
                lambda dt: self.connect_callback(username, host), 
                0.5
            )
    
    def show_connecting_state(self):
        """Show connecting animation and state."""
        # Disable button and show loading
        self.connect_button.disabled = True
        self.connect_button.md_bg_color = [0.3, 0.3, 0.35, 1]
        
        # Show loading indicator
        self.loading_label.height = dp(30)
        load_anim = Animation(opacity=1, duration=0.3)
        load_anim.start(self.loading_label)
        
        # Rotate loading emoji
        self.animate_loading()
    
    def animate_loading(self):
        """Animate loading indicator."""
        def rotate_loading(dt):
            if self.loading_label.opacity > 0:
                # Simple text rotation effect
                loading_chars = ["🔄", "⏳", "🔄", "⏳"]
                current_text = self.loading_label.text
                if "🔄" in current_text:
                    self.loading_label.text = "⏳ Connecting..."
                else:
                    self.loading_label.text = "🔄 Connecting..."
                
                Clock.schedule_once(rotate_loading, 0.5)
        
        Clock.schedule_once(rotate_loading, 0.5)
    
    def hide_connecting_state(self):
        """Hide connecting state and restore button."""
        self.connect_button.disabled = False
        self.connect_button.md_bg_color = [0.2, 0.6, 1.0, 1]
        
        # Hide loading indicator
        hide_anim = Animation(opacity=0, height=dp(0), duration=0.3)
        hide_anim.start(self.loading_label)
    
    def get_username(self) -> str:
        """Get entered username."""
        return self.username_input.text.strip()
    
    def get_host(self) -> str:
        """Get entered host IP."""
        return self.ip_input.text.strip()
    
    def validate_inputs(self, username: str, host: str) -> bool:
        """Enhanced input validation with visual feedback."""
        is_valid = True
        
        if not username:
            self.show_field_error(self.username_input, "Username is required")
            is_valid = False
        elif len(username) < 2:
            self.show_field_error(self.username_input, "Username must be at least 2 characters")
            is_valid = False
        
        if not host:
            self.show_field_error(self.ip_input, "Server IP address is required")
            is_valid = False
        elif not self.is_valid_ip_format(host):
            self.show_field_error(self.ip_input, "Please enter a valid IP address")
            is_valid = False
        
        return is_valid
    
    def show_field_error(self, field: MDTextField, error_msg: str):
        """Show field validation error with animation."""
        # Red border animation
        field.line_color_normal = [1, 0.3, 0.3, 1]
        field.line_color_focus = [1, 0.3, 0.3, 1]
        
        # Shake animation
        original_x = field.x
        shake_anim = Animation(x=original_x + dp(10), duration=0.1)
        shake_anim += Animation(x=original_x - dp(10), duration=0.1)
        shake_anim += Animation(x=original_x + dp(5), duration=0.1)
        shake_anim += Animation(x=original_x, duration=0.1)
        shake_anim.start(field)
        
        # Reset border color after delay
        Clock.schedule_once(
            lambda dt: self.reset_field_colors(field), 
            2.0
        )
    
    def reset_field_colors(self, field: MDTextField):
        """Reset field colors to normal."""
        field.line_color_normal = [0.3, 0.3, 0.4, 1]
        field.line_color_focus = [0.2, 0.6, 1.0, 1]
    
    def is_valid_ip_format(self, ip: str) -> bool:
        """Enhanced IP validation."""
        if ip == "localhost":
            return True
        
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
    
    def clear_inputs(self):
        """Clear inputs with animation."""
        fade_out = Animation(opacity=0.5, duration=0.2)
        fade_in = Animation(opacity=1, duration=0.2)
        
        fade_out.bind(on_complete=lambda *x: setattr(self.username_input, 'text', ''))
        fade_out += fade_in
        fade_out.start(self.username_input)
        
        fade_out.bind(on_complete=lambda *x: setattr(self.ip_input, 'text', ''))
        fade_out.start(self.ip_input)
    
    def set_default_values(self, username: str = "", host: str = "192.168.0.125"):
        """Set default values with smooth typing animation."""
        if username:
            self.username_input.text = username
        if host:
            self.ip_input.text = host
    
    def focus_username_input(self):
        """Focus username input with highlight."""
        self.username_input.focus = True
        
        # Subtle glow effect
        glow_anim = Animation(
            line_color_focus=[0.3, 0.8, 1.0, 1],
            duration=0.3
        )
        glow_anim.start(self.username_input)
    
    def animate_entrance(self):
        self.opacity = 0
    
    # Animate to semi-transparent background effect
        anim1 = Animation(opacity=0.9, duration=0.3)
        Clock.schedule_once(lambda dt: anim1.start(self), 0.1)


class LoginDialogManager:
    """Enhanced login dialog manager with improved animations."""
    
    def __init__(self, parent_screen, connect_callback: Callable[[str, str], None]):
        self.parent_screen = parent_screen
        self.connect_callback = connect_callback
        self.dialog: Optional[EnhancedLoginDialog] = None
    
    def show_login(self, default_username: str = "", default_host: str = "192.168.0.125"):
        """Show enhanced login dialog."""
        # FIXED: Proper parent management to prevent widget parent error
        if self.dialog is not None:
            # If dialog exists and has a parent, remove it first
            if self.dialog.parent:
                self.dialog.parent.remove_widget(self.dialog)
            # Clear the reference to create a fresh dialog
            self.dialog = None
        
        # Create new dialog instance
        self.dialog = EnhancedLoginDialog(self.on_connect_requested)
        self.dialog.set_default_values(default_username, default_host)
        
        # Add to parent screen
        self.parent_screen.add_widget(self.dialog)
        
        # Focus username input after a short delay
        Clock.schedule_once(lambda dt: self.dialog.focus_username_input(), 0.5)

    # Also update the hide_login method to properly clear the dialog reference:

    def hide_login(self):
        """Hide login dialog with exit animation."""
        if self.dialog and self.dialog.parent:
            # Get reference to the Color instruction for background fade
            bg_color = self.dialog.canvas.before.children[0]
            
            # Background fade out animation
            bg_anim = Animation(a=0, duration=0.3)
            
            # Card exit animation - using opacity and position instead of scale
            exit_anim = Animation(
                opacity=0,
                y=self.dialog.login_card.y - dp(30),  # Slide down slightly
                duration=0.3,
                t='in_cubic'
            )
            
            def remove_dialog(*args):
                if self.dialog and self.dialog.parent:
                    self.parent_screen.remove_widget(self.dialog)
                    # Clear dialog reference after removal
                    self.dialog = None
            
            # Bind completion callback and start animations
            exit_anim.bind(on_complete=remove_dialog)
            exit_anim.start(self.dialog.login_card)
            bg_anim.start(bg_color)

    def on_connect_requested(self, username: str, host: str):
        """Handle connection request with enhanced feedback."""
        success = self.connect_callback(username, host)
        if success:
            # Success animation before hiding
            success_anim = Animation(
                md_bg_color=[0.2, 0.8, 0.2, 1],
                duration=0.3
            )
            success_anim.bind(
                on_complete=lambda *x: Clock.schedule_once(
                    lambda dt: self.hide_login(), 0.5
                )
            )
            success_anim.start(self.dialog.connect_button)
        else:
            # Reset connecting state on failure
            self.dialog.hide_connecting_state()
            # Error shake animation - ensure we have valid position
            if hasattr(self.dialog.login_card, 'pos') and self.dialog.login_card.pos:
                original_pos = self.dialog.login_card.pos
                shake = Animation(x=original_pos[0] + dp(15), duration=0.1)
                shake += Animation(x=original_pos[0] - dp(15), duration=0.1)
                shake += Animation(x=original_pos[0], duration=0.1)
                shake.start(self.dialog.login_card)
        
        def cleanup(self):
            """Enhanced cleanup with animations."""
            if self.dialog:
                self.hide_login()
                Clock.schedule_once(lambda dt: setattr(self, 'dialog', None), 0.5)


# Additional utility classes for enhanced styling

class GradientCard(MDCard):
    """Card with gradient background effect."""
    
    def __init__(self, gradient_colors: list = None, **kwargs):
        super().__init__(**kwargs)
        self.gradient_colors = gradient_colors or [
            [0.1, 0.1, 0.15, 1],
            [0.05, 0.05, 0.08, 1]
        ]
        self.setup_gradient()
    
    def setup_gradient(self):
        """Setup gradient background."""
        with self.canvas.before:
            # Simple gradient simulation with overlapping colors
            Color(*self.gradient_colors[0])
            self.bg_rect1 = RoundedRectangle(
                pos=self.pos, 
                size=self.size, 
                radius=self.radius
            )
            Color(*self.gradient_colors[1])
            self.bg_rect2 = RoundedRectangle(
                pos=(self.x, self.y + self.height * 0.5), 
                size=(self.width, self.height * 0.5),
                radius=[0, 0] + self.radius[2:]
            )
        
        self.bind(pos=self.update_gradient, size=self.update_gradient)
    
    def update_gradient(self, *args):
        """Update gradient rectangles."""
        self.bg_rect1.pos = self.pos
        self.bg_rect1.size = self.size
        self.bg_rect2.pos = (self.x, self.y + self.height * 0.5)
        self.bg_rect2.size = (self.width, self.height * 0.5)


class AnimatedLabel(MDLabel):
    """Label with typewriter animation effect."""
    
    def __init__(self, target_text: str, **kwargs):
        self.target_text = target_text
        self.current_text = ""
        super().__init__(text="", **kwargs)
        self.start_typewriter()
    
    def start_typewriter(self):
        """Start typewriter animation."""
        def add_character(dt):
            if len(self.current_text) < len(self.target_text):
                self.current_text += self.target_text[len(self.current_text)]
                self.text = self.current_text + "|"  # Cursor effect
                Clock.schedule_once(add_character, 0.05)
            else:
                self.text = self.current_text  # Remove cursor
        
        Clock.schedule_once(add_character, 0.1)
class PulsingIcon(MDLabel):
    """Icon with pulsing animation effect."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation = None
        self.start_pulsing()
    
    def start_pulsing(self):
        """Start pulsing animation."""
        pulse_anim = Animation(opacity=0.5, duration=1.0, t='in_out_sine')
        pulse_anim += Animation(opacity=1.0, duration=1.0, t='in_out_sine')
        pulse_anim.repeat = True
        
        # Store reference to animation for potential cleanup
        self.animation = pulse_anim
        pulse_anim.start(self)
    
    def stop_pulsing(self):
        """Stop pulsing animation."""
        if self.animation:
            self.animation.cancel(self)
            self.opacity = 1.0  # Reset to full opacity