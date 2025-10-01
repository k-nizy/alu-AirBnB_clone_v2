# Storage Engines

Two storage backends are supported: JSON file storage and MySQL via SQLAlchemy.

## FileStorage
- Module: `models/engine/file_storage.py`
- Responsibilities: serialize/deserialize objects to `file.json`
- Key methods:
  - `all(cls=None) -> dict`
  - `new(obj)`
  - `save()`
  - `reload()`
  - `delete(obj=None)`
  - `close()`

Example
```python
from models.engine.file_storage import FileStorage
s = FileStorage(); s.reload()
print(list(s.all().keys()))
```

## DBStorage
- Module: `models/engine/db_storage.py`
- Responsibilities: persist objects to MySQL using SQLAlchemy sessions
- Env vars: `HBNB_MYSQL_USER`, `HBNB_MYSQL_PWD`, `HBNB_MYSQL_HOST`, `HBNB_MYSQL_DB`, `HBNB_ENV`
- Key methods:
  - `all(cls=None) -> dict`
  - `new(obj)`
  - `save()`
  - `reload()`
  - `delete(obj=None)`
  - `close()`

Switching backends

- Set `HBNB_TYPE_STORAGE=db` for DB; omit or set differently for file.
- Models adapt relationships/properties based on the backend.