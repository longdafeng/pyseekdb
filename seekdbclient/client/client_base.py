"""
Base client interface definition
"""
from abc import ABC, abstractmethod
from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .collection import Collection


class BaseClient(ABC):
    """
    Abstract base class for all clients, defining a unified interface.
    Data operations are performed through Collection objects.
    """
    
    # ==================== Connection Management ====================
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check connection status"""
        pass
    
    @abstractmethod
    def _cleanup(self):
        """Internal cleanup method to close connection and release resources"""
        pass
    
    @abstractmethod
    def execute(self, sql: str) -> Any:
        """Execute SQL statement (basic functionality)"""
        pass
    
    @abstractmethod
    def get_raw_connection(self) -> Any:
        """Get raw connection object"""
        pass
    
    @property
    @abstractmethod
    def mode(self) -> str:
        """Return client mode (e.g., 'SeekdbEmbeddedClient', 'SeekdbServerClient', 'OceanBaseServerClient')"""
        pass
    
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
    
    # ==================== Context Manager ====================
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support: automatic resource cleanup"""
        self._cleanup()
    
    def __del__(self):
        """Destructor: ensure connection is closed to prevent resource leaks"""
        try:
            if hasattr(self, '_connection') and self.is_connected():
                self._cleanup()
        except Exception:
            # Ignore all exceptions in destructor
            # Avoid issues during interpreter shutdown
            pass
