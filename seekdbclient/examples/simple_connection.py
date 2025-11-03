"""
Simple connection examples - automatic connection management
"""
import sys
from pathlib import Path

# Add project path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import seekdbclient


def test_embedded():
    """Test embedded mode connection"""
    print("=" * 60)
    print("1. Embedded Mode")
    print("=" * 60)
    
    try:
        # Create client (no need to explicitly call connect)
        client = seekdbclient.Client(
            path="./seekdb",
            database="test"
        )
        
        print(f"✅ Client created successfully")
        print(f"   Type: {type(client).__name__}")
        print(f"   Mode: {client.mode}")
        
        # Execute query directly (auto connect)
        result = client.execute("SELECT OB_VERSION()")
        version = result[0][0]
        print(f"✅ Query successful (auto connected)")
        print(f"   OceanBase version: {version}")
        print(f"   Connection status: {client.is_connected()}")
        
        # Manual close (optional)
        client.close()
        print(f"✅ Connection closed")
        print(f"   Connection status: {client.is_connected()}")
        
    except Exception as e:
        print(f"❌ Failed: {e}")


def test_server():
    """Test server mode connection"""
    print("\n" + "=" * 60)
    print("2. Server Mode")
    print("=" * 60)
    
    try:
        client = seekdbclient.Client(
            host='localhost',
            port=2882,
            database="test",
            user="root",
            password=""
        )
        
        print(f"✅ Client created successfully")
        print(f"   Type: {type(client).__name__}")
        print(f"   Mode: {client.mode}")
        
        # Execute query directly (auto connect)
        result = client.execute("SELECT 1 as test")
        print(f"✅ Query successful (auto connected)")
        print(f"   Query result: {result}")
        print(f"   Connection status: {client.is_connected()}")
        
        client.close()
        print(f"✅ Connection closed")
        
    except Exception as e:
        print(f"❌ Failed: {e}")


def test_oceanbase():
    """Test OceanBase mode connection"""
    print("\n" + "=" * 60)
    print("3. OceanBase Mode")
    print("=" * 60)
    
    try:
        client = seekdbclient.OBClient(
            host='localhost',
            port=2881,
            tenant="test",
            database="test",
            user="root",
            password=""
        )
        
        print(f"✅ Client created successfully")
        print(f"   Type: {type(client).__name__}")
        print(f"   Mode: {client.mode}")
        print(f"   Full username: {client.full_user}")
        
        # Execute query directly (auto connect)
        result = client.execute("SELECT 1 as test")
        print(f"✅ Query successful (auto connected)")
        
        client.close()
        print(f"✅ Connection closed")
        
    except Exception as e:
        print(f"❌ Failed: {e}")


def test_context_manager():
    """Test context manager (recommended method)"""
    print("\n" + "=" * 60)
    print("4. Context Manager (Recommended)")
    print("=" * 60)
    
    print("\n✨ Using with statement for fully automatic connection management:")
    print("\nExample code:")
    print("```python")
    print("with seekdbclient.Client(path='./seekdb', database='test') as client:")
    print("    result = client.execute('SELECT 1')  # Auto connect")
    print("    print(result)")
    print("# Auto close connection on exit")
    print("```")
    
    try:
        with seekdbclient.Client(path="./seekdb", database="test") as client:
            result = client.execute("SELECT 'Hello from SeekDBClient!' as message")
            print(f"\n✅ Execution result: {result[0][0]}")
        print(f"✅ Connection automatically closed (exited with statement)")
    except Exception as e:
        print(f"❌ Failed: {e}")


if __name__ == "__main__":
    print("\n" + "🎯 " * 20)
    print("SeekDBClient - Automatic Connection Management Demo")
    print("🎯 " * 20)
    print("\n💡 Features: No need to explicitly call connect() and close()")
    print("   - Auto connect on first use (lazy connection)")
    print("   - Auto close using context manager")
    print("   - Can also manually call close() (optional)\n")
    
    # Run all tests
    test_embedded()
    test_server()
    test_oceanbase()
    test_context_manager()
    
    print("\n" + "=" * 60)
    print("  Usage Recommendations")
    print("=" * 60)
    print("\nRecommended (using context manager):")
    print("```python")
    print("with seekdbclient.Client(path='./seekdb') as client:")
    print("    result = client.execute('SELECT 1')")
    print("```")
    print("\nSimple way (auto connect):")
    print("```python")
    print("client = seekdbclient.Client(path='./seekdb')")
    print("result = client.execute('SELECT 1')  # Auto connect")
    print("# No need to manually close(), but using with statement is recommended")
    print("```")
    print("\n" + "=" * 60 + "\n")
