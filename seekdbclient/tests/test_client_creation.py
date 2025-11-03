"""
Client creation and connection tests - testing connection and query execution for all three modes
Supports configuring connection parameters via environment variables
"""
import pytest
import sys
import os
from pathlib import Path

# Add project path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import seekdbclient


# ==================== Environment Variable Configuration ====================
# Embedded mode
SEEKDB_PATH = os.environ.get('SEEKDB_PATH', os.path.join(project_root, "seekdb"))
SEEKDB_DATABASE = os.environ.get('SEEKDB_DATABASE', 'test')

# Server mode
SERVER_HOST = os.environ.get('SERVER_HOST', 'localhost')
SERVER_PORT = int(os.environ.get('SERVER_PORT', '2882'))
SERVER_DATABASE = os.environ.get('SERVER_DATABASE', 'test')
SERVER_USER = os.environ.get('SERVER_USER', 'root')
SERVER_PASSWORD = os.environ.get('SERVER_PASSWORD', '')

# OceanBase mode
OB_HOST = os.environ.get('OB_HOST', 'localhost')
OB_PORT = int(os.environ.get('OB_PORT', '2881'))
OB_TENANT = os.environ.get('OB_TENANT', 'test')
OB_DATABASE = os.environ.get('OB_DATABASE', 'test')
OB_USER = os.environ.get('OB_USER', 'root')
OB_PASSWORD = os.environ.get('OB_PASSWORD', '')


class TestClientCreation:
    """Test client creation, connection, and query execution for all three modes"""
    
    def test_create_embedded_client(self):
        """Test creating embedded client (lazy loading) and executing queries"""
        if not os.path.exists(SEEKDB_PATH):
            pytest.skip(f"SeekDB data directory does not exist: {SEEKDB_PATH}")
        
        # Create client (no immediate connection)
        client = seekdbclient.Client(
            path=SEEKDB_PATH,
            database=SEEKDB_DATABASE
        )
        
        # Verify client type and properties
        assert client is not None
        assert isinstance(client, seekdbclient.SeekdbEmbeddedClient)
        assert client.mode == "SeekdbEmbeddedClient"
        assert client.database == SEEKDB_DATABASE
        
        # Should not be connected at this point (lazy loading)
        assert not client.is_connected()
        
        # Execute query (first use, triggers connection)
        result = client.execute("SELECT 1")
        assert result is not None
        assert len(result) > 0
        
        # Should be connected now
        assert client.is_connected()
        
        print(f"\n✅ Embedded client created and connected successfully: path={SEEKDB_PATH}, database={SEEKDB_DATABASE}")
        print(f"   Query result: {result[0]}")
        
        # Automatic cleanup (via __del__)
    
    def test_create_server_client(self):
        """Test creating server client (lazy loading) and executing queries"""
        # Create client (no immediate connection)
        client = seekdbclient.Client(
            host=SERVER_HOST,
            port=SERVER_PORT,
            database=SERVER_DATABASE,
            user=SERVER_USER,
            password=SERVER_PASSWORD
        )
        
        # Verify client type and properties
        assert client is not None
        assert isinstance(client, seekdbclient.SeekdbServerClient)
        assert client.mode == "SeekdbServerClient"
        assert client.host == SERVER_HOST
        assert client.port == SERVER_PORT
        assert client.database == SERVER_DATABASE
        assert client.user == SERVER_USER
        
        # Should not be connected at this point (lazy loading)
        assert not client.is_connected()
        
        # Execute query (first use, triggers connection)
        try:
            result = client.execute("SELECT 1 as test")
            assert result is not None
            assert len(result) > 0
            assert result[0]['test'] == 1
            
            # Should be connected now
            assert client.is_connected()
            
            print(f"\n✅ Server client created and connected successfully: {SERVER_USER}@{SERVER_HOST}:{SERVER_PORT}/{SERVER_DATABASE}")
            print(f"   Query result: {result[0]}")
            
        except Exception as e:
            pytest.fail(f"Server connection failed ({SERVER_HOST}:{SERVER_PORT}): {e}\n"
                       f"Hint: Please ensure SeekDB Server is running")
        
        # Automatic cleanup (via __del__)
    
    def test_create_oceanbase_client(self):
        """Test creating OceanBase client (lazy loading) and executing queries"""
        # Create client (no immediate connection)
        client = seekdbclient.OBClient(
            host=OB_HOST,
            port=OB_PORT,
            tenant=OB_TENANT,
            database=OB_DATABASE,
            user=OB_USER,
            password=OB_PASSWORD
        )
        
        # Verify client type and properties
        assert client is not None
        assert isinstance(client, seekdbclient.OceanBaseServerClient)
        assert client.mode == "OceanBaseServerClient"
        assert client.host == OB_HOST
        assert client.port == OB_PORT
        assert client.tenant == OB_TENANT
        assert client.database == OB_DATABASE
        assert client.user == OB_USER
        assert client.full_user == f"{OB_USER}@{OB_TENANT}"
        
        # Should not be connected at this point (lazy loading)
        assert not client.is_connected()
        
        # Execute query (first use, triggers connection)
        try:
            result = client.execute("SELECT 1 as test")
            assert result is not None
            assert len(result) > 0
            assert result[0]['test'] == 1
            
            # Should be connected now
            assert client.is_connected()
            
            print(f"\n✅ OceanBase client created and connected successfully: {client.full_user}@{OB_HOST}:{OB_PORT}/{OB_DATABASE}")
            print(f"   Query result: {result[0]}")
            
        except Exception as e:
            pytest.fail(f"OceanBase connection failed ({OB_HOST}:{OB_PORT}): {e}\n"
                       f"Hint: Please ensure OceanBase is running and tenant '{OB_TENANT}' is created")
        
        # Automatic cleanup (via __del__)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SeekDBClient - Client Creation and Connection Tests")
    print("="*60)
    print(f"\nEnvironment Variable Configuration:")
    print(f"  Embedded mode: path={SEEKDB_PATH}, database={SEEKDB_DATABASE}")
    print(f"  Server mode: {SERVER_USER}@{SERVER_HOST}:{SERVER_PORT}/{SERVER_DATABASE}")
    print(f"  OceanBase mode: {OB_USER}@{OB_TENANT} -> {OB_HOST}:{OB_PORT}/{OB_DATABASE}")
    print("="*60 + "\n")
    
    pytest.main([__file__, "-v", "-s"])
