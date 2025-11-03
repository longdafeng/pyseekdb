"""
Server mode client - based on pymysql
"""
import logging
from typing import Any, List, Optional

import pymysql
from pymysql.cursors import DictCursor

from .client_base import BaseClient
from .collection import Collection

logger = logging.getLogger(__name__)


class SeekdbServerClient(BaseClient):
    """SeekDB server mode client (connecting via pymysql, lazy loading)"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 2882,
        database: str = "test",
        user: str = "root",
        password: str = "",
        charset: str = "utf8mb4",
        **kwargs
    ):
        """
        Initialize server mode client (no immediate connection)
        
        Args:
            host: server address
            port: server port
            database: database name
            user: username
            password: password
            charset: charset
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset
        self.kwargs = kwargs
        self._connection = None
        
        logger.info(
            f"Initialize SeekdbServerClient: {self.user}@{self.host}:{self.port}/{self.database}"
        )
    
    # ==================== Connection Management ====================
    
    def _ensure_connection(self) -> pymysql.Connection:
        """Ensure connection is established (internal method)"""
        if self._connection is None or not self._connection.open:
            self._connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                cursorclass=DictCursor,
                **self.kwargs
            )
            logger.info(f"✅ Connected to server: {self.host}:{self.port}/{self.database}")
        
        return self._connection
    
    def _cleanup(self):
        """Internal cleanup method: close connection)"""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            logger.info("Connection closed")
    
    def is_connected(self) -> bool:
        """Check connection status"""
        return self._connection is not None and self._connection.open
    
    def execute(self, sql: str) -> Any:
        """Execute SQL statement"""
        conn = self._ensure_connection()
        
        with conn.cursor() as cursor:
            cursor.execute(sql)
            
            if sql.strip().upper().startswith('SELECT') or sql.strip().upper().startswith('SHOW'):
                return cursor.fetchall()
            
            conn.commit()
            return cursor
    
    def get_raw_connection(self) -> pymysql.Connection:
        """Get raw connection object"""
        return self._ensure_connection()
    
    @property
    def mode(self) -> str:
        return "SeekdbServerClient"
    
    # ==================== Collection Management (framework) ====================
    
    def create_collection(
        self,
        name: str,
        dimension: Optional[int] = None,
        **kwargs
    ) -> Collection:
        """Create collection"""
        logger.info(f"SeekdbServerClient: create_collection framework for {name} (dim={dimension})")
        # TODO: implement PyMySQL create_collection logic
        # Return Collection object after creating table
        return Collection(client=self, name=name, dimension=dimension, **kwargs)
    
    def get_collection(self, name: str) -> Collection:
        """Get collection object"""
        logger.info(f"SeekdbServerClient: get_collection framework for {name}")
        # TODO: implement PyMySQL get_collection logic
        # Return Collection object after getting table info
        return Collection(client=self, name=name)
    
    def delete_collection(self, name: str) -> None:
        """Delete collection"""
        logger.info(f"SeekdbServerClient: delete_collection framework for {name}")
        # TODO: implement PyMySQL delete_collection logic
        pass
    
    def list_collections(self) -> List[Collection]:
        """List all collections"""
        logger.info("SeekdbServerClient: list_collections framework")
        # TODO: implement PyMySQL list_collections logic
        # Return list of Collection objects
        return []
    
    def has_collection(self, name: str) -> bool:
        """Check if collection exists"""
        logger.info(f"SeekdbServerClient: has_collection framework for {name}")
        # TODO: implement PyMySQL has_collection logic
        return False
    
    def __repr__(self):
        status = "connected" if self.is_connected() else "disconnected"
        return f"<SeekdbServerClient {self.user}@{self.host}:{self.port}/{self.database} status={status}>"
