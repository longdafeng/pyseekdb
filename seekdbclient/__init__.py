"""
SeekDBClient - Unified vector database client wrapper

Based on seekdb and pymysql, providing a simple and unified API.

Supports three modes:
1. Embedded mode - using local seekdb
2. Server mode - connecting to remote seekdb via pymysql
3. OceanBase mode - connecting to OceanBase via pymysql

Examples:
    >>> import seekdbclient

    >>> # Embedded mode
    >>> client = seekdbclient.Client(path="./seekdb", database="test")

    >>> # Server mode
    >>> client = seekdbclient.Client(
    ...     host='localhost',
    ...     port=2882,
    ...     database="test",
    ...     user="root",
    ...     password="pass"
    ... )

    >>> # OceanBase mode
    >>> ob_client = seekdbclient.OBClient(
    ...     host='localhost',
    ...     port=2881,
    ...     tenant="test",
    ...     database="test",
    ...     user="root",
    ...     password=""
    ... )
"""
import logging

from .client import (
    BaseClient,
    SeekdbEmbeddedClient,
    SeekdbServerClient,
    OceanBaseServerClient,
    Client,
    OBClient,
)
from .client.collection import Collection

__version__ = "0.1.0"
__author__ = "SeekDBClient Team"

__all__ = [
    'BaseClient',
    'SeekdbEmbeddedClient',
    'SeekdbServerClient',
    'OceanBaseServerClient',
    'Client',
    'OBClient',
    'Collection',
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

