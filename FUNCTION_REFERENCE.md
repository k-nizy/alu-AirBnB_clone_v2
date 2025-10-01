# AirBnB Clone - Function Reference Guide

## Table of Contents
1. [BaseModel Functions](#basemodel-functions)
2. [Storage Engine Functions](#storage-engine-functions)
3. [Console Functions](#console-functions)
4. [Web Framework Functions](#web-framework-functions)
5. [Utility Functions](#utility-functions)
6. [Deployment Functions](#deployment-functions)

## BaseModel Functions

### Core Methods

#### `__init__(self, *args, **kwargs)`
**Purpose:** Initialize a new BaseModel instance with optional attributes.

**Parameters:**
- `*args` (tuple): Positional arguments (unused)
- `**kwargs` (dict): Keyword arguments for object initialization
  - `id` (str, optional): Unique identifier
  - `created_at` (str, optional): ISO format datetime string
  - `updated_at` (str, optional): ISO format datetime string
  - Any other attribute name-value pairs

**Behavior:**
- If `kwargs` provided: Sets attributes from dictionary, converts datetime strings
- If no `kwargs`: Generates new UUID and sets current timestamp
- Automatically registers new objects with storage

**Example:**
```python
# Create empty instance
model = BaseModel()

# Create with attributes
model = BaseModel(name="Test", value=42)

# Create from dictionary (e.g., from JSON)
data = {
    "id": "12345",
    "created_at": "2023-01-01T12:00:00.000000",
    "name": "Restored Object"
}
model = BaseModel(**data)
```

#### `save(self)`
**Purpose:** Update the object's `updated_at` timestamp and persist to storage.

**Parameters:** None

**Returns:** None

**Side Effects:**
- Updates `self.updated_at` to current datetime
- Calls `storage.new(self)` to register object
- Calls `storage.save()` to persist changes

**Example:**
```python
model = BaseModel()
original_time = model.updated_at
time.sleep(1)
model.save()
assert model.updated_at > original_time
```

#### `to_dict(self)`
**Purpose:** Convert object to dictionary representation for serialization.

**Parameters:** None

**Returns:** `dict` containing:
- All instance attributes (excluding SQLAlchemy internal attributes)
- `__class__`: String name of the object's class
- `created_at`: ISO format datetime string
- `updated_at`: ISO format datetime string

**Example:**
```python
model = BaseModel()
model.name = "Test Model"
result = model.to_dict()

# Result structure:
{
    'id': '12345678-1234-1234-1234-123456789012',
    'created_at': '2023-01-01T12:00:00.000000',
    'updated_at': '2023-01-01T12:00:00.000000',
    '__class__': 'BaseModel',
    'name': 'Test Model'
}
```

#### `delete(self)`
**Purpose:** Remove the object from storage.

**Parameters:** None

**Returns:** None

**Side Effects:**
- Calls `storage.delete(self)` to remove from storage
- Object becomes inaccessible through storage queries

**Example:**
```python
model = BaseModel()
model.save()
model.delete()  # Object removed from storage
```

#### `__str__(self)`
**Purpose:** Provide human-readable string representation.

**Parameters:** None

**Returns:** `str` in format: `[ClassName] (id) {attributes_dict}`

**Example:**
```python
model = BaseModel()
print(model)
# Output: [BaseModel] (12345678-1234-1234-1234-123456789012) {'id': '...', 'created_at': datetime(...), ...}
```

## Storage Engine Functions

### FileStorage Functions

#### `all(self, cls=None)`
**Purpose:** Retrieve objects from storage, optionally filtered by class.

**Parameters:**
- `cls` (class, optional): Filter results to instances of this class

**Returns:** `dict` where:
- Keys: `"ClassName.object_id"`
- Values: Object instances

**Example:**
```python
from models import storage
from models.user import User

# Get all objects
all_objects = storage.all()

# Get only User objects
users = storage.all(User)
# or
users = storage.all("User")
```

#### `new(self, obj)`
**Purpose:** Add object to the storage dictionary (in memory).

**Parameters:**
- `obj`: Object instance to add

**Returns:** None

**Side Effects:**
- Adds object to `__objects` dictionary with key `"ClassName.id"`

**Example:**
```python
user = User()
storage.new(user)  # Object added to memory storage
```

#### `save(self)`
**Purpose:** Serialize all objects to JSON file.

**Parameters:** None

**Returns:** None

**Side Effects:**
- Writes all objects in `__objects` to `file.json`
- Converts objects to dictionaries using `to_dict()`

**File Format:**
```json
{
    "User.12345": {
        "id": "12345",
        "__class__": "User",
        "created_at": "2023-01-01T12:00:00.000000",
        "email": "user@example.com"
    }
}
```

#### `reload(self)`
**Purpose:** Load objects from JSON file into memory.

**Parameters:** None

**Returns:** None

**Side Effects:**
- Reads `file.json` and recreates objects
- Populates `__objects` dictionary
- Handles missing file gracefully

**Example:**
```python
storage.reload()  # Objects loaded from file.json
```

#### `delete(self, obj=None)`
**Purpose:** Remove object from storage and save changes.

**Parameters:**
- `obj`: Object to remove (if None, no action taken)

**Returns:** None

**Side Effects:**
- Removes object from `__objects` dictionary
- Calls `save()` to persist changes

### DBStorage Functions

#### `__init__(self)`
**Purpose:** Initialize database connection and engine.

**Parameters:** None

**Environment Variables Required:**
- `HBNB_MYSQL_USER`: Database username
- `HBNB_MYSQL_PWD`: Database password
- `HBNB_MYSQL_HOST`: Database host
- `HBNB_MYSQL_DB`: Database name

**Side Effects:**
- Creates SQLAlchemy engine
- Drops all tables if `HBNB_ENV=test`

#### `all(self, cls=None)`
**Purpose:** Query database for objects.

**Parameters:**
- `cls` (str/class, optional): Class name or class object to filter by

**Returns:** `dict` with same format as FileStorage

**Example:**
```python
# Get all users from database
users = storage.all("User")

# Get all objects
all_objects = storage.all()
```

#### `new(self, obj)`
**Purpose:** Add object to current database session.

**Parameters:**
- `obj`: Object to add

**Returns:** None

**Side Effects:**
- Calls `session.add(obj)`

#### `save(self)`
**Purpose:** Commit current database session.

**Parameters:** None

**Returns:** None

**Side Effects:**
- Calls `session.commit()`

#### `reload(self)`
**Purpose:** Create database tables and session.

**Parameters:** None

**Returns:** None

**Side Effects:**
- Creates all tables using SQLAlchemy metadata
- Initializes scoped session

#### `delete(self, obj=None)`
**Purpose:** Delete object from database.

**Parameters:**
- `obj`: Object to delete

**Returns:** None

**Side Effects:**
- Calls `session.delete(obj)`
- Commits transaction

#### `close(self)`
**Purpose:** Close database session.

**Parameters:** None

**Returns:** None

**Side Effects:**
- Closes current session

## Console Functions

### HBNBCommand Methods

#### `do_create(self, line)`
**Purpose:** Create new instance of specified class.

**Parameters:**
- `line` (str): Command line arguments in format: `ClassName [param1=value1 param2=value2 ...]`

**Parameter Parsing:**
- String values: `name="My_Place"` (underscores become spaces)
- Integer values: `number_rooms=4`
- Float values: `latitude=37.7749`

**Returns:** Prints object ID or error message

**Example:**
```bash
create User email="test@example.com" first_name="John"
create Place name="Cozy_Apartment" price_by_night=100 latitude=37.7749
```

#### `do_show(self, line)`
**Purpose:** Display object by class name and ID.

**Parameters:**
- `line` (str): `"ClassName object_id"`

**Returns:** Prints object string representation or error

**Example:**
```bash
show User 12345678-1234-1234-1234-123456789012
```

#### `do_all(self, line)`
**Purpose:** Display all objects or all objects of a class.

**Parameters:**
- `line` (str): Optional class name

**Returns:** Prints list of object string representations

**Example:**
```bash
all
all User
```

#### `do_update(self, line)`
**Purpose:** Update object attribute.

**Parameters:**
- `line` (str): `"ClassName object_id attribute_name attribute_value"`

**Attribute Type Handling:**
- Automatically converts strings to appropriate types
- Handles quoted strings with spaces

**Example:**
```bash
update User 12345 first_name "John Doe"
update User 12345 age 25
```

#### `do_destroy(self, line)`
**Purpose:** Delete object from storage.

**Parameters:**
- `line` (str): `"ClassName object_id"`

**Returns:** None (silent success) or error message

**Example:**
```bash
destroy User 12345678-1234-1234-1234-123456789012
```

#### `do_count(self, line)`
**Purpose:** Count objects of specified class.

**Parameters:**
- `line` (str): Class name

**Returns:** Prints count of objects

**Example:**
```bash
count User
# Output: 5
```

#### `default(self, line)`
**Purpose:** Handle alternative command syntax.

**Supported Syntax:**
- `ClassName.all()`
- `ClassName.count()`
- `ClassName.show("id")`
- `ClassName.destroy("id")`
- `ClassName.update("id", "attr", "value")`
- `ClassName.update("id", {"attr1": "value1", "attr2": "value2"})`

**Example:**
```bash
User.all()
User.count()
User.show("12345")
User.update("12345", "name", "John")
User.update("12345", {"name": "John", "age": 25})
```

## Web Framework Functions

### Route Handler Functions

#### `hello_hbnb()`
**Purpose:** Simple greeting endpoint.

**Route:** `GET /`

**Parameters:** None

**Returns:** `str` - "Hello HBNB!"

**Example:**
```python
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'
```

#### `states_list()`
**Purpose:** Display all states in HTML template.

**Route:** `GET /states_list`

**Parameters:** None

**Returns:** Rendered HTML template with states data

**Template Variables:**
- `all_states`: List of State objects

**Example:**
```python
@app.route('/states_list', strict_slashes=False)
def states_list():
    all_states = storage.all("State").values()
    return render_template('7-states_list.html', all_states=all_states)
```

#### `cities_by_states()`
**Purpose:** Display states with their cities.

**Route:** `GET /cities_by_states`

**Parameters:** None

**Returns:** Rendered HTML with states and cities

**Template Variables:**
- `all_states`: List of State objects (with cities relationship)

#### `hbnb_filters()`
**Purpose:** Display filtering interface for places.

**Route:** `GET /hbnb_filters`

**Parameters:** None

**Returns:** Rendered HTML with filter options

**Template Variables:**
- `states`: List of State objects
- `amenities`: List of Amenity objects

#### `teardown(exception)`
**Purpose:** Clean up storage session after request.

**Decorator:** `@app.teardown_appcontext`

**Parameters:**
- `exception`: Exception that occurred (if any)

**Returns:** None

**Side Effects:**
- Calls `storage.close()` to close database session

**Example:**
```python
@app.teardown_appcontext
def teardown(exception):
    storage.close()
```

### Template Functions

Templates use Jinja2 syntax with custom filters:

#### State/City Sorting
```html
{% for state in all_states|sort(attribute='name') %}
    <li>{{ state.id }}: <b>{{ state.name }}</b>
        <ul>
        {% for city in state.cities|sort(attribute='name') %}
            <li>{{ city.id }}: <b>{{ city.name }}</b></li>
        {% endfor %}
        </ul>
    </li>
{% endfor %}
```

## Utility Functions

### Parameter Parsing (Console)

#### `parse_line(line)`
**Purpose:** Parse command line arguments into components.

**Parameters:**
- `line` (str): Raw command line input

**Returns:** `list` of parsed arguments

**Handles:**
- Quoted strings with spaces
- Key=value parameter pairs
- Type conversion for values

### String Processing

#### `process_string_value(value)`
**Purpose:** Convert parameter string to appropriate Python value.

**Parameters:**
- `value` (str): String representation of value

**Returns:** Converted value (str, int, float)

**Rules:**
- Quoted strings: Remove quotes, replace underscores with spaces
- Numeric strings: Convert to int or float
- Other: Return as string

**Example:**
```python
process_string_value('"My_Place"')  # Returns: "My Place"
process_string_value('42')          # Returns: 42
process_string_value('3.14')        # Returns: 3.14
```

## Deployment Functions

### Fabric Functions

#### `do_pack()`
**Purpose:** Create compressed archive of web_static directory.

**Parameters:** None

**Returns:** `str` - Archive path on success, `None` on failure

**Process:**
1. Generate timestamp-based filename
2. Create `versions` directory
3. Create tar.gz archive
4. Return archive path

**Example:**
```python
def do_pack():
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"web_static_{datetime_str}.tgz"
    try:
        local('mkdir -p versions')
        local(f'tar -cvzf versions/{file_name} web_static')
        return f"versions/{file_name}"
    except:
        return None
```

#### `do_deploy(archive_path)`
**Purpose:** Deploy archive to remote servers.

**Parameters:**
- `archive_path` (str): Path to archive file

**Returns:** `bool` - True on success, False on failure

**Process:**
1. Upload archive to `/tmp/`
2. Extract to `/data/web_static/releases/`
3. Update symbolic link
4. Clean up temporary files

**Example:**
```python
def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        # ... deployment steps ...
        return True
    except:
        return False
```

#### `deploy()`
**Purpose:** Complete deployment pipeline.

**Parameters:** None

**Returns:** `bool` - Success status

**Process:**
1. Call `do_pack()` to create archive
2. Call `do_deploy()` with archive path
3. Return combined success status

**Example:**
```python
def deploy():
    try:
        archive_path = do_pack()
        if archive_path:
            return do_deploy(archive_path)
        return False
    except:
        return False
```

### Server Management

#### `setup_web_static()`
**Purpose:** Configure web server for static file serving.

**Process:**
1. Create directory structure
2. Configure Nginx
3. Set permissions
4. Restart services

**Directory Structure:**
```
/data/
├── web_static/
│   ├── releases/
│   │   └── web_static_YYYYMMDDHHMMSS/
│   ├── shared/
│   └── current -> releases/web_static_YYYYMMDDHHMMSS/
```

---

## Function Categories Summary

### Core Model Functions
- Object lifecycle: `__init__`, `save`, `delete`
- Serialization: `to_dict`, `__str__`
- Storage integration: automatic registration

### Storage Functions
- CRUD operations: `all`, `new`, `save`, `delete`
- Session management: `reload`, `close`
- Backend abstraction: same interface for file/database

### Console Functions
- Object management: `create`, `show`, `update`, `destroy`
- Querying: `all`, `count`
- Alternative syntax: method-style commands

### Web Functions
- Route handlers: request processing and response generation
- Template rendering: data preparation for views
- Session cleanup: resource management

### Deployment Functions
- Archive creation: packaging static files
- Remote deployment: server configuration and file transfer
- Pipeline automation: end-to-end deployment process

Each function is designed with specific responsibilities and clear interfaces, enabling modular development and easy testing.