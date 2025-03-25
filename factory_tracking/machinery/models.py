# Standard library imports for basic functionality
from enum import Enum  # For creating enumerated types
from datetime import datetime  # For handling dates and timestamps

# SQLAlchemy imports for database functionality
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum  # Database column types
from werkzeug.security import generate_password_hash, check_password_hash  # Password security functions
from database import Base  # SQLAlchemy declarative base class

# Define the possible user roles as an enumeration
# This ensures only valid roles can be assigned to users
class UserRole(Enum):
    MANAGER = "Manager"      # Can perform all operations
    TECHNICIAN = "Technician"  # Can report issues and add warnings
    REPAIR = "Repair"        # Can fix issues and remove warnings
    VIEW_ONLY = "View-only"  # Can only view information

# User model class for storing user information in the database
class User(Base):
    """
    User model representing system users with role-based access control.
    Inherits from SQLAlchemy Base class for database functionality.
    """
    __tablename__ = 'users'  # Name of the database table

    # Database columns
    id = Column(Integer, primary_key=True)  # Unique identifier for each user
    username = Column(String(50), unique=True, nullable=False)  # User's login name (must be unique)
    password_hash = Column(String(256), nullable=False)  # Stored hashed password (never plain text)
    role = Column(SQLEnum(UserRole), nullable=False)  # User's role from UserRole enum
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of account creation
    last_login = Column(DateTime)  # Timestamp of last login

    def __init__(self, username, password, role):
        """
        Initialize a new user instance
        Args:
            username (str): The user's username
            password (str): The user's plain text password (will be hashed)
            role (UserRole): The user's role in the system
        """
        self.username = username
        self.set_password(password)  # Hash password before storing
        self.role = role

    def set_password(self, password):
        """
        Hash and set the user's password
        Args:
            password (str): Plain text password to be hashed
        Note:
            Never stores the original password, only the hash
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify if the provided password matches the stored hash
        Args:
            password (str): Plain text password to check
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert user object to dictionary for API responses
        Returns:
            dict: User data safe for public consumption
                  (excludes sensitive data like password_hash)
        """
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role.value  # Convert enum to string value
        }

    # Role checking properties
    
    @property
    def is_manager(self):
        """
        Check if user has manager role
        Returns:
            bool: True if user is a manager, False otherwise
        """
        return self.role == UserRole.MANAGER

    @property
    def is_technician(self):
        """
        Check if user has technician role
        Returns:
            bool: True if user is a technician, False otherwise
        """
        return self.role == UserRole.TECHNICIAN

    @property
    def is_repair(self):
        """
        Check if user has repair role
        Returns:
            bool: True if user is a repair technician, False otherwise
        """
        return self.role == UserRole.REPAIR

    @property
    def is_view_only(self):
        """
        Check if user has view-only role
        Returns:
            bool: True if user has view-only access, False otherwise
        """
        return self.role == UserRole.VIEW_ONLY 