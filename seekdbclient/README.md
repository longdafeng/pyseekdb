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

### Collection Framework (Roadmap)
TODO

## Project Layout
```
seekdbclient/
├── __init__.py                     # Library entry point
├── client/
│   ├── __init__.py                 # Factory and exports
│   ├── client_base.py              # BaseClient interface (lazy connection + cleanup)
│   ├── client_seekdb_embedded.py   # Embedded SeekDB implementation
│   ├── client_seekdb_server.py     # Remote SeekDB implementation (pymysql)
│   ├── client_oceanbase_server.py  # OceanBase implementation (pymysql)
│   └── collection.py               # Collection interface definitions
├── examples/
│   └── simple_connection.py        # End-to-end usage example
├── tests/
│   ├── test_api_framework.py       # Verifies API surface
│   └── test_client_creation.py     # Exercises real connection flow
└── test_oceanbase_connection.py    # Manual OceanBase connectivity script
```

## Testing
```bash
# Run all tests
poetry run pytest seekdbclient/tests/ -v

# Exercise only the API surface checks
poetry run pytest seekdbclient/tests/test_api_framework.py -v

# Optional: run the live OceanBase check (requires running server)
poetry run python test_oceanbase_connection.py
```

### Environment Variables (Optional)
`test_client_creation.py` honors the following overrides:
```bash
export SEEKDB_PATH=/data/seekdb
export SEEKDB_DATABASE=demo
export SERVER_HOST=127.0.0.1
export SERVER_PORT=2882
export SERVER_USER=root
export SERVER_PASSWORD=secret
export OB_HOST=127.0.0.1
export OB_PORT=11402
export OB_TENANT=mysql
export OB_USER=root
export OB_PASSWORD=secret
```

## Status
| Component                 | State       | Notes                              |
|---------------------------|------------|------------------------------------|
| Client instantiation      | ✅ Complete | All three connection modes         |
| Connection management     | ✅ Complete | Lazy connect + automatic cleanup   |
| SQL execution             | ✅ Complete | Uses seekdb / pymysql cursors      |
| Collection interfaces     | 🚧 Planned  | Signatures only, no logic yet      |
| Vector/query operations   | 🚧 Planned  | To be implemented per backend      |

## License
MIT License
