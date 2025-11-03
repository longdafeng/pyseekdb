"""
OceanBase mode client - based on pymysql
"""
import logging
from typing import Any, List, Optional

import pymysql
from pymysql.cursors import DictCursor

from .client_base import BaseClient
from .collection import Collection

logger = logging.getLogger(__name__)


class OceanBaseServerClient(BaseClient):
    """OceanBase database client (based on pymysql, lazy connection)"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 2881,
        tenant: str = "test",
        database: str = "test",
        user: str = "root",
        password: str = "",
        **kwargs
    ):
        """
        Initialize OceanBase client (no immediate connection)
        
        Args:
            host: OceanBase server address
            port: OceanBase server port (default 2881)
            tenant: tenant name
            database: database name
            user: username (without tenant suffix)
            password: password
            **kwargs: other pymysql connection parameters
        """
        self.host = host
        self.port = port
        self.tenant = tenant
        self.database = database
        self.user = user
        self.password = password
        self.kwargs = kwargs
        
        # OceanBase username format: user@tenant
        self.full_user = f"{user}@{tenant}"
        self._connection: Optional[pymysql.Connection] = None
        
        logger.info(
            f"Initialize OceanBaseServerClient: {self.full_user}@{self.host}:{self.port}/{self.database}"
        )
    
    # ==================== Connection Management ====================
    
    def _ensure_connection(self) -> pymysql.Connection:
        """Ensure connection is established (internal method)"""
        if self._connection is None or not self._connection.open:
            self._connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.full_user,  # OceanBase format: user@tenant
                password=self.password,
                database=self.database,
                cursorclass=DictCursor,
                **self.kwargs
            )
            logger.info(f"✅ Connected to OceanBase: {self.host}:{self.port}/{self.database}")
        
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
        return "OceanBaseServerClient"
    
    # ==================== Collection Management (framework) ====================
    
    def create_collection(
        self,
        name: str,
        dimension: Optional[int] = None,
        **kwargs
    ) -> Collection:
        """Create collection"""
        logger.info(f"OceanBaseServerClient: create_collection framework for {name} (dim={dimension})")
        # TODO: implement OceanBase create_collection logic
        # Return Collection object after creating table
        return Collection(client=self, name=name, dimension=dimension, **kwargs)
    
    def get_collection(self, name: str) -> Collection:
        """Get collection object"""
        logger.info(f"OceanBaseServerClient: get_collection framework for {name}")
        # TODO: implement OceanBase get_collection logic
        # Return Collection object after getting table info
        return Collection(client=self, name=name)
    
    def delete_collection(self, name: str) -> None:
        """Delete collection"""
        logger.info(f"OceanBaseServerClient: delete_collection framework for {name}")
        # TODO: implement OceanBase delete_collection logic
        pass
    
    def list_collections(self) -> List[Collection]:
        """List all collections"""
        logger.info("OceanBaseServerClient: list_collections framework")
        # TODO: implement OceanBase list_collections logic
        # Return list of Collection objects
        return []
    
    def has_collection(self, name: str) -> bool:
        """Check if collection exists"""
        logger.info(f"OceanBaseServerClient: has_collection framework for {name}")
        # TODO: implement OceanBase has_collection logic
        return False
    
    def __repr__(self):
        status = "connected" if self.is_connected() else "disconnected"
        return f"<OceanBaseServerClient {self.full_user}@{self.host}:{self.port}/{self.database} status={status}>"
