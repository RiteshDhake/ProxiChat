"""
Enhanced constants and configuration values for modern UI components.
This file replaces your existing constants.py
"""

from kivy.metrics import dp, sp

# ============================================================================
# WINDOW AND LAYOUT CONFIGURATION
# ============================================================================

# Window Configuration
WINDOW_SIZE = (1200, 800)  # Increased for better modern layout
MIN_WINDOW_SIZE = (900, 650)
MAX_WINDOW_SIZE = (1920, 1080)

# Layout Ratios
SIDEBAR_WIDTH_RATIO = 0.32
CHAT_AREA_WIDTH_RATIO = 0.68
MESSAGE_CARD_WIDTH_RATIO = 0.75

# ============================================================================
# MODERN SPACING AND SIZING
# ============================================================================

# Spacing Values
TINY_SPACING = dp(4)
SMALL_SPACING = dp(8)
DEFAULT_SPACING = dp(12)
MEDIUM_SPACING = dp(16)
LARGE_SPACING = dp(24)
EXTRA_LARGE_SPACING = dp(32)

# Padding Values
TINY_PADDING = dp(4)
SMALL_PADDING = dp(8)
DEFAULT_PADDING = dp(16)
MEDIUM_PADDING = dp(20)
LARGE_PADDING = dp(24)
EXTRA_LARGE_PADDING = dp(32)

# Component Heights
APP_BAR_HEIGHT = dp(75)
CHAT_HEADER_HEIGHT = dp(70)
MESSAGE_INPUT_HEIGHT = dp(90)
USER_INFO_CARD_HEIGHT = dp(140)
USER_LIST_ITEM_HEIGHT = dp(45)
SYSTEM_MESSAGE_HEIGHT = dp(45)
EMPTY_STATE_HEIGHT = dp(200)

# Component Widths
SIDEBAR_MIN_WIDTH = dp(280)
SIDEBAR_MAX_WIDTH = dp(400)
MESSAGE_CARD_MAX_WIDTH = dp(600)
LOGIN_DIALOG_WIDTH = dp(420)
LOGIN_DIALOG_HEIGHT = dp(480)

# Border Radius Values
SMALL_RADIUS = dp(8)
DEFAULT_RADIUS = dp(12)
MEDIUM_RADIUS = dp(16)
LARGE_RADIUS = dp(20)
EXTRA_LARGE_RADIUS = dp(25)

# ============================================================================
# MODERN COLOR SCHEME
# ============================================================================

class ModernColors:
    """Modern dark theme color palette."""
    
    # Background Colors
    MAIN_BACKGROUND = [0.03, 0.03, 0.05, 1.0]
    SIDEBAR_BACKGROUND = [0.06, 0.06, 0.09, 1.0]
    CHAT_BACKGROUND = [0.05, 0.05, 0.08, 1.0]
    CARD_BACKGROUND = [0.1, 0.1, 0.15, 0.95]
    INPUT_BACKGROUND = [0.12, 0.12, 0.16, 1.0]
    APP_BAR_BACKGROUND = [0.08, 0.08, 0.12, 1.0]
    
    # Message Colors
    OWN_MESSAGE_BG = [0.2, 0.6, 1.0, 1.0]
    OTHER_MESSAGE_BG = [0.15, 0.15, 0.17, 1.0]
    SYSTEM_MESSAGE_BG = [0.2, 0.6, 1.0, 0.9]
    
    # Accent Colors
    PRIMARY = [0.2, 0.6, 1.0, 1.0]
    PRIMARY_LIGHT = [0.3, 0.7, 1.0, 1.0]
    PRIMARY_DARK = [0.1, 0.5, 0.9, 1.0]
    
    # Status Colors
    SUCCESS = [0.2, 0.8, 0.2, 1.0]
    ERROR = [1.0, 0.3, 0.3, 1.0]
    WARNING = [1.0, 0.7, 0.2, 1.0]
    INFO = [0.2, 0.6, 1.0, 1.0]
    
    # Text Colors
    TEXT_PRIMARY = [1.0, 1.0, 1.0, 1.0]
    TEXT_SECONDARY = [0.9, 0.9, 0.9, 1.0]
    TEXT_TERTIARY = [0.7, 0.7, 0.7, 1.0]
    TEXT_QUATERNARY = [0.6, 0.6, 0.7, 1.0]
    TEXT_DISABLED = [0.4, 0.4, 0.4, 1.0]
    TEXT_HINT = [0.5, 0.5, 0.6, 1.0]
    
    # Border and Line Colors
    BORDER_NORMAL = [0.3, 0.3, 0.4, 1.0]
    BORDER_FOCUS = [0.2, 0.6, 1.0, 1.0]
    BORDER_ERROR = [1.0, 0.3, 0.3, 1.0]
    BORDER_SUCCESS = [0.2, 0.8, 0.2, 1.0]
    BORDER_WARNING = [1.0, 0.7, 0.2, 1.0]
    
    # Online Status Colors
    ONLINE_GREEN = [0, 1, 0, 1]
    OFFLINE_GRAY = [0.5, 0.5, 0.5, 1]
    AWAY_YELLOW = [1, 1, 0, 1]
    BUSY_RED = [1, 0.3, 0.3, 1]
    
    # Transparency Levels
    OVERLAY_DARK = [0, 0, 0, 0.8]
    OVERLAY_LIGHT = [0, 0, 0, 0.5]
    GLASSMORPHISM = [0.1, 0.1, 0.15, 0.95]


# ============================================================================
# TYPOGRAPHY CONFIGURATION
# ============================================================================

class Typography:
    """Modern typography scale."""
    
    # Font Sizes
    DISPLAY_LARGE = sp(32)
    DISPLAY_MEDIUM = sp(28)
    DISPLAY_SMALL = sp(24)
    
    HEADLINE_LARGE = sp(22)
    HEADLINE_MEDIUM = sp(20)
    HEADLINE_SMALL = sp(18)
    
    TITLE_LARGE = sp(18)
    TITLE_MEDIUM = sp(16)
    TITLE_SMALL = sp(14)
    
    BODY_LARGE = sp(16)
    BODY_MEDIUM = sp(14)
    BODY_SMALL = sp(12)
    
    LABEL_LARGE = sp(14)
    LABEL_MEDIUM = sp(12)
    LABEL_SMALL = sp(10)
    
    # Line Heights
    LINE_HEIGHT_TIGHT = 1.1
    LINE_HEIGHT_NORMAL = 1.2
    LINE_HEIGHT_LOOSE = 1.4


# ============================================================================
# ANIMATION CONFIGURATION
# ============================================================================

class Animations:
    """Animation timing and easing configurations."""
    
    # Duration Constants
    INSTANT = 0.0
    FAST = 0.15
    NORMAL = 0.3
    SLOW = 0.5
    VERY_SLOW = 0.8
    
    # Easing Functions
    EASE_IN = 'in_cubic'
    EASE_OUT = 'out_cubic'
    EASE_IN_OUT = 'in_out_cubic'
    EASE_BACK = 'out_back'
    EASE_ELASTIC = 'out_elastic'
    EASE_BOUNCE = 'out_bounce'
    
    # Common Animation Patterns
    ENTRANCE_DURATION = 0.4
    EXIT_DURATION = 0.3
    HOVER_DURATION = 0.2
    PRESS_DURATION = 0.1
    
    # Stagger Delays
    STAGGER_SHORT = 0.05
    STAGGER_MEDIUM = 0.1
    STAGGER_LONG = 0.15


# ============================================================================
# COMPONENT SPECIFIC CONFIGURATIONS
# ============================================================================

# Input Field Configurations
class InputConfig:
    MAX_USERNAME_LENGTH = 64
    MAX_MESSAGE_LENGTH = 1000
    MAX_IP_LENGTH = 15
    MIN_USERNAME_LENGTH = 2
    
    # Validation Patterns
    USERNAME_PATTERN = r'^[a-zA-Z0-9_-]+'
    IP_PATTERN = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'


# Avatar Configuration
class AvatarConfig:
    SMALL_SIZE = dp(24)
    MEDIUM_SIZE = dp(32)
    LARGE_SIZE = dp(50)
    EXTRA_LARGE_SIZE = dp(64)
    
    # Avatar Colors (for different users)
    AVATAR_COLORS = [
        [0.2, 0.6, 1.0, 1.0],    # Blue
        [0.8, 0.2, 0.8, 1.0],    # Purple
        [0.2, 0.8, 0.2, 1.0],    # Green
        [1.0, 0.6, 0.2, 1.0],    # Orange
        [0.8, 0.2, 0.2, 1.0],    # Red
        [0.2, 0.8, 0.8, 1.0],    # Cyan
        [0.8, 0.8, 0.2, 1.0],    # Yellow
        [0.6, 0.2, 0.8, 1.0],    # Violet
    ]


# ============================================================================
# THEME CONFIGURATION
# ============================================================================

# Material Design Theme
THEME_STYLE = "Dark"
PRIMARY_PALETTE = "Blue"
ACCENT_PALETTE = "LightBlue"

# Custom Theme Colors
THEME_COLORS = {
    "primary": ModernColors.PRIMARY,
    "secondary": [0.3, 0.3, 0.4, 1.0],
    "success": ModernColors.SUCCESS,
    "error": ModernColors.ERROR,
    "warning": ModernColors.WARNING,
    "info": ModernColors.INFO,
}

# ============================================================================
# NETWORK CONFIGURATION
# ============================================================================

# Network Settings
DEFAULT_PORT = 1234
DEFAULT_HOST = "192.168.0.125"
LOCALHOST = "127.0.0.1"
MESSAGE_ENCODING = 'utf-8'

# Connection Timeouts
CONNECTION_TIMEOUT = 10.0
RECONNECTION_DELAY = 3.0
HEARTBEAT_INTERVAL = 30.0

# ============================================================================
# FILE TRANSFER CONFIGURATION
# ============================================================================

# File Transfer Constants
FILE_TRANSFER_SIGNAL = "sending_file"
FILE_END_MARKER = b"<END>"
RECV_FILE_NAME = "Recv_file.txt"
BUFFER_SIZE = 4096
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Supported File Types
SUPPORTED_FILE_TYPES = [
    '.txt', '.pdf', '.doc', '.docx', '.jpg', '.jpeg', 
    '.png', '.gif', '.mp3', '.mp4', '.zip', '.rar'
]

# ============================================================================
# UI TEXT CONSTANTS
# ============================================================================

# Application Titles
APP_TITLE = "Chattr"
APP_SUBTITLE = "Modern Desktop Chat"
WINDOW_TITLE = "Chattr - Desktop Chat Application"

# Dialog Titles
LOGIN_DIALOG_TITLE = "Join Chat Server"
FILE_DIALOG_TITLE = "Select File to Send"
SETTINGS_DIALOG_TITLE = "Chat Settings"

# Section Titles
CHAT_HEADER_TITLE = "General Chat"
ONLINE_USERS_TITLE = "Online Users"
USER_INFO_TITLE = "Your Profile"

# ============================================================================
# PLACEHOLDER AND HINT TEXTS
# ============================================================================

# Input Placeholders
USERNAME_HINT = "Enter your username"
IP_HINT = "Server IP address (e.g., 192.168.1.100)"
MESSAGE_HINT = "Type your message here..."
SEARCH_HINT = "Search messages..."

# Welcome Messages
WELCOME_TITLE = "Welcome to Chattr!"
WELCOME_SUBTITLE = "Connect to start chatting with others"
WELCOME_DESCRIPTION = "Share your thoughts, files, and connect with friends in real-time"

# Empty State Messages
NO_USERS_TITLE = "No users online"
NO_USERS_SUBTITLE = "Users will appear here when they connect"
NO_MESSAGES_TITLE = "No messages yet"
NO_MESSAGES_SUBTITLE = "Start the conversation!"

# ============================================================================
# BUTTON AND ACTION TEXTS
# ============================================================================

# Button Labels
CONNECT_BUTTON_TEXT = "Connect to Server"
DISCONNECT_BUTTON_TEXT = "Disconnect"
SEND_BUTTON_TEXT = "Send"
FILE_BUTTON_TEXT = "File"
CANCEL_BUTTON_TEXT = "Cancel"
RETRY_BUTTON_TEXT = "Retry"
CLEAR_BUTTON_TEXT = "Clear Chat"

# Action Labels
CONNECTING_TEXT = "Connecting..."
SENDING_TEXT = "Sending..."
LOADING_TEXT = "Loading..."
RECONNECTING_TEXT = "Reconnecting..."

# ============================================================================
# STATUS AND STATE MESSAGES
# ============================================================================

# Connection Status
STATUS_ONLINE = "Online"
STATUS_OFFLINE = "Offline"
STATUS_CONNECTING = "Connecting"
STATUS_DISCONNECTED = "Disconnected"
STATUS_NOT_CONNECTED = "Not Connected"
STATUS_RECONNECTING = "Reconnecting"

# System Messages
class SystemMessages:
    # Connection Messages
    CONNECTED = "🎉 Connected to server successfully!"
    DISCONNECTED = "🔌 Disconnected from server"
    CONNECTION_FAILED = "❌ Failed to connect to server"
    CONNECTION_LOST = "⚠️ Connection lost - attempting to reconnect..."
    RECONNECTED = "✅ Reconnected to server"
    
    # User Activity Messages
    USER_JOINED = "👋 {username} joined the chat"
    USER_LEFT = "👋 {username} left the chat"
    USER_TYPING = "{username} is typing..."
    
    # File Transfer Messages
    FILE_RECEIVED = "📥 File received: {filename}"
    FILE_SENT = "📤 File sent: {filename}"
    FILE_SENDING = "⬆️ Sending file: {filename}"
    FILE_RECEIVE_FAILED = "❌ Failed to receive file: {filename}"
    FILE_SEND_FAILED = "❌ Failed to send file: {filename}"
    
    # General Messages
    CHAT_CLEARED = "🧹 Chat history cleared"
    SERVER_MAINTENANCE = "🔧 Server is under maintenance"
    RATE_LIMITED = "⏳ Slow down! You're sending messages too quickly"

# ============================================================================
# ERROR MESSAGES
# ============================================================================

class ErrorMessages:
    # Input Validation Errors
    NO_USERNAME = "Please enter a username"
    USERNAME_TOO_SHORT = "Username must be at least 2 characters"
    USERNAME_INVALID = "Username can only contain letters, numbers, _ and -"
    NO_HOST = "Please enter a server IP address"
    INVALID_IP = "Please enter a valid IP address"
    
    # Connection Errors
    CONNECTION_REFUSED = "Connection refused - server may be offline"
    CONNECTION_TIMEOUT = "Connection timed out - check your network"
    NETWORK_ERROR = "Network error - check your internet connection"
    SERVER_ERROR = "Server error - please try again later"
    
    # Message Errors
    MESSAGE_TOO_LONG = "Message is too long (max {max_length} characters)"
    MESSAGE_EMPTY = "Cannot send empty message"
    NOT_CONNECTED = "Not connected to server"
    SEND_FAILED = "Failed to send message - please try again"
    
    # File Transfer Errors
    FILE_TOO_LARGE = "File is too large (max {max_size}MB)"
    FILE_TYPE_UNSUPPORTED = "File type not supported"
    FILE_NOT_FOUND = "File not found"
    FILE_PERMISSION_ERROR = "Permission denied accessing file"

# ============================================================================
# ICON CONFIGURATION
# ============================================================================

# Material Design Icons
class Icons:
    # User and Profile
    ACCOUNT = "account-circle"
    AVATAR = "account"
    PROFILE = "account-box"
    
    # Connection and Network
    CONNECT = "wifi"
    DISCONNECT = "wifi-off"
    SERVER = "server-network"
    NETWORK = "network"
    
    # Communication
    SEND = "send"
    MESSAGE = "message-text"
    CHAT = "chat"
    
    # Files and Media
    FILE = "file-document"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "volume-high"
    ATTACHMENT = "paperclip"
    
    # Status Indicators
    ONLINE = "circle"
    OFFLINE = "circle-outline"
    AWAY = "clock"
    BUSY = "minus-circle"
    
    # Actions
    CLEAR = "delete-sweep"
    SETTINGS = "cog"
    REFRESH = "refresh"
    SEARCH = "magnify"
    
    # Navigation
    MENU = "menu"
    CLOSE = "close"
    BACK = "arrow-left"
    
    # Feedback
    SUCCESS = "check-circle"
    ERROR = "alert-circle"
    WARNING = "alert"
    INFO = "information"

# ============================================================================
# EMOJI SETS
# ============================================================================

class Emojis:
    """Modern emoji sets for enhanced visual communication."""
    
    # Status Emojis
    ONLINE = "🟢"
    OFFLINE = "⚫"
    AWAY = "🟡"
    BUSY = "🔴"
    
    # Activity Emojis
    CONNECTED = "🎉"
    DISCONNECTED = "🔌"
    JOINED = "👋"
    LEFT = "👋"
    TYPING = "✏️"
    
    # File Transfer Emojis
    FILE_RECEIVED = "📥"
    FILE_SENT = "📤"
    FILE_SENDING = "⬆️"
    FILE_ERROR = "❌"
    
    # System Emojis
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    LOADING = "🔄"
    
    # App Emojis
    LOGO = "💬"
    ROCKET = "🚀"
    SPARKLES = "✨"

# ============================================================================
# LAYOUT BREAKPOINTS
# ============================================================================

class Breakpoints:
    """Responsive design breakpoints."""
    
    MOBILE = 480
    TABLET = 768
    DESKTOP = 1024
    LARGE_DESKTOP = 1440
    
    # Sidebar behavior at different sizes
    HIDE_SIDEBAR_BELOW = 600
    COLLAPSE_SIDEBAR_BELOW = 800

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================

class Performance:
    """Performance and optimization settings."""
    
    # Message Management
    MAX_MESSAGES_DISPLAY = 100
    MESSAGE_CLEANUP_THRESHOLD = 150
    
    # Animation Performance
    REDUCE_ANIMATIONS_BELOW_FPS = 30
    ANIMATION_FRAME_RATE = 60
    
    # Memory Management
    AVATAR_CACHE_SIZE = 50
    IMAGE_CACHE_SIZE = 20

# ============================================================================
# ACCESSIBILITY CONFIGURATION
# ============================================================================

class Accessibility:
    """Accessibility and usability settings."""
    
    # Minimum Touch Targets
    MIN_TOUCH_SIZE = dp(44)
    
    # Contrast Ratios (for WCAG compliance)
    MIN_CONTRAST_NORMAL = 4.5
    MIN_CONTRAST_LARGE = 3.0
    
    # Focus Indicators
    FOCUS_RING_WIDTH = dp(2)
    FOCUS_RING_COLOR = ModernColors.PRIMARY
    
    # Screen Reader
    ENABLE_SCREEN_READER_SUPPORT = True

# ============================================================================
# FEATURE FLAGS
# ============================================================================

class Features:
    """Feature flags for enabling/disabling functionality."""
    
    # UI Features
    ENABLE_ANIMATIONS = True
    ENABLE_SOUND_EFFECTS = False
    ENABLE_HAPTIC_FEEDBACK = False
    ENABLE_DARK_MODE_ONLY = True
    
    # Chat Features
    ENABLE_FILE_SHARING = True
    ENABLE_EMOJI_REACTIONS = False
    ENABLE_MESSAGE_EDITING = False
    ENABLE_MESSAGE_DELETION = False
    ENABLE_TYPING_INDICATORS = True
    
    # Advanced Features
    ENABLE_MESSAGE_ENCRYPTION = False
    ENABLE_VOICE_MESSAGES = False
    ENABLE_VIDEO_CALLS = False

# ============================================================================
# DEVELOPMENT AND DEBUG
# ============================================================================

class Debug:
    """Debug and development configurations."""
    
    # Logging
    ENABLE_VERBOSE_LOGGING = False
    LOG_NETWORK_TRAFFIC = False
    LOG_UI_EVENTS = False
    
    # Development
    SHOW_FPS_COUNTER = False
    SHOW_WIDGET_BOUNDS = False
    ENABLE_HOT_RELOAD = False

# ============================================================================
# LEGACY COMPATIBILITY
# ============================================================================

# Maintain backwards compatibility with existing code
OVERLAY_COLOR = ModernColors.OVERLAY_DARK

# Legacy color hex codes for markup text (kept for compatibility)
COLORS = {
    'success': '00ff00',
    'error': 'ff0000', 
    'warning': 'ffff00',
    'info': '00aaff',
    'username': 'ffff00',
    'own_message': '00ffff',
    'default': 'ffffff',
    'primary': '3399ff',
    'secondary': '666666'
}

# Legacy constants (kept for backwards compatibility)
USER_INFO_CARD_HEIGHT = dp(100)
MESSAGE_INPUT_HEIGHT = dp(70)
CHAT_HEADER_HEIGHT = dp(50)
USER_LIST_ITEM_HEIGHT = dp(30)
TITLE_LABEL_HEIGHT = dp(40)
LOGIN_DIALOG_SIZE = (dp(400), dp(350))
DEFAULT_SPACING = dp(10)
DEFAULT_PADDING = dp(15)
SMALL_PADDING = dp(5)
LARGE_PADDING = dp(30)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_avatar_color(username: str) -> list[float]:
    """Get consistent avatar color for a username."""
    if not username:
        return AvatarConfig.AVATAR_COLORS[0]
    
    # Simple hash to get consistent color
    hash_value = sum(ord(char) for char in username)
    color_index = hash_value % len(AvatarConfig.AVATAR_COLORS)
    return AvatarConfig.AVATAR_COLORS[color_index]


def get_message_alignment(is_own_message: bool) -> str:
    """Get message alignment based on sender."""
    return "right" if is_own_message else "left"


def get_status_color(status: str) -> list[float]:
    """Get color for connection status."""
    status_colors = {
        "Online": ModernColors.ONLINE_GREEN,
        "Offline": ModernColors.OFFLINE_GRAY,
        "Away": [1, 1, 0, 1],
        "Busy": [1, 0.3, 0.3, 1],
        "Connecting": ModernColors.PRIMARY,
        "Reconnecting": ModernColors.WARNING
    }
    return status_colors.get(status, ModernColors.OFFLINE_GRAY)


def scale_for_screen_size(base_size: float, screen_width: float) -> float:
    """Scale UI elements based on screen size."""
    if screen_width < Breakpoints.TABLET:
        return base_size * 0.9
    elif screen_width > Breakpoints.LARGE_DESKTOP:
        return base_size * 1.1
    return base_size


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_username(username: str) -> tuple[bool, str]:
    """Validate username input."""
    if not username:
        return False, ErrorMessages.NO_USERNAME
    if len(username) < InputConfig.MIN_USERNAME_LENGTH:
        return False, ErrorMessages.USERNAME_TOO_SHORT
    if len(username) > InputConfig.MAX_USERNAME_LENGTH:
        return False, f"Username too long (max {InputConfig.MAX_USERNAME_LENGTH} characters)"
    
    import re
    if not re.match(InputConfig.USERNAME_PATTERN, username):
        return False, ErrorMessages.USERNAME_INVALID
    
    return True, ""


def validate_ip_address(ip: str) -> tuple[bool, str]:
    """Validate IP address input."""
    if not ip:
        return False, ErrorMessages.NO_HOST
    
    if ip.lower() == "localhost":
        return True, ""
    
    import re
    if not re.match(InputConfig.IP_PATTERN, ip):
        return False, ErrorMessages.INVALID_IP
    
    return True, ""


def validate_message(message: str) -> tuple[bool, str]:
    """Validate message input."""
    if not message.strip():
        return False, ErrorMessages.MESSAGE_EMPTY
    if len(message) > InputConfig.MAX_MESSAGE_LENGTH:
        return False, ErrorMessages.MESSAGE_TOO_LONG.format(max_length=InputConfig.MAX_MESSAGE_LENGTH)
    
    return True, ""

# ============================================================================
# EXPORT ALL CONSTANTS
# ============================================================================

__all__ = [
    'ModernColors', 'Typography', 'Animations', 'InputConfig', 'AvatarConfig',
    'Icons', 'Emojis', 'Breakpoints', 'Performance', 'Accessibility', 'Features',
    'Debug', 'SystemMessages', 'ErrorMessages', 'THEME_COLORS',
    'DEFAULT_PORT', 'DEFAULT_HOST', 'MESSAGE_ENCODING',
    'get_avatar_color', 'get_message_alignment', 'get_status_color',
    'scale_for_screen_size', 'validate_username', 'validate_ip_address', 'validate_message'
]