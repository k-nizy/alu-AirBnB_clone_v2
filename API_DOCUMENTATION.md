# AirBnB Clone - Comprehensive API Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Core Models](#core-models)
3. [Storage Engines](#storage-engines)
4. [Console Interface](#console-interface)
5. [Web Framework](#web-framework)
6. [Deployment Scripts](#deployment-scripts)
7. [Usage Examples](#usage-examples)
8. [API Reference](#api-reference)

## Project Overview

The AirBnB Clone is a full-stack web application that replicates core functionality of AirBnB. It consists of:

- **Data Models**: Object-oriented models for users, places, states, cities, amenities, and reviews
- **Storage Engines**: File-based and MySQL database storage systems
- **Command Interpreter**: Interactive console for managing objects
- **Web Interface**: Flask-based web application with templating
- **Deployment Tools**: Fabric scripts for automated deployment

### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │     Console     │    │  Storage Engine │
│    (Flask)      │◄──►│  (cmd.Cmd)      │◄──►│ (File/Database) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │   Data Models   │
                    │ (BaseModel etc) │
                    └─────────────────┘
```

## Core Models

### BaseModel

The foundation class for all other models, providing common attributes and methods.

#### Attributes
- `id` (str): Unique identifier (UUID4)
- `created_at` (datetime): Object creation timestamp
- `updated_at` (datetime): Last modification timestamp

#### Methods

##### `__init__(self, *args, **kwargs)`
Initialize a new BaseModel instance.

**Parameters:**
- `*args`: Unused positional arguments
- `**kwargs`: Keyword arguments for object initialization

**Example:**
```python
from models.base_model import BaseModel

# Create new instance
model = BaseModel()
print(model.id)  # e.g., "12345678-1234-1234-1234-123456789012"

# Create from dictionary
data = {"id": "test-id", "created_at": "2023-01-01T00:00:00.000000"}
model = BaseModel(**data)
```

##### `save(self)`
Update the `updated_at` timestamp and save to storage.

**Example:**
```python
model = BaseModel()
original_time = model.updated_at
model.save()
print(model.updated_at > original_time)  # True
```

##### `to_dict(self)`
Convert the object to a dictionary representation.

**Returns:** Dictionary with all object attributes and metadata

**Example:**
```python
model = BaseModel()
model_dict = model.to_dict()
print(model_dict.keys())  # ['id', 'created_at', 'updated_at', '__class__']
```

##### `delete(self)`
Remove the object from storage.

**Example:**
```python
model = BaseModel()
model.delete()  # Object removed from storage
```

### User

Represents a user in the system.

#### Attributes
- Inherits from `BaseModel`
- `email` (str): User's email address (required)
- `password` (str): User's password (required)
- `first_name` (str): User's first name (optional)
- `last_name` (str): User's last name (optional)

#### Relationships
- `places`: One-to-many relationship with Place objects
- `reviews`: One-to-many relationship with Review objects

#### Example Usage
```python
from models.user import User

# Create a new user
user = User()
user.email = "john@example.com"
user.password = "secure123"
user.first_name = "John"
user.last_name = "Doe"
user.save()

# Access user's places
for place in user.places:
    print(f"Place: {place.name}")
```

### State

Represents a geographical state.

#### Attributes
- Inherits from `BaseModel`
- `name` (str): State name (required)

#### Relationships
- `cities`: One-to-many relationship with City objects

#### Example Usage
```python
from models.state import State

# Create a new state
state = State()
state.name = "California"
state.save()

# Access state's cities
for city in state.cities:
    print(f"City: {city.name}")
```

### City

Represents a city within a state.

#### Attributes
- Inherits from `BaseModel`
- `name` (str): City name (required)
- `state_id` (str): Foreign key to State (required)

#### Relationships
- `state`: Many-to-one relationship with State
- `places`: One-to-many relationship with Place objects

#### Example Usage
```python
from models.city import City
from models.state import State

# Create a city
state = State(name="California")
state.save()

city = City()
city.name = "San Francisco"
city.state_id = state.id
city.save()
```

### Place

Represents a rental property.

#### Attributes
- Inherits from `BaseModel`
- `city_id` (str): Foreign key to City (required)
- `user_id` (str): Foreign key to User (required)
- `name` (str): Place name (required)
- `description` (str): Place description (optional)
- `number_rooms` (int): Number of rooms (default: 0)
- `number_bathrooms` (int): Number of bathrooms (default: 0)
- `max_guest` (int): Maximum guests (default: 0)
- `price_by_night` (int): Price per night (default: 0)
- `latitude` (float): Latitude coordinate (optional)
- `longitude` (float): Longitude coordinate (optional)

#### Relationships
- `user`: Many-to-one relationship with User
- `city`: Many-to-one relationship with City
- `reviews`: One-to-many relationship with Review objects
- `amenities`: Many-to-many relationship with Amenity objects

#### Example Usage
```python
from models.place import Place

place = Place()
place.name = "Cozy Apartment"
place.description = "A beautiful apartment in downtown"
place.city_id = city.id
place.user_id = user.id
place.number_rooms = 2
place.number_bathrooms = 1
place.max_guest = 4
place.price_by_night = 100
place.save()
```

### Amenity

Represents an amenity that can be associated with places.

#### Attributes
- Inherits from `BaseModel`
- `name` (str): Amenity name (required)

#### Relationships
- `place_amenities`: Many-to-many relationship with Place objects

#### Example Usage
```python
from models.amenity import Amenity

amenity = Amenity()
amenity.name = "WiFi"
amenity.save()

# Associate with a place
place.amenities.append(amenity)
place.save()
```

### Review

Represents a review for a place.

#### Attributes
- Inherits from `BaseModel`
- `place_id` (str): Foreign key to Place (required)
- `user_id` (str): Foreign key to User (required)
- `text` (str): Review text (required)

#### Relationships
- `place`: Many-to-one relationship with Place
- `user`: Many-to-one relationship with User

#### Example Usage
```python
from models.review import Review

review = Review()
review.place_id = place.id
review.user_id = user.id
review.text = "Great place to stay! Highly recommended."
review.save()
```

## Storage Engines

The application supports two storage backends: file-based storage and MySQL database storage.

### FileStorage

JSON file-based storage system.

#### Configuration
Set environment variable: `HBNB_TYPE_STORAGE=file` (default)

#### Methods

##### `all(self, cls=None)`
Retrieve all objects or objects of a specific class.

**Parameters:**
- `cls` (class, optional): Filter by class type

**Returns:** Dictionary of objects

**Example:**
```python
from models import storage

# Get all objects
all_objects = storage.all()

# Get only User objects
users = storage.all(User)
```

##### `new(self, obj)`
Add a new object to storage.

**Parameters:**
- `obj`: Object to add

**Example:**
```python
user = User()
storage.new(user)  # Object added to storage
```

##### `save(self)`
Persist all objects to the JSON file.

**Example:**
```python
storage.save()  # All objects written to file.json
```

##### `reload(self)`
Load objects from the JSON file.

**Example:**
```python
storage.reload()  # Objects loaded from file.json
```

##### `delete(self, obj=None)`
Remove an object from storage.

**Parameters:**
- `obj`: Object to delete

**Example:**
```python
storage.delete(user)  # User removed from storage
```

### DBStorage

MySQL database storage system.

#### Configuration
Set environment variables:
```bash
export HBNB_TYPE_STORAGE=db
export HBNB_MYSQL_USER=your_username
export HBNB_MYSQL_PWD=your_password
export HBNB_MYSQL_HOST=localhost
export HBNB_MYSQL_DB=hbnb_dev_db
```

#### Methods
Same interface as FileStorage, but persists to MySQL database.

#### Database Schema
```sql
-- Users table
CREATE TABLE users (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    email VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(128),
    last_name VARCHAR(128)
);

-- States table
CREATE TABLE states (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    name VARCHAR(128) NOT NULL
);

-- Cities table
CREATE TABLE cities (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    name VARCHAR(128) NOT NULL,
    state_id VARCHAR(60) NOT NULL,
    FOREIGN KEY (state_id) REFERENCES states(id)
);

-- Places table
CREATE TABLE places (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    city_id VARCHAR(60) NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(1024),
    number_rooms INTEGER DEFAULT 0,
    number_bathrooms INTEGER DEFAULT 0,
    max_guest INTEGER DEFAULT 0,
    price_by_night INTEGER DEFAULT 0,
    latitude FLOAT,
    longitude FLOAT,
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Amenities table
CREATE TABLE amenities (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    name VARCHAR(128) NOT NULL
);

-- Reviews table
CREATE TABLE reviews (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    text VARCHAR(1024) NOT NULL,
    place_id VARCHAR(60) NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Place-Amenity association table
CREATE TABLE place_amenity (
    place_id VARCHAR(60) NOT NULL,
    amenity_id VARCHAR(60) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);
```

## Console Interface

Interactive command-line interface for managing objects.

### Starting the Console
```bash
./console.py
```

### Available Commands

#### `create <class_name> [<param1>=<value1> <param2>=<value2> ...]`
Create a new instance of a class.

**Parameters:**
- `class_name`: Name of the class to create
- `param=value`: Optional parameters to set

**Examples:**
```bash
(hbnb) create User
12345678-1234-1234-1234-123456789012

(hbnb) create State name="California"
87654321-4321-4321-4321-210987654321

(hbnb) create Place city_id="city-id" user_id="user-id" name="My_Place" number_rooms=4 price_by_night=120 latitude=37.7749 longitude=-122.4194
```

#### `show <class_name> <id>`
Display an object by class and ID.

**Examples:**
```bash
(hbnb) show User 12345678-1234-1234-1234-123456789012
[User] (12345678-1234-1234-1234-123456789012) {'id': '12345678-1234-1234-1234-123456789012', 'created_at': datetime.datetime(2023, 1, 1, 0, 0, 0), 'updated_at': datetime.datetime(2023, 1, 1, 0, 0, 0)}
```

#### `all [<class_name>]`
Display all objects or all objects of a specific class.

**Examples:**
```bash
(hbnb) all
["[User] (12345678-1234-1234-1234-123456789012) {...}", "[State] (87654321-4321-4321-4321-210987654321) {...}"]

(hbnb) all User
["[User] (12345678-1234-1234-1234-123456789012) {...}"]
```

#### `update <class_name> <id> <attribute_name> "<attribute_value>"`
Update an object's attribute.

**Examples:**
```bash
(hbnb) update User 12345678-1234-1234-1234-123456789012 first_name "John"
(hbnb) update User 12345678-1234-1234-1234-123456789012 age 25
```

#### `destroy <class_name> <id>`
Delete an object.

**Examples:**
```bash
(hbnb) destroy User 12345678-1234-1234-1234-123456789012
```

#### `count <class_name>`
Count objects of a specific class.

**Examples:**
```bash
(hbnb) count User
3
```

#### Alternative Syntax
The console also supports method-style commands:

```bash
(hbnb) User.all()
(hbnb) User.count()
(hbnb) User.show("12345678-1234-1234-1234-123456789012")
(hbnb) User.destroy("12345678-1234-1234-1234-123456789012")
(hbnb) User.update("12345678-1234-1234-1234-123456789012", "first_name", "John")
(hbnb) User.update("12345678-1234-1234-1234-123456789012", {"first_name": "John", "age": 25})
```

## Web Framework

Flask-based web application providing HTTP endpoints.

### Basic Routes

#### Hello Route (`/`)
**File:** `web_flask/0-hello_route.py`

Simple greeting endpoint.

**Example:**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Return greeting message"""
    return 'Hello HBNB!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

**Usage:**
```bash
curl http://localhost:5000/
# Output: Hello HBNB!
```

#### States List (`/states_list`)
**File:** `web_flask/7-states_list.py`

Display all states from storage.

**Example:**
```python
from flask import Flask, render_template
from models import storage

app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display all states"""
    all_states = storage.all("State").values()
    return render_template('7-states_list.html', all_states=all_states)

@app.teardown_appcontext
def teardown(self):
    """Close storage session"""
    storage.close()
```

**Template (`templates/7-states_list.html`):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>HBNB</title>
</head>
<body>
    <h1>States</h1>
    <ul>
    {% for state in all_states|sort(attribute='name') %}
        <li>{{ state.id }}: <b>{{ state.name }}</b></li>
    {% endfor %}
    </ul>
</body>
</html>
```

### Advanced Routes

#### Dynamic Routes with Parameters
**File:** `web_flask/4-number_route.py`

```python
@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Display number if it's an integer"""
    return f"{n} is a number"
```

#### Template Rendering with Filters
**File:** `web_flask/10-hbnb_filters.py`

Complete filtering interface for places.

```python
@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Display filters page"""
    states = storage.all("State").values()
    amenities = storage.all("Amenity").values()
    return render_template('10-hbnb_filters.html', 
                         states=states, amenities=amenities)
```

## Deployment Scripts

Automated deployment using Fabric.

### Pack Web Static (`1-pack_web_static.py`)
Create a compressed archive of web static files.

**Example:**
```python
from fabric.api import local
from datetime import datetime

def do_pack():
    """Create archive of web_static folder"""
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"web_static_{datetime_str}.tgz"
    
    try:
        local('mkdir -p versions')
        local(f'tar -cvzf versions/{file_name} web_static')
        return f"versions/{file_name}"
    except:
        return None
```

**Usage:**
```bash
fab -f 1-pack_web_static.py do_pack
```

### Deploy Web Static (`3-deploy_web_static.py`)
Complete deployment pipeline.

**Functions:**
- `do_pack()`: Create archive
- `do_deploy(archive_path)`: Deploy to servers
- `deploy()`: Complete deployment process

**Usage:**
```bash
fab -f 3-deploy_web_static.py deploy
```

**Server Configuration:**
```python
env.hosts = ['server1.example.com', 'server2.example.com']
```

## Usage Examples

### Complete Workflow Example

```python
#!/usr/bin/env python3
"""Complete workflow example"""

from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage

# Create a user
user = User()
user.email = "john@example.com"
user.password = "secure123"
user.first_name = "John"
user.last_name = "Doe"
user.save()

# Create a state and city
state = State()
state.name = "California"
state.save()

city = City()
city.name = "San Francisco"
city.state_id = state.id
city.save()

# Create amenities
wifi = Amenity()
wifi.name = "WiFi"
wifi.save()

parking = Amenity()
parking.name = "Parking"
parking.save()

# Create a place
place = Place()
place.name = "Cozy Downtown Apartment"
place.description = "Beautiful apartment in the heart of the city"
place.city_id = city.id
place.user_id = user.id
place.number_rooms = 2
place.number_bathrooms = 1
place.max_guest = 4
place.price_by_night = 150
place.latitude = 37.7749
place.longitude = -122.4194
place.save()

# Associate amenities with place (DB storage only)
if hasattr(place, 'amenities'):
    place.amenities.extend([wifi, parking])
    place.save()

# Create a review
review = Review()
review.place_id = place.id
review.user_id = user.id
review.text = "Amazing place! Great location and very clean."
review.save()

# Query data
print("All users:", storage.all(User))
print("All places in San Francisco:", [p for p in storage.all(Place).values() 
                                      if p.city_id == city.id])
print("Reviews for place:", [r for r in storage.all(Review).values() 
                            if r.place_id == place.id])
```

### Console Usage Example

```bash
# Start the console
./console.py

# Create objects
(hbnb) create User email="jane@example.com" password="pass123" first_name="Jane"
abcd1234-5678-9012-3456-789012345678

(hbnb) create State name="New_York"
efgh5678-9012-3456-7890-123456789012

(hbnb) create City name="New_York_City" state_id="efgh5678-9012-3456-7890-123456789012"
ijkl9012-3456-7890-1234-567890123456

# Show objects
(hbnb) show User abcd1234-5678-9012-3456-789012345678
[User] (abcd1234-5678-9012-3456-789012345678) {'id': 'abcd1234-5678-9012-3456-789012345678', 'email': 'jane@example.com', ...}

# Update objects
(hbnb) update User abcd1234-5678-9012-3456-789012345678 last_name "Smith"

# List all objects of a type
(hbnb) all State
["[State] (efgh5678-9012-3456-7890-123456789012) {...}"]

# Count objects
(hbnb) count User
1

# Alternative syntax
(hbnb) User.all()
(hbnb) State.count()
```

### Web Application Usage

```bash
# Start the web application
cd web_flask
python3 7-states_list.py

# Access endpoints
curl http://localhost:5000/states_list
# Returns HTML page with all states

# With templates and static files
python3 100-hbnb.py
# Full web interface available at http://localhost:5000/hbnb
```

## API Reference

### Model Methods Summary

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `__init__(**kwargs)` | Initialize object | kwargs: object attributes | None |
| `save()` | Save object to storage | None | None |
| `to_dict()` | Convert to dictionary | None | dict |
| `delete()` | Remove from storage | None | None |
| `__str__()` | String representation | None | str |

### Storage Methods Summary

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `all(cls=None)` | Get all objects | cls: class filter | dict |
| `new(obj)` | Add object | obj: object to add | None |
| `save()` | Persist to storage | None | None |
| `reload()` | Load from storage | None | None |
| `delete(obj)` | Remove object | obj: object to remove | None |
| `close()` | Close storage session | None | None |

### Console Commands Summary

| Command | Description | Syntax | Example |
|---------|-------------|--------|---------|
| `create` | Create new object | `create <class> [params]` | `create User email="test@test.com"` |
| `show` | Display object | `show <class> <id>` | `show User 1234-5678` |
| `all` | List objects | `all [<class>]` | `all User` |
| `update` | Modify object | `update <class> <id> <attr> <value>` | `update User 1234 name "John"` |
| `destroy` | Delete object | `destroy <class> <id>` | `destroy User 1234` |
| `count` | Count objects | `count <class>` | `count User` |
| `quit/EOF` | Exit console | `quit` or Ctrl+D | `quit` |

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `HBNB_TYPE_STORAGE` | Storage backend | `file` | `db` |
| `HBNB_MYSQL_USER` | MySQL username | None | `hbnb_dev` |
| `HBNB_MYSQL_PWD` | MySQL password | None | `hbnb_dev_pwd` |
| `HBNB_MYSQL_HOST` | MySQL host | None | `localhost` |
| `HBNB_MYSQL_DB` | MySQL database | None | `hbnb_dev_db` |
| `HBNB_ENV` | Environment | None | `test` |

### Error Handling

Common error scenarios and solutions:

#### Storage Errors
```python
# FileNotFoundError: file.json doesn't exist
# Solution: Run storage.save() to create the file

# MySQL connection errors
# Solution: Check environment variables and database status
```

#### Console Errors
```bash
# ** class doesn't exist **
# Solution: Use valid class names (User, State, City, Place, Amenity, Review)

# ** no instance found **
# Solution: Verify object ID exists using 'all' command

# ** missing attribute **
# Solution: Provide all required parameters for create command
```

#### Web Application Errors
```python
# Template not found
# Solution: Ensure templates directory exists with required HTML files

# Storage session errors
# Solution: Implement proper teardown_appcontext handlers
```

---

## Contributing

When extending the API:

1. **Models**: Inherit from `BaseModel` and follow SQLAlchemy patterns
2. **Storage**: Implement both file and database storage methods
3. **Console**: Add commands to `HBNBCommand` class
4. **Web**: Follow Flask best practices and implement teardown handlers
5. **Tests**: Write comprehensive unit tests for all new functionality

## License

This project is part of the Holberton School curriculum.