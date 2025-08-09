"""
Sidebar component for displaying user information and online users.
"""

from kivymd.uix.boxlayout import MDBoxLayout
from .components import UserInfoCard, OnlineUsersCard
from kivy.metrics import dp
from typing import List


class Sidebar(MDBoxLayout):
    """Sidebar containing user info and online users list."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_users: List[str] = []
        self.setup_sidebar()
    
    def setup_sidebar(self):
        """Setup the sidebar layout and components."""
        self.orientation = "vertical"
        self.size_hint_x = 0.25  # 25% of screen width
        self.padding = [dp(0), dp(0), dp(0), dp(0)]
        self.spacing = dp(10)
        
        # Create user info card
        self.user_info_card = UserInfoCard()
        self.add_widget(self.user_info_card)
        
        # Create online users card
        self.online_users_card = OnlineUsersCard()
        self.add_widget(self.online_users_card)
    
    def update_user_info(self, username: str, status: str = "Online"):
        """Update the current user's information."""
        self.user_info_card.update_user_info(username, status)
    
    def add_active_user(self, username: str):
        """Add a user to the active users list."""
        if username not in self.active_users:
            self.active_users.append(username)
            self.update_users_list()
    
    def remove_active_user(self, username: str):
        """Remove a user from the active users list."""
        if username in self.active_users:
            self.active_users.remove(username)
            self.update_users_list()
    
    def update_users_list(self):
        """Update the online users display."""
        self.online_users_card.update_users_list(self.active_users)
    
    def clear_users_list(self):
        """Clear all users from the list."""
        self.active_users.clear()
        self.update_users_list()
    
    def get_active_users(self) -> List[str]:
        """Get the list of active users."""
        return self.active_users.copy()
    
    def get_user_count(self) -> int:
        """Get the number of active users."""
        return len(self.active_users)
    
    def set_user_offline(self):
        """Set the current user as offline."""
        current_username = self.user_info_card.username
        if current_username != "Not Connected":
            self.user_info_card.update_user_info(current_username, "Offline")
    
    def set_user_online(self, username: str):
        """Set the current user as online."""
        self.user_info_card.update_user_info(username, "Online")
    
    def reset_sidebar(self):
        """Reset the sidebar to initial state."""
        self.user_info_card.update_user_info("Not Connected", "Offline")
        self.clear_users_list()