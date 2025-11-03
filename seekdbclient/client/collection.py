"""
Collection class - represents a collection and provides data operation interface
"""
from typing import Any, List, Dict, Optional, Union


class Collection:
    """
    Collection class - encapsulates collection properties and data operation methods
    """
    
    def __init__(
        self,
        client: Any,  # BaseClient instance
        name: str,
        dimension: Optional[int] = None,
        **metadata
    ):
        """
        Initialize collection object
        
        Args:
            client: client instance
            name: collection name
            dimension: vector dimension
            **metadata: other metadata
        """
        self._client = client
        self._name = name
        self._dimension = dimension
        self._metadata = metadata
    
    @property
    def name(self) -> str:
        """Collection name"""
        return self._name
    
    @property
    def dimension(self) -> Optional[int]:
        """Vector dimension"""
        return self._dimension
    
    @property
    def client(self) -> Any:
        """Associated client"""
        return self._client
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """Collection metadata"""
        return self._metadata
    
    def __repr__(self) -> str:
        return f"Collection(name='{self._name}', dimension={self._dimension})"
    
    # ==================== Data Operations ====================
    
    def add(self, data: Union[Dict, List[Dict]], **kwargs) -> None:
        """
        Add data to collection
        
        Args:
            data: single data (dict) or multiple data (list of dicts)
            **kwargs: other parameters
        """
        # TODO: implement specific logic
        pass
    
    def update(self, data: Dict, filter: Optional[str] = None, **kwargs) -> None:
        """
        Update data in collection
        
        Args:
            data: data to update
            filter: filter condition
            **kwargs: other parameters
        """
        # TODO: implement specific logic
        pass
    
    def delete(
        self,
        ids: Optional[List[Union[str, int]]] = None,
        filter: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Delete data from collection
        
        Args:
            ids: list of data IDs to delete
            filter: filter condition
            **kwargs: other parameters
        """
        # TODO: implement specific logic
        pass
    
    # ==================== Data Query ====================
    
    def search(
        self,
        query_vector: Union[List[float], Dict],
        top_k: int = 10,
        output_fields: Optional[List[str]] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Vector similarity search
        
        Args:
            query_vector: query vector
            top_k: number of results to return
            output_fields: fields to return
            **kwargs: other parameters
            
        Returns:
            List of query results
        """
        # TODO: implement specific logic
        return []
    
    def get_by_id(
        self,
        ids: List[Union[str, int]],
        output_fields: Optional[List[str]] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Query data by ID
        
        Args:
            ids: list of data IDs
            output_fields: fields to return
            **kwargs: other parameters
            
        Returns:
            List of query results
        """
        # TODO: implement specific logic
        return []
    
    def query(
        self,
        filter: Optional[str] = None,
        output_fields: Optional[List[str]] = None,
        limit: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Query data by filter condition
        
        Args:
            filter: filter condition
            output_fields: fields to return
            limit: limit on number of results
            **kwargs: other parameters
            
        Returns:
            List of query results
        """
        # TODO: implement specific logic
        return []
    
    def hybrid_search(
        self,
        query_vector: Union[List[float], Dict],
        filter: Optional[str] = None,
        top_k: int = 10,
        output_fields: Optional[List[str]] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Hybrid search (vector + filter)
        
        Args:
            query_vector: query vector
            filter: filter condition
            top_k: number of results to return
            output_fields: fields to return
            **kwargs: other parameters
            
        Returns:
            List of query results
        """
        # TODO: implement specific logic
        return []
    
    # ==================== Collection Info ====================
    
    def describe(self) -> Dict[str, Any]:
        """
        Get detailed collection information
        
        Returns:
            Collection information dict
        """
        # TODO: implement specific logic
        return {
            "name": self._name,
            "dimension": self._dimension,
            **self._metadata
        }
    
    def count(self) -> int:
        """
        Get number of data in collection
        
        Returns:
            Data count
        """
        # TODO: implement specific logic
        return 0

