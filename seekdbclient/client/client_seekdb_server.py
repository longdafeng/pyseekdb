"""
Server mode client - based on pymysql
"""
import logging
from typing import Any, List, Optional, Sequence

import pymysql
from pymysql.cursors import DictCursor

from .client_base import BaseClient
from .collection import Collection
from .database import Database
from .admin_client import DEFAULT_TENANT

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
    
    # ==================== Database Management ====================
    
    def create_database(self, name: str, tenant: str = DEFAULT_TENANT) -> None:
        """
        Create database (tenant parameter ignored for server mode)
        
        Args:
            name: database name
            tenant: ignored for server mode (no tenant concept)
        """
        logger.info(f"Creating database: {name}")
        sql = f"CREATE DATABASE IF NOT EXISTS `{name}`"
        self.execute(sql)
        logger.info(f"✅ Database created: {name}")
    
    def get_database(self, name: str, tenant: str = DEFAULT_TENANT) -> Database:
        """
        Get database object (tenant parameter ignored for server mode)
        
        Args:
            name: database name
            tenant: ignored for server mode (no tenant concept)
        """
        logger.info(f"Getting database: {name}")
        sql = f"SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = '{name}'"
        result = self.execute(sql)
        
        if not result:
            raise ValueError(f"Database not found: {name}")
        
        row = result[0]
        return Database(
            name=row['SCHEMA_NAME'],
            tenant=None,  # No tenant concept in server mode
            charset=row['DEFAULT_CHARACTER_SET_NAME'],
            collation=row['DEFAULT_COLLATION_NAME']
        )
    
    def delete_database(self, name: str, tenant: str = DEFAULT_TENANT) -> None:
        """
        Delete database (tenant parameter ignored for server mode)
        
        Args:
            name: database name
            tenant: ignored for server mode (no tenant concept)
        """
        logger.info(f"Deleting database: {name}")
        sql = f"DROP DATABASE IF EXISTS `{name}`"
        self.execute(sql)
        logger.info(f"✅ Database deleted: {name}")
    
    def list_databases(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        tenant: str = DEFAULT_TENANT
    ) -> Sequence[Database]:
        """
        List all databases (tenant parameter ignored for server mode)
        
        Args:
            limit: maximum number of results to return
            offset: number of results to skip
            tenant: ignored for server mode (no tenant concept)
        """
        logger.info("Listing databases")
        sql = "SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME FROM information_schema.SCHEMATA"
        
        if limit is not None:
            if offset is not None:
                sql += f" LIMIT {offset}, {limit}"
            else:
                sql += f" LIMIT {limit}"
        
        result = self.execute(sql)
        
        databases = []
        for row in result:
            databases.append(Database(
                name=row['SCHEMA_NAME'],
                tenant=None,  # No tenant concept in server mode
                charset=row['DEFAULT_CHARACTER_SET_NAME'],
                collation=row['DEFAULT_COLLATION_NAME']
            ))
        
        logger.info(f"✅ Found {len(databases)} databases")
        return databases
    
    def __repr__(self):
        status = "connected" if self.is_connected() else "disconnected"
        return f"<SeekdbServerClient {self.user}@{self.host}:{self.port}/{self.database} status={status}>"
