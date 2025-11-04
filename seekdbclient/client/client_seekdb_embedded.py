"""
Embedded mode client - based on seekdb
"""
import os
import logging
from typing import Any, List, Optional, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    import seekdb  # type: ignore

from .client_base import BaseClient
from .collection import Collection
from .database import Database
from .admin_client import DEFAULT_TENANT

logger = logging.getLogger(__name__)


class SeekdbEmbeddedClient(BaseClient):
    """Embedded SeekDB client (lazy connection)"""
    
    def __init__(
        self,
        path: str = "./seekdb",
        database: str = "test",
        autocommit: bool = False,
        **kwargs
    ):
        """
        Initialize embedded client (no immediate connection)
        
        Args:
            path: seekdb data directory path
            database: database name
            autocommit: whether to auto-commit
        """
        self.path = os.path.abspath(path)
        self.database = database
        self.autocommit = autocommit
        self._connection = None
        self._initialized = False
        
        logger.info(f"Initialize SeekdbEmbeddedClient: path={self.path}, database={self.database}")
    
    # ==================== Connection Management ====================
    
    def _ensure_connection(self) -> Any:  # seekdb.Connection
        """Ensure connection is established (internal method)"""
        # Lazy import seekdb to avoid importing during module load
        # Note: temporarily remove project root and clean module cache to avoid naming conflict with seekdb C extension (pyseekdb.so)
        import sys
        import importlib
        
        project_root = "/home/lyl512932/pythonSDK/pyobvector"
        root_was_in_path = project_root in sys.path
        
        # Clean possibly contaminated seekdb module
        if 'seekdb' in sys.modules:
            seekdb_mod = sys.modules['seekdb']
            # Check if contaminated (has our classes)
            if hasattr(seekdb_mod, 'SeekdbEmbeddedClient'):
                logger.warning("Detected seekdb module contamination, reloading...")
                del sys.modules['seekdb']
        
        if root_was_in_path:
            sys.path.remove(project_root)
        
        try:
            import seekdb  # type: ignore
            
            # Initialize seekdb module while sys.path still does not contain project root
            if not self._initialized:
                # 1. Check if data directory exists
                if not os.path.exists(self.path):
                    raise FileNotFoundError(f"SeekDB data directory does not exist: {self.path}")
                
                # 2. Ensure seekdb module is properly initialized
                if not hasattr(seekdb, 'open'):
                    logger.info("SeekDB module needs initialization, calling _initialize_module()...")
                    attrs = seekdb._initialize_module()  # type: ignore
                    logger.info(f"SeekDB initialization complete, loaded {len(attrs)} attributes: {attrs}")
                    
                    # Check again
                    if not hasattr(seekdb, 'open'):
                        raise RuntimeError(
                            "SeekDB module initialization failed: missing 'open' method."
                            "Please ensure seekdb and seekdb-lib are properly installed."
                        )
        finally:
            if root_was_in_path:
                sys.path.insert(0, project_root)
        
        if not self._initialized:
            
            # 3. Switch to data directory and open
            original_dir = os.getcwd()
            try:
                os.chdir(self.path)
                try:
                    seekdb.open()  # type: ignore
                    logger.info(f"✅ SeekDB opened: {self.path}")
                except Exception as e:
                    if "initialized twice" not in str(e):
                        raise
                    logger.debug(f"SeekDB already opened: {e}")
            finally:
                os.chdir(original_dir)
            
            self._initialized = True
        
        # 4. Create connection
        if self._connection is None:
            self._connection = seekdb.connect(  # type: ignore
                db_name=self.database,
                autocommit=self.autocommit
            )
            logger.info(f"✅ Connected to database: {self.database}")
        
        return self._connection
    
    def _cleanup(self):
        """Internal cleanup method: close connection)"""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            logger.info("Connection closed")
    
    def is_connected(self) -> bool:
        """Check connection status"""
        return self._connection is not None and self._initialized
    
    def execute(self, sql: str) -> Any:
        """Execute SQL statement"""
        conn = self._ensure_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            
            if sql.strip().upper().startswith('SELECT') or sql.strip().upper().startswith('SHOW'):
                return cursor.fetchall()
            
            if not self.autocommit:
                conn.commit()
            
            return cursor
        except Exception as e:
            if not self.autocommit:
                conn.rollback()
            raise e
    
    def get_raw_connection(self) -> Any:  # seekdb.Connection
        """Get raw connection object"""
        return self._ensure_connection()
    
    @property
    def mode(self) -> str:
        return "SeekdbEmbeddedClient"
    
    # ==================== Collection Management (framework) ====================
    
    def create_collection(
        self,
        name: str,
        dimension: Optional[int] = None,
        **kwargs
    ) -> Collection:
        """Create collection"""
        logger.info(f"SeekdbEmbeddedClient: create_collection framework for {name} (dim={dimension})")
        # TODO: implement seekdb create_collection logic
        # Return Collection object after creating table
        return Collection(client=self, name=name, dimension=dimension, **kwargs)
    
    def get_collection(self, name: str) -> Collection:
        """Get collection object"""
        logger.info(f"SeekdbEmbeddedClient: get_collection framework for {name}")
        # TODO: implement seekdb get_collection logic
        # Return Collection object after getting table info
        return Collection(client=self, name=name)
    
    def delete_collection(self, name: str) -> None:
        """Delete collection"""
        logger.info(f"SeekdbEmbeddedClient: delete_collection framework for {name}")
        # TODO: implement seekdb delete_collection logic
        pass
    
    def list_collections(self) -> List[Collection]:
        """List all collections"""
        logger.info("SeekdbEmbeddedClient: list_collections framework")
        # TODO: implement seekdb list_collections logic
        # Return list of Collection objects
        return []
    
    def has_collection(self, name: str) -> bool:
        """Check if collection exists"""
        logger.info(f"SeekdbEmbeddedClient: has_collection framework for {name}")
        # TODO: implement seekdb has_collection logic
        return False
    
    # ==================== Database Management ====================
    
    def create_database(self, name: str, tenant: str = DEFAULT_TENANT) -> None:
        """
        Create database (tenant parameter ignored for embedded mode)
        
        Args:
            name: database name
            tenant: ignored for embedded mode (no tenant concept)
        """
        logger.info(f"Creating database: {name}")
        sql = f"CREATE DATABASE IF NOT EXISTS `{name}`"
        self.execute(sql)
        logger.info(f"✅ Database created: {name}")
    
    def get_database(self, name: str, tenant: str = DEFAULT_TENANT) -> Database:
        """
        Get database object (tenant parameter ignored for embedded mode)
        
        Args:
            name: database name
            tenant: ignored for embedded mode (no tenant concept)
        """
        logger.info(f"Getting database: {name}")
        sql = f"SELECT SCHEMA_NAME, DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = '{name}'"
        result = self.execute(sql)
        
        if not result:
            raise ValueError(f"Database not found: {name}")
        
        row = result[0]
        return Database(
            name=row[0] if isinstance(row, tuple) else row.get('SCHEMA_NAME'),
            tenant=None,  # No tenant concept in embedded mode
            charset=row[1] if isinstance(row, tuple) else row.get('DEFAULT_CHARACTER_SET_NAME'),
            collation=row[2] if isinstance(row, tuple) else row.get('DEFAULT_COLLATION_NAME')
        )
    
    def delete_database(self, name: str, tenant: str = DEFAULT_TENANT) -> None:
        """
        Delete database (tenant parameter ignored for embedded mode)
        
        Args:
            name: database name
            tenant: ignored for embedded mode (no tenant concept)
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
        List all databases (tenant parameter ignored for embedded mode)
        
        Args:
            limit: maximum number of results to return
            offset: number of results to skip
            tenant: ignored for embedded mode (no tenant concept)
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
                name=row[0] if isinstance(row, tuple) else row.get('SCHEMA_NAME'),
                tenant=None,  # No tenant concept in embedded mode
                charset=row[1] if isinstance(row, tuple) else row.get('DEFAULT_CHARACTER_SET_NAME'),
                collation=row[2] if isinstance(row, tuple) else row.get('DEFAULT_COLLATION_NAME')
            ))
        
        logger.info(f"✅ Found {len(databases)} databases")
        return databases
    
    def __repr__(self):
        status = "connected" if self.is_connected() else "disconnected"
        return f"<SeekdbEmbeddedClient path={self.path} database={self.database} status={status}>"
