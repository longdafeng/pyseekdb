"""
Base client interface definition (Server API)
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Sequence, TYPE_CHECKING

from .base_connection import BaseConnection
from .admin_client import AdminAPI, DEFAULT_TENANT

if TYPE_CHECKING:
    from .collection import Collection
    from .database import Database


class ClientAPI(ABC):
    """
    Client API interface for collection operations only.
    This is what end users interact with through the Client proxy.
    """
    
    @abstractmethod
    def create_collection(
        self,
        name: str,
        dimension: Optional[int] = None,
        **kwargs
    ) -> "Collection":
        """Create collection"""
        pass
    
    @abstractmethod
    def get_collection(self, name: str) -> "Collection":
        """Get collection object"""
        pass
    
    @abstractmethod
    def delete_collection(self, name: str) -> None:
        """Delete collection"""
        pass
    
    @abstractmethod
    def list_collections(self) -> List["Collection"]:
        """List all collections"""
        pass
    
    @abstractmethod
    def has_collection(self, name: str) -> bool:
        """Check if collection exists"""
        pass


class BaseClient(BaseConnection, AdminAPI):
    """
    Abstract base class for all clients (ServerAPI pattern).
    Provides both Collection management and Database management.
    All concrete implementations handle the actual business logic.
    Inherits connection management from BaseConnection and database operations from AdminAPI.
    """
    
    # ==================== Collection Management ====================
    
    @abstractmethod
    def create_collection(
        self,
        name: str,
        dimension: Optional[int] = None,
        **kwargs
    ) -> "Collection":
        """
        Create collection
        
        Args:
            name: collection name
            dimension: vector dimension
            **kwargs: other parameters
            
        Returns:
            Collection object
        """
        pass
    
    @abstractmethod
    def get_collection(self, name: str) -> "Collection":
        """
        Get collection object
        
        Args:
            name: collection name
            
        Returns:
            Collection object
        """
        pass
    
    @abstractmethod
    def delete_collection(self, name: str) -> None:
        """
        Delete collection
        
        Args:
            name: collection name
        """
        pass
    
    @abstractmethod
    def list_collections(self) -> List["Collection"]:
        """
        List all collections
        
        Returns:
            List of Collection objects
        """
        pass
    
    @abstractmethod
    def has_collection(self, name: str) -> bool:
        """
        Check if collection exists
        
        Args:
            name: collection name
            
        Returns:
            Whether it exists
        """
        pass
