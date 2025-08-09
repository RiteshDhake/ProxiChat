"""
Constants and configuration values for the UI components.
"""

from kivy.metrics import dp

# Window Configuration
WINDOW_SIZE = (1000, 700)
MIN_WINDOW_SIZE = (800, 600)

# Layout Ratios
SIDEBAR_WIDTH_RATIO = 0.25
CHAT_AREA_WIDTH_RATIO = 0.75
MESSAGE_CARD_WIDTH_RATIO = 0.7

# Spacing and Padding
DEFAULT_SPACING = dp(10)
DEFAULT_PADDING = dp(15)
SMALL_PADDING = dp(5)
LARGE_PADDING = dp(30)

# Component Heights
USER_INFO_CARD_HEIGHT = dp(100)
MESSAGE_INPUT_HEIGHT = dp(70)
CHAT_HEADER_HEIGHT = dp(50)
USER_LIST_ITEM_HEIGHT = dp(30)
TITLE_LABEL_HEIGHT = dp(40)

# Component Sizes
LOGIN_DIALOG_SIZE = (dp(400), dp(350))

# Input Field Configurations
MAX_USERNAME_LENGTH = 128
MAX_IP_LENGTH = 15

# Colors (RGB tuples for md_bg_color)
OVERLAY_COLOR = (0, 0, 0, 0.7)

# Color hex codes for markup text
COLORS = {
    'success': '00ff00',    # Green
    'error': 'ff0000',      # Red  
    'warning': 'ffff00',    # Yellow
    'info': '00ff00',       # Green
    'username': 'ffff00',   # Yellow
    'own_message': '00ffff', # Cyan
    'default': 'ffffff'     # White
}

# Theme Configuration
THEME_STYLE = "Dark"
PRIMARY_PALETTE = "Indigo"

# Network Configuration
DEFAULT_PORT = 1234
DEFAULT_HOST = "127.0.0.1"
MESSAGE_ENCODING = 'utf-8'

# File Transfer
FILE_TRANSFER_SIGNAL = "sending_file"
FILE_END_MARKER = b"<END>"
RECV_FILE_NAME = "Recv_file.txt"
BUFFER_SIZE = 1024

# UI Text Constants
APP_TITLE = "Chattr - Desktop Chat Application"
LOGIN_DIALOG_TITLE = "Join Chat Server"
CHAT_HEADER_TITLE = "General Chat"
ONLINE_USERS_TITLE = "Online Users"

# Placeholder texts
USERNAME_HINT = "Username"
IP_HINT = "Server IP address"
MESSAGE_HINT = "Type your message here..."

# Button texts
CONNECT_BUTTON_TEXT = "Connect"
SEND_BUTTON_TEXT = "Send"
FILE_BUTTON_TEXT = "File"

# Status messages
STATUS_ONLINE = "Online"
STATUS_OFFLINE = "Offline" 
STATUS_NOT_CONNECTED = "Not Connected"

# System messages
MSG_CONNECTED = "Connected to server"
MSG_DISCONNECTED = "Disconnected from server"
MSG_CONNECTION_FAILED = "Connection failed"
MSG_FILE_RECEIVED = "File received"
MSG_FILE_SENT = "File sent"

# Error messages
ERROR_NO_USERNAME = "Please enter a username"
ERROR_NO_HOST = "Please enter a server IP address"
ERROR_INVALID_IP = "Please enter a valid IP address"
ERROR_CONNECTION_LOST = "Connection lost"
ERROR_SEND_FAILED = "Failed to send message"
ERROR_FILE_SEND_FAILED = "Failed to send file"
ERROR_FILE_RECEIVE_FAILED = "Failed to receive file"
ERROR_NOT_CONNECTED = "Not connected to server"

# Icon names (Material Design Icons)
ICONS = {
    'account': 'account',
    'ip': 'ip',
    'connect': 'transit-connection-variant',
    'send': 'send',
    'file': 'file',
    'online': 'circle',
    'offline': 'circle-outline'
}