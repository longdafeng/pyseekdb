"""
API framework test - verify all clients implement connection interface
"""
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import seekdbclient
from seekdbclient.client.client_base import BaseClient


class TestAPIFramework:
    """Test API framework completeness"""
    
    def test_all_clients_are_base_client_subclass(self):
        """Test all clients are subclasses of BaseClient"""
        assert issubclass(seekdbclient.SeekdbEmbeddedClient, BaseClient)
        assert issubclass(seekdbclient.SeekdbServerClient, BaseClient)
        assert issubclass(seekdbclient.OceanBaseServerClient, BaseClient)
        print("✅ All clients inherit from BaseClient")
    
    def test_connection_methods(self):
        """Test if connection management methods exist"""
        required_methods = [
            'is_connected',
            'execute',
            'get_raw_connection',
            'mode',
            '_cleanup'  # internal cleanup method
        ]
        
        for ClientClass in [
            seekdbclient.SeekdbEmbeddedClient,
            seekdbclient.SeekdbServerClient,
            seekdbclient.OceanBaseServerClient
        ]:
            for method in required_methods:
                assert hasattr(ClientClass, method), \
                    f"{ClientClass.__name__} missing method: {method}"
            
            print(f"✅ {ClientClass.__name__}: All connection methods defined")
    
    def test_collection_management_methods(self):
        """Test if Collection management methods exist"""
        required_methods = [
            'create_collection',
            'get_collection',
            'delete_collection',
            'list_collections',
            'has_collection'
        ]
        
        for ClientClass in [
            seekdbclient.SeekdbEmbeddedClient,
            seekdbclient.SeekdbServerClient,
            seekdbclient.OceanBaseServerClient
        ]:
            for method in required_methods:
                assert hasattr(ClientClass, method), \
                    f"{ClientClass.__name__} missing method: {method}"
            
            print(f"✅ {ClientClass.__name__}: Collection management methods defined")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
