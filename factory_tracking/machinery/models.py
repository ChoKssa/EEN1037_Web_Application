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

    @classmethod
    def create_user(cls, username, password, role, created_by=None):
        """
        Create a new user with role validation
        Args:
            username (str): The user's username
            password (str): The user's plain text password
            role (str): The user's role (must match UserRole enum)
            created_by (User): The manager creating the user
        Returns:
            User: New user instance
        Raises:
            RoleError: If creator doesn't have permission or role is invalid
        """
        # Validate that only managers can create users
        if created_by and not created_by.is_manager:
            raise RoleError("Only managers can create new users")

        # Validate and convert role string to enum
        try:
            role_enum = UserRole[role.upper()]
        except KeyError:
            raise RoleError(f"Invalid role: {role}. Must be one of {[r.name for r in UserRole]}")

        return cls(username=username, password=password, role=role_enum)

    def update_role(self, new_role, updated_by):
        """
        Update user's role with proper validation
        Args:
            new_role (str): New role to assign
            updated_by (User): The manager updating the role
        Raises:
            RoleError: If updater doesn't have permission or role is invalid
        """
        # Validate that only managers can update roles
        if not updated_by.is_manager:
            raise RoleError("Only managers can update user roles")

        # Validate and convert role string to enum
        try:
            role_enum = UserRole[new_role.upper()]
        except KeyError:
            raise RoleError(f"Invalid role: {new_role}. Must be one of {[r.name for r in UserRole]}")

        self.role = role_enum

    def can_manage_machines(self):
        """
        Check if user can manage (create/update/delete) machines
        Returns:
            bool: True if user has machine management permissions
        """
        return self.is_manager

    def can_manage_warnings(self):
        """
        Check if user can manage machine warnings
        Returns:
            bool: True if user can add/remove warnings
        """
        return self.is_technician or self.is_repair

    def can_create_fault_reports(self):
        """
        Check if user can create fault reports
        Returns:
            bool: True if user can create fault reports
        """
        return self.is_technician

    def can_manage_repairs(self):
        """
        Check if user can manage repairs
        Returns:
            bool: True if user can manage repairs
        """
        return self.is_repair

    def has_access_to_machine(self, machine):
        """
        Check if user has access to a specific machine
        Args:
            machine: Machine instance to check access for
        Returns:
            bool: True if user has access to the machine
        """
        # Managers have access to all machines
        if self.is_manager:
            return True
        
        # View-only users can view but not modify
        if self.is_view_only:
            return True

        # Technicians and Repairers can access assigned machines
        if self.is_technician or self.is_repair:
            return self in machine.assigned_users

        return False

class RoleError(Exception):
    """Custom exception for role-related errors"""
    pass


    

