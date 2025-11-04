# SeekDBClient

SeekDBClient is a unified Python client that wraps three database connection modes—embedded SeekDB, remote SeekDB servers, and OceanBase—behind a single, concise API. 

## Installation
```bash
cd .../pyobvector
poetry install
```

## Quick Start
### Embedded SeekDB
```python
import seekdbclient

client = seekdbclient.Client(path="./seekdb", database="demo")
rows = client.execute("SELECT 1")
print(rows)
```

### Remote SeekDB Server
```python
import seekdbclient

with seekdbclient.Client(
    host="127.0.0.1",
    port=2882,
    database="demo",
    user="root",
    password=""
) as client:
    print(client.execute("SHOW TABLES"))
```

### OceanBase
```python
import seekdbclient

with seekdbclient.OBClient(
    host="127.0.0.1",
    port=11402,
    tenant="mysql",
    database="test",
    user="root",
    password=""
) as client:
    version = client.execute("SELECT version() AS v")
    print(version[0]["v"])
```

## API Overview
### Factory Functions
```python
seekdbclient.Client(path="/data/seekdb", database="demo")        # SeekdbEmbeddedClient
seekdbclient.Client(host="localhost", port=2882, database="demo") # SeekdbServerClient
seekdbclient.OBClient(host="localhost", tenant="mysql")           # OceanBaseServerClient
```

### Client Methods
| Method / Property     | Description                                                    |
|-----------------------|----------------------------------------------------------------|
| `execute(sql)`        | Run SQL and return cursor results (commits automatically when needed). |
| `is_connected()`      | Check whether an underlying connection is active.             |
| `get_raw_connection()`| Access the underlying seekdb / pymysql connection.            |
| `mode`                | Returns the concrete client class name (`SeekdbEmbeddedClient`, `SeekdbServerClient`, or `OceanBaseServerClient`). |
| `_ensure_connection()`| Internal lazy connector (not part of public API).             |
| `_cleanup()`          | Internal cleanup hook; called by `__exit__` / `__del__`.       |

### AdminClient for Database Management
```python
import seekdbclient

# Server mode - Database management
admin = seekdbclient.AdminClient(host="127.0.0.1", port=2881, user="root")
admin.create_database("my_database")
databases = admin.list_databases()
admin.delete_database("my_database")

# OceanBase mode - Database management (multi-tenant)
admin = seekdbclient.OBAdminClient(host="127.0.0.1", port=11402, tenant="mysql")
admin.create_database("analytics")
databases = admin.list_databases()  # Scoped to tenant
```

**AdminClient Methods:**
| Method                    | Description                                        |
|---------------------------|----------------------------------------------------|
| `create_database(name)`   | Create a new database                              |
| `get_database(name)`      | Get database object with metadata                  |
| `delete_database(name)`   | Delete a database                                  |
| `list_databases(limit, offset)` | List all databases                          |

**Note:** 
- Embedded/Server mode: No tenant concept (tenant=None in Database objects)
- OceanBase mode: Multi-tenant architecture (tenant is set in Database objects)


## Testing
```bash
python3 -m pytest seekdbclient/tests/ -v

python3 -m pytest seekdbclient/tests/ -v -s # print log

python3 -m pytest seekdbclient/tests/test_client_creation.py::TestClientCreation::test_create_server_client -v

python3 -m pytest seekdbclient/tests/test_client_creation.py -v

```

### Environment Variables (Optional)
`test_client_creation.py` honors the following overrides:
```bash
export SEEKDB_PATH=/data/seekdb
export SEEKDB_DATABASE=demo
export SERVER_HOST=127.0.0.1
export SERVER_PORT=2881           # SeekDB Server port
export SERVER_USER=root
export SERVER_PASSWORD=secret
export OB_HOST=127.0.0.1
export OB_PORT=11402               # OceanBase port (from 'ob do mysql -n ob1')
export OB_TENANT=mysql             # OceanBase tenant
export OB_USER=root
export OB_PASSWORD=
```

## Architecture
Following chromadb's design pattern:
- **ClientAPI**: Collection operations interface
- **AdminAPI**: Database operations interface
- **ServerAPI (BaseClient)**: Implements both interfaces
- **_ClientProxy**: Exposes only collection operations
- **_AdminClientProxy**: Exposes only database operations

```
Client() → _ClientProxy → BaseClient (ServerAPI)
AdminClient() → _AdminClientProxy → BaseClient (ServerAPI)
```

## License
MIT License
