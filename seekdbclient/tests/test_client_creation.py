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

# Server mode (SeekDB Server)
SERVER_HOST = os.environ.get('SERVER_HOST', '127.0.0.1')
SERVER_PORT = int(os.environ.get('SERVER_PORT', '2881'))  # SeekDB Server port
SERVER_DATABASE = os.environ.get('SERVER_DATABASE', 'test')
SERVER_USER = os.environ.get('SERVER_USER', 'root')
SERVER_PASSWORD = os.environ.get('SERVER_PASSWORD', '')

# OceanBase mode
OB_HOST = os.environ.get('OB_HOST', '127.0.0.1')
OB_PORT = int(os.environ.get('OB_PORT', '11402'))
OB_TENANT = os.environ.get('OB_TENANT', 'mysql')
OB_DATABASE = os.environ.get('OB_DATABASE', 'test')
OB_USER = os.environ.get('OB_USER', 'root')
OB_PASSWORD = os.environ.get('OB_PASSWORD', '')


class TestClientCreation:
    """Test client creation, connection, and query execution for all three modes"""
    
    def test_create_embedded_client(self):
        """Test creating embedded client (lazy loading) and executing queries"""
        if not os.path.exists(SEEKDB_PATH):
            pytest.fail(
                f"❌ SeekDB data directory does not exist: {SEEKDB_PATH}\n\n"
                f"Solution:\n"
                f"  1. Create the directory: mkdir -p {SEEKDB_PATH}\n"
                f"  2. Or set SEEKDB_PATH environment variable to an existing directory:\n"
                f"     export SEEKDB_PATH=/path/to/your/seekdb/data\n"
                f"     python3 -m pytest seekdbclient/tests/test_client_creation.py -v -s"
            )
        
        # Check if seekdb package is available and properly configured
        try:
            import sys
            project_root = "/home/lyl512932/pythonSDK/pyobvector"
            if project_root in sys.path:
                sys.path.remove(project_root)
            import seekdb
            if not hasattr(seekdb, 'open') and not hasattr(seekdb, '_initialize_module'):
                pytest.fail(
                    "❌ SeekDB embedded package is not properly installed!\n"
                    "The 'seekdb' module exists but lacks required methods.\n"
                    "Required: 'open' method or '_initialize_module' method\n\n"
                    "Solution: Please install the seekdb embedded package from correct source:\n"
                    "  pip install seekdb\n"
                    "Or contact the seekdb package maintainer for installation guide."
                )
        except ImportError:
            pytest.fail(
                "❌ SeekDB embedded package is not installed!\n"
                "The 'seekdb' module cannot be imported.\n\n"
                "Solution: Please install the seekdb embedded package:\n"
                "  pip install seekdb\n"
                "Or contact the seekdb package maintainer for installation guide."
            )
        finally:
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
        
        # Create client (returns _ClientProxy)
        client = seekdbclient.Client(
            path=SEEKDB_PATH,
            database=SEEKDB_DATABASE
        )
        
        # Verify client type and properties
        assert client is not None
        # Client now returns a proxy
        assert hasattr(client, '_server')
        assert isinstance(client._server, seekdbclient.SeekdbEmbeddedClient)
        assert client._server.mode == "SeekdbEmbeddedClient"
        assert client._server.database == SEEKDB_DATABASE
        
        # Should not be connected at this point (lazy loading)
        assert not client._server.is_connected()
        
        # Execute query through proxy (first use, triggers connection)
        result = client._server.execute("SELECT 1")
        assert result is not None
        assert len(result) > 0
        
        # Should be connected now
        assert client._server.is_connected()
        
        print(f"\n✅ Embedded client created and connected successfully: path={SEEKDB_PATH}, database={SEEKDB_DATABASE}")
        print(f"   Query result: {result[0]}")
        
        # Automatic cleanup (via __del__)
    
    def test_create_server_client(self):
        """Test creating server client (lazy loading) and executing queries"""
        # Create client (returns _ClientProxy)
        client = seekdbclient.Client(
            host=SERVER_HOST,
            port=SERVER_PORT,
            database=SERVER_DATABASE,
            user=SERVER_USER,
            password=SERVER_PASSWORD
        )
        
        # Verify client type and properties
        assert client is not None
        assert hasattr(client, '_server')
        assert isinstance(client._server, seekdbclient.SeekdbServerClient)
        assert client._server.mode == "SeekdbServerClient"
        assert client._server.host == SERVER_HOST
        assert client._server.port == SERVER_PORT
        assert client._server.database == SERVER_DATABASE
        assert client._server.user == SERVER_USER
        
        # Should not be connected at this point (lazy loading)
        assert not client._server.is_connected()
        
        # Execute query through proxy (first use, triggers connection)
        try:
            result = client._server.execute("SELECT 1 as test")
            assert result is not None
            assert len(result) > 0
            assert result[0]['test'] == 1
            
            # Should be connected now
            assert client._server.is_connected()
            
            print(f"\n✅ Server client created and connected successfully: {SERVER_USER}@{SERVER_HOST}:{SERVER_PORT}/{SERVER_DATABASE}")
            print(f"   Query result: {result[0]}")
            
        except Exception as e:
            pytest.fail(f"Server connection failed ({SERVER_HOST}:{SERVER_PORT}): {e}\n"
                       f"Hint: Please ensure SeekDB Server is running on port {SERVER_PORT}")
        
        # Automatic cleanup (via __del__)
    
    def test_create_oceanbase_client(self):
        """Test creating OceanBase client (lazy loading) and executing queries"""
        # Create client (returns _ClientProxy)
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
        assert hasattr(client, '_server')
        assert isinstance(client._server, seekdbclient.OceanBaseServerClient)
        assert client._server.mode == "OceanBaseServerClient"
        assert client._server.host == OB_HOST
        assert client._server.port == OB_PORT
        assert client._server.tenant == OB_TENANT
        assert client._server.database == OB_DATABASE
        assert client._server.user == OB_USER
        assert client._server.full_user == f"{OB_USER}@{OB_TENANT}"
        
        # Should not be connected at this point (lazy loading)
        assert not client._server.is_connected()
        
        # Execute query through proxy (first use, triggers connection)
        try:
            result = client._server.execute("SELECT 1 as test")
            assert result is not None
            assert len(result) > 0
            assert result[0]['test'] == 1
            
            # Should be connected now
            assert client._server.is_connected()
            
            print(f"\n✅ OceanBase client created and connected successfully: {client._server.full_user}@{OB_HOST}:{OB_PORT}/{OB_DATABASE}")
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
