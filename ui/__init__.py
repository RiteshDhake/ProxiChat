"""
Enhanced UI module initialization with modern components.
This file replaces your existing __init__.py
"""

# Import enhanced components
from .components import (
    MessageCard, 
    MessageContainer,
    EnhancedUserListItem,
    ChatHeader,
    MessageInputCard,
    SystemMessageCard,
)

from .login_dialog import (
    EnhancedLoginDialog,
    LoginDialogManager,
    # GradientCard,
    PulsingIcon,
    AnimatedLabel
)

from .sidebar import (
    EnhancedSidebar,
    UserInfoCard,
    OnlineUsersCard
)

from .chat_interface import (
    ModernChatInterface,
    ModernTheme
)

from .constants import (
    ModernColors,
    Typography,
    Animations,
    InputConfig,
    AvatarConfig,
    Icons,
    Emojis,
    SystemMessages,
    ErrorMessages,
    Features,
    get_avatar_color,
    get_status_color,
    validate_username,
    validate_ip_address,
    validate_message
)

# ============================================================================
# PUBLIC API - Main Components
# ============================================================================

# Primary interface component
ChatInterface = ModernChatInterface

# Core UI components
__all__ = [
    # Main Interface
    'ModernChatInterface',
    'ChatInterface',  # Alias for backwards compatibility
    
    # Component Classes
    'MessageCard',
    'MessageContainer', 
    'EnhancedUserListItem',
    'ChatHeader',
    'MessageInputCard',
    'SystemMessageCard',
    
    # Enhanced Components
    'GradientCard',
    'AnimatedLabel',
    'PulsingIcon',
    
    # Dialog Components
    'EnhancedLoginDialog',
    'LoginDialogManager',
    
    # Sidebar Components
    'EnhancedSidebar',
    'UserInfoCard',
    'OnlineUsersCard',
    
    # Theme and Styling
    'ModernTheme',
    'ModernColors',
    'Typography',
    'Animations',
    
    # Configuration
    'InputConfig',
    'AvatarConfig',
    'Icons',
    'Emojis',
    'SystemMessages',
    'ErrorMessages',
    'Features',
    
    # Utility Functions
    'get_avatar_color',
    'get_status_color',
    'validate_username',
    'validate_ip_address',
    'validate_message'
]

# ============================================================================
# BACKWARDS COMPATIBILITY ALIASES
# ============================================================================

# Legacy component names for existing code
UserListItem = EnhancedUserListItem
LoginDialog = EnhancedLoginDialog
Sidebar = EnhancedSidebar

# ============================================================================
# VERSION INFORMATION
# ============================================================================

__version__ = "2.0.0"
__author__ = "Chattr Development Team"
__description__ = "Modern UI components for desktop chat application"

# ============================================================================
# QUICK START GUIDE
# ============================================================================

"""
QUICK START GUIDE:

1. Import the main interface:
   ```python
   from ui import ModernChatInterface
   ```

2. Create and configure the interface:
   ```python
   chat_interface = ModernChatInterface()
   chat_interface.set_callbacks(
       send_message_callback=your_send_function,
       send_file_callback=your_file_function,
       connect_callback=your_connect_function
   )
   ```

3. Show login dialog:
   ```python
   chat_interface.show_login_dialog("default_username", "192.168.1.100")
   ```

4. Handle user events:
   ```python
   # Display received message
   chat_interface.display_message("username", "message content")
   
   # Update user status
   chat_interface.user_joined("new_user")
   chat_interface.user_left("leaving_user")
   
   # Show system messages
   chat_interface.add_enhanced_system_message("Server restarted", "info")
   ```

5. Use modern styling:
   ```python
   from ui.constants import ModernColors, Typography, Icons
   
   # Apply consistent colors
   widget.md_bg_color = ModernColors.CARD_BACKGROUND
   
   # Use standardized typography
   label.font_size = Typography.BODY_LARGE
   
   # Consistent iconography
   button.icon = Icons.SEND
   ```

KEY FEATURES:
- Dark theme with glassmorphism effects
- Smooth animations and transitions
- Enhanced user feedback
- Modern typography and spacing
- Responsive design elements
- Accessibility improvements
- Performance optimizations

MIGRATION FROM OLD UI:
- Replace 'ChatInterface' with 'ModernChatInterface'
- Update color references to use ModernColors class
- Replace manual styling with Typography constants
- Use new validation functions for inputs
- Enhanced error handling and user feedback
"""