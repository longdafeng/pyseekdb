"""
OceanBase mode client - based on pymysql
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
    
    # ==================== Database Management ====================
    
    def create_database(self, name: str, tenant: str = DEFAULT_TENANT) -> None:
        """
        Create database (OceanBase has tenant concept, uses client's tenant)
        
        Args:
            name: database name
            tenant: tenant name (if different from client tenant, will use client tenant)
        
        Note:
            OceanBase has multi-tenant architecture. Database is scoped to client's tenant.
        """
        if tenant != self.tenant and tenant != DEFAULT_TENANT:
            logger.warning(f"Specified tenant '{tenant}' differs from client tenant '{self.tenant}', using client tenant")
        
        logger.info(f"Creating database: {name} in tenant: {self.tenant}")
        sql = f"CREATE DATABASE IF NOT EXISTS `{name}`"
        self.execute(sql)
        logger.info(f"✅ Database created: {name} in tenant: {self.tenant}")
    
    def get_database(self, name: str, tenant: str = DEFAULT_TENANT) -> Database:
        """
        Get database object (OceanBase has tenant concept, uses client's tenant)
        
        Args:
            name: database name
            tenant: tenant name (if different from client tenant, will use client tenant)
        
        Returns:
            Database object with tenant information
        
        Note:
            OceanBase has multi-tenant architecture. Database is scoped to client's tenant.
        """
        if tenant != self.tenant and tenant != DEFAULT_TENANT:
            logger.warning(f"Specified tenant '{tenant}' differs from client tenant '{self.tenant}', using client tenant")
        
        logger.info(f"Getting database: {name} in tenant: {self.tenant}")
        sql = f"SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = '{name}'"
        result = self.execute(sql)
        
        if not result:
            raise ValueError(f"Database not found: {name}")
        
        row = result[0]
        return Database(
            name=row['SCHEMA_NAME'],
            tenant=self.tenant,  # OceanBase has tenant concept
            charset=row['DEFAULT_CHARACTER_SET_NAME'],
            collation=row['DEFAULT_COLLATION_NAME']
        )
    
    def delete_database(self, name: str, tenant: str = DEFAULT_TENANT) -> None:
        """
        Delete database (OceanBase has tenant concept, uses client's tenant)
        
        Args:
            name: database name
            tenant: tenant name (if different from client tenant, will use client tenant)
        
        Note:
            OceanBase has multi-tenant architecture. Database is scoped to client's tenant.
        """
        if tenant != self.tenant and tenant != DEFAULT_TENANT:
            logger.warning(f"Specified tenant '{tenant}' differs from client tenant '{self.tenant}', using client tenant")
        
        logger.info(f"Deleting database: {name} in tenant: {self.tenant}")
        sql = f"DROP DATABASE IF EXISTS `{name}`"
        self.execute(sql)
        logger.info(f"✅ Database deleted: {name} in tenant: {self.tenant}")
    
    def list_databases(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        tenant: str = DEFAULT_TENANT
    ) -> Sequence[Database]:
        """
        List all databases (OceanBase has tenant concept, uses client's tenant)
        
        Args:
            limit: maximum number of results to return
            offset: number of results to skip
            tenant: tenant name (if different from client tenant, will use client tenant)
        
        Returns:
            Sequence of Database objects with tenant information
        
        Note:
            OceanBase has multi-tenant architecture. Lists databases in client's tenant.
        """
        if tenant != self.tenant and tenant != DEFAULT_TENANT:
            logger.warning(f"Specified tenant '{tenant}' differs from client tenant '{self.tenant}', using client tenant")
        
        logger.info(f"Listing databases in tenant: {self.tenant}")
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
                tenant=self.tenant,  # OceanBase has tenant concept
                charset=row['DEFAULT_CHARACTER_SET_NAME'],
                collation=row['DEFAULT_COLLATION_NAME']
            ))
        
        logger.info(f"✅ Found {len(databases)} databases in tenant {self.tenant}")
        return databases
    
    def __repr__(self):
        status = "connected" if self.is_connected() else "disconnected"
        return f"<OceanBaseServerClient {self.full_user}@{self.host}:{self.port}/{self.database} status={status}>"
