"""
SeekDBClient client module

Provides three client modes:
1. Embedded mode (SeekdbEmbeddedClient) - using seekdb
2. Server mode (SeekdbServerClient) - using pymysql
3. OceanBase mode (OceanBaseServerClient) - using pymysql
"""
import logging
from typing import Optional, Union

from .client_base import BaseClient
from .client_seekdb_embedded import SeekdbEmbeddedClient
from .client_seekdb_server import SeekdbServerClient
from .client_oceanbase_server import OceanBaseServerClient

logger = logging.getLogger(__name__)

__all__ = [
    'BaseClient',
    'SeekdbEmbeddedClient',
    'SeekdbServerClient',
    'OceanBaseServerClient',
    'Client',
    'OBClient',
]


def Client(
    path: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    database: str = "test",
    user: Optional[str] = None,
    password: str = "",
    **kwargs
) -> Union[SeekdbEmbeddedClient, SeekdbServerClient]:
    """
    Smart client factory function
    
    Automatically selects embedded or server mode based on parameters:
    - If path is provided, uses embedded mode
    - If host/port is provided, uses server mode
    
    Args:
        path: seekdb data directory path (embedded mode)
        host: server address (server mode)
        port: server port (server mode)
        database: database name
        user: username (server mode)
        password: password (server mode)
        **kwargs: other parameters
    
    Returns:
        SeekdbEmbeddedClient or SeekdbServerClient
    
    Examples:
        >>> # Embedded mode
        >>> client = Client(path="/path/to/seekdb", database="db1")
        
        >>> # Server mode
        >>> client = Client(
        ...     host='localhost',
        ...     port=2882,
        ...     database="db1",
        ...     user="u01",
        ...     password="pass"
        ... )
    """
    # Determine mode
    if path is not None:
        # Embedded mode
        logger.info(f"Creating embedded client: path={path}, database={database}")
        return SeekdbEmbeddedClient(
            path=path,
            database=database,
            **kwargs
        )
    
    elif host is not None:
        # Server mode
        if port is None:
            port = 2882  # Default port
        if user is None:
            user = "root"
        
        logger.info(
            f"Creating server mode client: {user}@{host}:{port}/{database}"
        )
        return SeekdbServerClient(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            **kwargs
        )
    
    else:
        raise ValueError(
            "Must provide either path (embedded mode) or host (server mode) parameter"
        )


def OBClient(
    host: str = "localhost",
    port: int = 2881,
    tenant: str = "test",
    database: str = "test",
    user: str = "root",
    password: str = "",
    **kwargs
) -> OceanBaseServerClient:
    """
    OceanBase client factory function
    
    Args:
        host: server address
        port: server port (default 2881)
        tenant: tenant name
        database: database name
        user: username (without tenant suffix)
        password: password
        **kwargs: other parameters
    
    Returns:
        OceanBaseServerClient
    
    Examples:
        >>> client = OBClient(
        ...     host='localhost',
        ...     port=2881,
        ...     tenant="tenant1",
        ...     database="db1",
        ...     user="u01",
        ...     password="pass"
        ... )
    """
    logger.info(
        f"Creating OceanBase client: {user}@{tenant}@{host}:{port}/{database}"
    )
    
    return OceanBaseServerClient(
        host=host,
        port=port,
        tenant=tenant,
        database=database,
        user=user,
        password=password,
        **kwargs
    )

