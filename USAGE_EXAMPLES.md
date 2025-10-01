# AirBnB Clone - Comprehensive Usage Examples

## Table of Contents
1. [Getting Started](#getting-started)
2. [Model Usage Examples](#model-usage-examples)
3. [Storage Examples](#storage-examples)
4. [Console Usage Examples](#console-usage-examples)
5. [Web Application Examples](#web-application-examples)
6. [Deployment Examples](#deployment-examples)
7. [Advanced Scenarios](#advanced-scenarios)
8. [Testing Examples](#testing-examples)

## Getting Started

### Environment Setup

#### File Storage (Default)
```bash
# Clone the repository
git clone <repository_url>
cd AirBnB_clone

# No additional setup required for file storage
python3 console.py
```

#### Database Storage
```bash
# Set up MySQL database
mysql -u root -p < setup_mysql_dev.sql

# Set environment variables
export HBNB_TYPE_STORAGE=db
export HBNB_MYSQL_USER=hbnb_dev
export HBNB_MYSQL_PWD=hbnb_dev_pwd
export HBNB_MYSQL_HOST=localhost
export HBNB_MYSQL_DB=hbnb_dev_db

# Start console with database storage
python3 console.py
```

### Basic Project Structure
```
AirBnB_clone/
├── models/
│   ├── __init__.py          # Storage initialization
│   ├── base_model.py        # Base class for all models
│   ├── user.py             # User model
│   ├── state.py            # State model
│   ├── city.py             # City model
│   ├── place.py            # Place model
│   ├── amenity.py          # Amenity model
│   ├── review.py           # Review model
│   └── engine/
│       ├── file_storage.py  # File-based storage
│       └── db_storage.py    # Database storage
├── console.py              # Command interpreter
├── web_flask/              # Flask web application
└── tests/                  # Unit tests
```

## Model Usage Examples

### Creating and Managing Users

#### Basic User Operations
```python
#!/usr/bin/env python3
"""User management examples"""

from models.user import User
from models import storage

# Create a new user
user = User()
user.email = "john.doe@example.com"
user.password = "secure_password_123"
user.first_name = "John"
user.last_name = "Doe"

# Save to storage
user.save()
print(f"Created user: {user.id}")

# Retrieve user
retrieved_user = storage.all(User)[f"User.{user.id}"]
print(f"Retrieved: {retrieved_user.first_name} {retrieved_user.last_name}")

# Update user
user.first_name = "Johnny"
user.save()
print(f"Updated name: {user.first_name}")

# Convert to dictionary
user_dict = user.to_dict()
print(f"User as dict: {user_dict}")

# Create user from dictionary
new_user = User(**user_dict)
print(f"Recreated user: {new_user.email}")
```

#### User with Validation
```python
#!/usr/bin/env python3
"""User creation with validation"""

from models.user import User
import re

def create_user_with_validation(email, password, first_name, last_name):
    """Create user with email validation"""
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")
    
    # Validate password strength
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    
    # Create user
    user = User()
    user.email = email
    user.password = password
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    
    return user

# Example usage
try:
    user = create_user_with_validation(
        "jane.smith@example.com",
        "strongpassword123",
        "Jane",
        "Smith"
    )
    print(f"User created successfully: {user.id}")
except ValueError as e:
    print(f"Validation error: {e}")
```

### Geographic Data Management

#### States and Cities
```python
#!/usr/bin/env python3
"""Geographic data management"""

from models.state import State
from models.city import City
from models import storage

# Create states
california = State()
california.name = "California"
california.save()

new_york = State()
new_york.name = "New York"
new_york.save()

# Create cities in California
sf = City()
sf.name = "San Francisco"
sf.state_id = california.id
sf.save()

la = City()
la.name = "Los Angeles"
la.state_id = california.id
la.save()

# Create cities in New York
nyc = City()
nyc.name = "New York City"
nyc.state_id = new_york.id
nyc.save()

# Query cities by state
def get_cities_by_state(state_name):
    """Get all cities in a specific state"""
    states = storage.all(State)
    target_state = None
    
    for state in states.values():
        if state.name == state_name:
            target_state = state
            break
    
    if not target_state:
        return []
    
    # For database storage, use relationship
    if hasattr(target_state, 'cities'):
        return target_state.cities
    
    # For file storage, query manually
    cities = storage.all(City)
    return [city for city in cities.values() if city.state_id == target_state.id]

# Example usage
ca_cities = get_cities_by_state("California")
print(f"Cities in California: {[city.name for city in ca_cities]}")
```

### Place Management

#### Creating Places with Amenities
```python
#!/usr/bin/env python3
"""Place and amenity management"""

from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models import storage

# Create necessary objects
user = User(email="host@example.com", password="hostpass", first_name="Host")
user.save()

state = State(name="California")
state.save()

city = City(name="San Francisco", state_id=state.id)
city.save()

# Create amenities
wifi = Amenity(name="WiFi")
wifi.save()

parking = Amenity(name="Parking")
parking.save()

kitchen = Amenity(name="Kitchen")
kitchen.save()

pool = Amenity(name="Swimming Pool")
pool.save()

# Create a place
place = Place()
place.name = "Luxury Downtown Apartment"
place.description = "Beautiful apartment with stunning city views"
place.city_id = city.id
place.user_id = user.id
place.number_rooms = 3
place.number_bathrooms = 2
place.max_guest = 6
place.price_by_night = 200
place.latitude = 37.7749
place.longitude = -122.4194
place.save()

# Associate amenities (for database storage)
if hasattr(place, 'amenities'):
    place.amenities.extend([wifi, parking, kitchen, pool])
    place.save()
else:
    # For file storage, manage amenity_ids list
    place.amenity_ids = [wifi.id, parking.id, kitchen.id, pool.id]
    place.save()

print(f"Created place: {place.name}")
print(f"Location: {place.latitude}, {place.longitude}")
print(f"Capacity: {place.max_guest} guests, {place.number_rooms} rooms")
print(f"Price: ${place.price_by_night}/night")
```

#### Place Search and Filtering
```python
#!/usr/bin/env python3
"""Place search functionality"""

from models.place import Place
from models.city import City
from models.state import State
from models import storage

def search_places(city_name=None, state_name=None, min_price=None, max_price=None, 
                 min_guests=None, amenities=None):
    """Search places with various filters"""
    
    places = storage.all(Place).values()
    results = []
    
    for place in places:
        # Filter by city
        if city_name:
            city = storage.all(City).get(f"City.{place.city_id}")
            if not city or city.name != city_name:
                continue
        
        # Filter by state
        if state_name:
            city = storage.all(City).get(f"City.{place.city_id}")
            if city:
                state = storage.all(State).get(f"State.{city.state_id}")
                if not state or state.name != state_name:
                    continue
        
        # Filter by price range
        if min_price and place.price_by_night < min_price:
            continue
        if max_price and place.price_by_night > max_price:
            continue
        
        # Filter by guest capacity
        if min_guests and place.max_guest < min_guests:
            continue
        
        # Filter by amenities (simplified for file storage)
        if amenities:
            place_amenity_ids = getattr(place, 'amenity_ids', [])
            if not all(amenity_id in place_amenity_ids for amenity_id in amenities):
                continue
        
        results.append(place)
    
    return results

# Example searches
print("=== Search Examples ===")

# Find places in San Francisco
sf_places = search_places(city_name="San Francisco")
print(f"Places in San Francisco: {len(sf_places)}")

# Find affordable places (under $150/night)
affordable_places = search_places(max_price=150)
print(f"Places under $150/night: {len(affordable_places)}")

# Find places for large groups (6+ guests)
large_places = search_places(min_guests=6)
print(f"Places for 6+ guests: {len(large_places)}")

# Combined search
luxury_sf_places = search_places(
    city_name="San Francisco",
    min_price=150,
    min_guests=4
)
print(f"Luxury SF places for 4+ guests: {len(luxury_sf_places)}")
```

### Review System

#### Creating and Managing Reviews
```python
#!/usr/bin/env python3
"""Review management system"""

from models.user import User
from models.place import Place
from models.review import Review
from models import storage
from datetime import datetime

def add_review(place_id, user_id, rating, comment):
    """Add a review for a place"""
    
    # Validate place exists
    place_key = f"Place.{place_id}"
    if place_key not in storage.all(Place):
        raise ValueError("Place not found")
    
    # Validate user exists
    user_key = f"User.{user_id}"
    if user_key not in storage.all(User):
        raise ValueError("User not found")
    
    # Create review
    review = Review()
    review.place_id = place_id
    review.user_id = user_id
    review.text = f"Rating: {rating}/5 - {comment}"
    review.save()
    
    return review

def get_place_reviews(place_id):
    """Get all reviews for a place"""
    reviews = storage.all(Review)
    place_reviews = [review for review in reviews.values() 
                    if review.place_id == place_id]
    return place_reviews

def calculate_place_rating(place_id):
    """Calculate average rating for a place"""
    reviews = get_place_reviews(place_id)
    if not reviews:
        return 0
    
    total_rating = 0
    count = 0
    
    for review in reviews:
        # Extract rating from review text (simplified)
        try:
            rating_part = review.text.split("Rating: ")[1].split("/5")[0]
            rating = float(rating_part)
            total_rating += rating
            count += 1
        except (IndexError, ValueError):
            continue
    
    return total_rating / count if count > 0 else 0

# Example usage
try:
    # Assume we have place_id and user_id from previous examples
    places = list(storage.all(Place).values())
    users = list(storage.all(User).values())
    
    if places and users:
        place = places[0]
        user = users[0]
        
        # Add some reviews
        review1 = add_review(place.id, user.id, 5, "Excellent place! Clean and comfortable.")
        review2 = add_review(place.id, user.id, 4, "Great location, minor issues with WiFi.")
        
        # Get reviews
        reviews = get_place_reviews(place.id)
        print(f"Reviews for {place.name}: {len(reviews)}")
        
        for review in reviews:
            print(f"- {review.text}")
        
        # Calculate rating
        avg_rating = calculate_place_rating(place.id)
        print(f"Average rating: {avg_rating:.1f}/5")

except ValueError as e:
    print(f"Error: {e}")
```

## Storage Examples

### File Storage Operations

#### Basic File Storage Usage
```python
#!/usr/bin/env python3
"""File storage examples"""

from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State

# Create storage instance
storage = FileStorage()

# Create some objects
user1 = User(email="user1@example.com", first_name="Alice")
user2 = User(email="user2@example.com", first_name="Bob")
state1 = State(name="Texas")

# Add to storage
storage.new(user1)
storage.new(user2)
storage.new(state1)

# Save to file
storage.save()
print("Objects saved to file.json")

# Clear memory and reload
storage._FileStorage__objects = {}
print(f"Objects in memory: {len(storage.all())}")

storage.reload()
print(f"Objects after reload: {len(storage.all())}")

# Query specific types
users = storage.all(User)
print(f"Users in storage: {len(users)}")

states = storage.all(State)
print(f"States in storage: {len(states)}")
```

#### File Storage with Error Handling
```python
#!/usr/bin/env python3
"""File storage with error handling"""

import json
import os
from models.engine.file_storage import FileStorage
from models.user import User

def safe_storage_operations():
    """Demonstrate safe storage operations"""
    
    storage = FileStorage()
    
    try:
        # Create and save objects
        user = User(email="test@example.com")
        storage.new(user)
        storage.save()
        print("✓ Save operation successful")
        
        # Backup current file
        if os.path.exists("file.json"):
            with open("file.json", 'r') as f:
                backup_data = f.read()
            with open("file.json.backup", 'w') as f:
                f.write(backup_data)
            print("✓ Backup created")
        
        # Test reload
        storage.reload()
        print("✓ Reload operation successful")
        
        # Verify data integrity
        loaded_users = storage.all(User)
        if user.id in [u.id for u in loaded_users.values()]:
            print("✓ Data integrity verified")
        else:
            print("✗ Data integrity check failed")
            
    except FileNotFoundError:
        print("Storage file not found, creating new one")
        storage.save()
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        # Restore from backup if available
        if os.path.exists("file.json.backup"):
            os.rename("file.json.backup", "file.json")
            storage.reload()
            print("✓ Restored from backup")
            
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run safe operations
safe_storage_operations()
```

### Database Storage Operations

#### Database Connection and Setup
```python
#!/usr/bin/env python3
"""Database storage examples"""

import os
from models.engine.db_storage import DBStorage
from models.user import User
from models.state import State

# Set environment variables
os.environ['HBNB_TYPE_STORAGE'] = 'db'
os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
os.environ['HBNB_MYSQL_HOST'] = 'localhost'
os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'

def test_database_operations():
    """Test database storage operations"""
    
    try:
        # Create storage instance
        storage = DBStorage()
        storage.reload()
        print("✓ Database connection established")
        
        # Create objects
        user = User(email="db_user@example.com", first_name="Database")
        state = State(name="Database State")
        
        # Add to session
        storage.new(user)
        storage.new(state)
        
        # Commit to database
        storage.save()
        print("✓ Objects saved to database")
        
        # Query from database
        users = storage.all(User)
        states = storage.all(State)
        
        print(f"Users in database: {len(users)}")
        print(f"States in database: {len(states)}")
        
        # Test relationships (if using database storage)
        for user_obj in users.values():
            if hasattr(user_obj, 'places'):
                print(f"User {user_obj.first_name} has {len(user_obj.places)} places")
        
        # Close session
        storage.close()
        print("✓ Database session closed")
        
    except Exception as e:
        print(f"Database error: {e}")
        print("Make sure MySQL is running and credentials are correct")

# Run database tests
test_database_operations()
```

## Console Usage Examples

### Basic Console Commands

#### Interactive Console Session
```bash
# Start the console
$ ./console.py
(hbnb) 

# Create objects
(hbnb) create User email="john@example.com" password="pass123" first_name="John" last_name="Doe"
12345678-1234-1234-1234-123456789012

(hbnb) create State name="California"
87654321-4321-4321-4321-210987654321

(hbnb) create City name="San_Francisco" state_id="87654321-4321-4321-4321-210987654321"
abcdefgh-1234-5678-9012-123456789012

# Show objects
(hbnb) show User 12345678-1234-1234-1234-123456789012
[User] (12345678-1234-1234-1234-123456789012) {'id': '12345678-1234-1234-1234-123456789012', 'created_at': datetime.datetime(2023, 1, 1, 12, 0, 0), 'updated_at': datetime.datetime(2023, 1, 1, 12, 0, 0), 'email': 'john@example.com', 'password': 'pass123', 'first_name': 'John', 'last_name': 'Doe'}

# List all objects
(hbnb) all
["[User] (12345678-1234-1234-1234-123456789012) {...}", "[State] (87654321-4321-4321-4321-210987654321) {...}", "[City] (abcdefgh-1234-5678-9012-123456789012) {...}"]

# List objects by type
(hbnb) all User
["[User] (12345678-1234-1234-1234-123456789012) {...}"]

# Update objects
(hbnb) update User 12345678-1234-1234-1234-123456789012 first_name "Johnny"
(hbnb) update User 12345678-1234-1234-1234-123456789012 age 30

# Count objects
(hbnb) count User
1
(hbnb) count State
1

# Delete objects
(hbnb) destroy User 12345678-1234-1234-1234-123456789012

# Exit console
(hbnb) quit
```

#### Alternative Command Syntax
```bash
(hbnb) User.all()
["[User] (12345678-1234-1234-1234-123456789012) {...}"]

(hbnb) User.count()
1

(hbnb) User.show("12345678-1234-1234-1234-123456789012")
[User] (12345678-1234-1234-1234-123456789012) {...}

(hbnb) User.update("12345678-1234-1234-1234-123456789012", "first_name", "Johnny")

(hbnb) User.update("12345678-1234-1234-1234-123456789012", {"first_name": "Johnny", "age": 30})

(hbnb) User.destroy("12345678-1234-1234-1234-123456789012")
```

### Batch Console Operations

#### Script for Bulk Data Creation
```python
#!/usr/bin/env python3
"""Bulk data creation script"""

import subprocess
import sys

def run_console_command(command):
    """Run a command in the console"""
    process = subprocess.Popen(['python3', 'console.py'], 
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
    
    output, error = process.communicate(input=command + '\nquit\n')
    return output, error

def create_sample_data():
    """Create sample data using console commands"""
    
    commands = [
        # Create states
        'create State name="California"',
        'create State name="New_York"',
        'create State name="Texas"',
        
        # Create users
        'create User email="alice@example.com" password="pass123" first_name="Alice" last_name="Johnson"',
        'create User email="bob@example.com" password="pass456" first_name="Bob" last_name="Smith"',
        'create User email="charlie@example.com" password="pass789" first_name="Charlie" last_name="Brown"',
        
        # Create amenities
        'create Amenity name="WiFi"',
        'create Amenity name="Parking"',
        'create Amenity name="Kitchen"',
        'create Amenity name="Pool"',
        'create Amenity name="Gym"',
        
        # Show summary
        'count State',
        'count User',
        'count Amenity',
        'all State'
    ]
    
    print("Creating sample data...")
    for command in commands:
        print(f"Running: {command}")
        output, error = run_console_command(command)
        if error:
            print(f"Error: {error}")
        else:
            # Extract relevant output (object ID or count)
            lines = output.strip().split('\n')
            for line in lines:
                if line.startswith('[') or line.isdigit() or 'hbnb' not in line:
                    print(f"Result: {line}")

if __name__ == "__main__":
    create_sample_data()
```

## Web Application Examples

### Basic Flask Routes

#### Simple Web Server
```python
#!/usr/bin/env python3
"""Simple web server example"""

from flask import Flask, render_template, request, jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Home page"""
    return '''
    <html>
        <head><title>AirBnB Clone</title></head>
        <body>
            <h1>Welcome to AirBnB Clone</h1>
            <ul>
                <li><a href="/states">View States</a></li>
                <li><a href="/places">View Places</a></li>
                <li><a href="/api/states">API: States</a></li>
            </ul>
        </body>
    </html>
    '''

@app.route('/states', methods=['GET'])
def show_states():
    """Display all states"""
    states = storage.all(State).values()
    states_list = sorted(states, key=lambda x: x.name)
    
    html = '<html><head><title>States</title></head><body>'
    html += '<h1>States</h1><ul>'
    
    for state in states_list:
        html += f'<li><a href="/states/{state.id}">{state.name}</a></li>'
    
    html += '</ul><a href="/">Back to Home</a></body></html>'
    return html

@app.route('/states/<state_id>', methods=['GET'])
def show_state_cities(state_id):
    """Display cities in a state"""
    state = storage.all(State).get(f"State.{state_id}")
    if not state:
        return "State not found", 404
    
    # Get cities for this state
    cities = []
    if hasattr(state, 'cities'):
        cities = state.cities
    else:
        all_cities = storage.all(City).values()
        cities = [city for city in all_cities if city.state_id == state_id]
    
    cities_list = sorted(cities, key=lambda x: x.name)
    
    html = f'<html><head><title>{state.name} Cities</title></head><body>'
    html += f'<h1>Cities in {state.name}</h1><ul>'
    
    for city in cities_list:
        html += f'<li>{city.name}</li>'
    
    html += '</ul><a href="/states">Back to States</a></body></html>'
    return html

@app.route('/api/states', methods=['GET'])
def api_states():
    """API endpoint for states"""
    states = storage.all(State).values()
    states_data = []
    
    for state in states:
        state_dict = state.to_dict()
        # Add cities count
        if hasattr(state, 'cities'):
            state_dict['cities_count'] = len(state.cities)
        else:
            all_cities = storage.all(City).values()
            cities = [city for city in all_cities if city.state_id == state.id]
            state_dict['cities_count'] = len(cities)
        
        states_data.append(state_dict)
    
    return jsonify(states_data)

@app.teardown_appcontext
def teardown(exception):
    """Close storage session"""
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### Advanced Web Application with Templates
```python
#!/usr/bin/env python3
"""Advanced web application with templates"""

from flask import Flask, render_template, request, redirect, url_for, flash
from models import storage
from models.user import User
from models.place import Place
from models.review import Review

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/places', methods=['GET'])
def list_places():
    """List all places with filters"""
    
    # Get filter parameters
    city_filter = request.args.get('city', '')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    
    # Get all places
    places = storage.all(Place).values()
    
    # Apply filters
    filtered_places = []
    for place in places:
        # City filter
        if city_filter:
            city = storage.all(City).get(f"City.{place.city_id}")
            if not city or city_filter.lower() not in city.name.lower():
                continue
        
        # Price filters
        if min_price and place.price_by_night < min_price:
            continue
        if max_price and place.price_by_night > max_price:
            continue
        
        filtered_places.append(place)
    
    # Sort by price
    filtered_places.sort(key=lambda x: x.price_by_night)
    
    return render_template('places.html', 
                         places=filtered_places,
                         city_filter=city_filter,
                         min_price=min_price,
                         max_price=max_price)

@app.route('/places/<place_id>', methods=['GET'])
def show_place(place_id):
    """Show place details with reviews"""
    
    place = storage.all(Place).get(f"Place.{place_id}")
    if not place:
        flash('Place not found', 'error')
        return redirect(url_for('list_places'))
    
    # Get place owner
    owner = storage.all(User).get(f"User.{place.user_id}")
    
    # Get place city and state
    city = storage.all(City).get(f"City.{place.city_id}")
    state = None
    if city:
        state = storage.all(State).get(f"State.{city.state_id}")
    
    # Get reviews
    all_reviews = storage.all(Review).values()
    reviews = [review for review in all_reviews if review.place_id == place_id]
    
    # Get review authors
    review_data = []
    for review in reviews:
        author = storage.all(User).get(f"User.{review.user_id}")
        review_data.append({
            'review': review,
            'author': author
        })
    
    return render_template('place_detail.html',
                         place=place,
                         owner=owner,
                         city=city,
                         state=state,
                         reviews=review_data)

@app.route('/places/<place_id>/review', methods=['POST'])
def add_review(place_id):
    """Add a review to a place"""
    
    # Get form data
    user_email = request.form.get('user_email')
    review_text = request.form.get('review_text')
    
    if not user_email or not review_text:
        flash('Please provide both email and review text', 'error')
        return redirect(url_for('show_place', place_id=place_id))
    
    # Find user by email
    users = storage.all(User).values()
    user = None
    for u in users:
        if u.email == user_email:
            user = u
            break
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('show_place', place_id=place_id))
    
    # Create review
    review = Review()
    review.place_id = place_id
    review.user_id = user.id
    review.text = review_text
    review.save()
    
    flash('Review added successfully', 'success')
    return redirect(url_for('show_place', place_id=place_id))

# Template files would be in templates/ directory
```

### Template Examples

#### places.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Places - AirBnB Clone</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .filter-form { background: #f5f5f5; padding: 20px; margin-bottom: 20px; }
        .place-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; }
        .place-title { color: #333; font-size: 18px; font-weight: bold; }
        .place-price { color: #e74c3c; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Available Places</h1>
    
    <!-- Filter Form -->
    <div class="filter-form">
        <h3>Filter Places</h3>
        <form method="GET">
            <label>City: <input type="text" name="city" value="{{ city_filter or '' }}"></label>
            <label>Min Price: <input type="number" name="min_price" value="{{ min_price or '' }}"></label>
            <label>Max Price: <input type="number" name="max_price" value="{{ max_price or '' }}"></label>
            <button type="submit">Filter</button>
            <a href="{{ url_for('list_places') }}">Clear Filters</a>
        </form>
    </div>
    
    <!-- Places List -->
    {% if places %}
        <p>Found {{ places|length }} places</p>
        {% for place in places %}
        <div class="place-card">
            <div class="place-title">
                <a href="{{ url_for('show_place', place_id=place.id) }}">{{ place.name }}</a>
            </div>
            <p>{{ place.description[:100] }}{% if place.description|length > 100 %}...{% endif %}</p>
            <p>Guests: {{ place.max_guest }} | Rooms: {{ place.number_rooms }} | Bathrooms: {{ place.number_bathrooms }}</p>
            <div class="place-price">${{ place.price_by_night }}/night</div>
        </div>
        {% endfor %}
    {% else %}
        <p>No places found matching your criteria.</p>
    {% endif %}
</body>
</html>
```

## Deployment Examples

### Fabric Deployment Scripts

#### Complete Deployment Workflow
```python
#!/usr/bin/env python3
"""Complete deployment workflow"""

from fabric.api import local, env, run, put, cd, sudo
from datetime import datetime
import os

# Server configuration
env.hosts = ['web-01.example.com', 'web-02.example.com']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def setup_server():
    """Initial server setup"""
    
    print("Setting up web server...")
    
    # Update system
    sudo('apt-get update')
    sudo('apt-get install -y nginx python3 python3-pip')
    
    # Create directories
    sudo('mkdir -p /data/web_static/releases/')
    sudo('mkdir -p /data/web_static/shared/')
    
    # Set permissions
    sudo('chown -R ubuntu:ubuntu /data/')
    
    # Configure Nginx
    nginx_config = '''
server {
    listen 80;
    server_name _;
    
    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
'''
    
    # Write Nginx config
    sudo('echo "%s" > /etc/nginx/sites-available/hbnb' % nginx_config)
    sudo('ln -sf /etc/nginx/sites-available/hbnb /etc/nginx/sites-enabled/')
    sudo('rm -f /etc/nginx/sites-enabled/default')
    sudo('nginx -t')
    sudo('service nginx restart')
    
    print("✓ Server setup complete")

def deploy_static():
    """Deploy static files"""
    
    print("Deploying static files...")
    
    # Create archive
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = f"versions/{archive_name}"
    
    # Create versions directory
    local('mkdir -p versions')
    
    # Create archive
    local(f'tar -czf {archive_path} web_static/')
    
    if not os.path.exists(archive_path):
        print("✗ Failed to create archive")
        return False
    
    print(f"✓ Archive created: {archive_path}")
    
    # Upload to servers
    put(archive_path, '/tmp/')
    
    # Extract on servers
    release_dir = f'/data/web_static/releases/web_static_{timestamp}/'
    run(f'mkdir -p {release_dir}')
    run(f'tar -xzf /tmp/{archive_name} -C {release_dir}')
    run(f'rm /tmp/{archive_name}')
    
    # Move files to correct location
    run(f'mv {release_dir}web_static/* {release_dir}')
    run(f'rm -rf {release_dir}web_static')
    
    # Update symlink
    run('rm -rf /data/web_static/current')
    run(f'ln -s {release_dir} /data/web_static/current')
    
    print("✓ Static files deployed")
    return True

def deploy_application():
    """Deploy Python application"""
    
    print("Deploying application...")
    
    # Create application directory
    app_dir = '/data/hbnb_app'
    run(f'mkdir -p {app_dir}')
    
    # Upload application files
    put('models/', f'{app_dir}/')
    put('web_flask/', f'{app_dir}/')
    put('console.py', f'{app_dir}/')
    put('requirements.txt', f'{app_dir}/')
    
    # Install dependencies
    with cd(app_dir):
        run('pip3 install -r requirements.txt')
    
    # Create systemd service
    service_config = f'''
[Unit]
Description=HBNB Flask Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory={app_dir}
Environment=HBNB_TYPE_STORAGE=db
Environment=HBNB_MYSQL_USER=hbnb_prod
Environment=HBNB_MYSQL_PWD=hbnb_prod_pwd
Environment=HBNB_MYSQL_HOST=localhost
Environment=HBNB_MYSQL_DB=hbnb_prod_db
ExecStart=/usr/bin/python3 web_flask/100-hbnb.py
Restart=always

[Install]
WantedBy=multi-user.target
'''
    
    sudo(f'echo "{service_config}" > /etc/systemd/system/hbnb.service')
    sudo('systemctl daemon-reload')
    sudo('systemctl enable hbnb')
    sudo('systemctl start hbnb')
    
    print("✓ Application deployed")

def deploy():
    """Complete deployment"""
    
    print("Starting deployment...")
    
    # Deploy static files
    if not deploy_static():
        return False
    
    # Deploy application
    deploy_application()
    
    # Restart services
    sudo('systemctl restart nginx')
    sudo('systemctl restart hbnb')
    
    print("✓ Deployment complete")
    return True

def rollback():
    """Rollback to previous version"""
    
    print("Rolling back deployment...")
    
    # Get list of releases
    releases = run('ls -t /data/web_static/releases/').split()
    
    if len(releases) < 2:
        print("✗ No previous version to rollback to")
        return False
    
    # Get previous release
    previous_release = releases[1]
    release_path = f'/data/web_static/releases/{previous_release}'
    
    # Update symlink
    run('rm -rf /data/web_static/current')
    run(f'ln -s {release_path} /data/web_static/current')
    
    # Restart services
    sudo('systemctl restart nginx')
    
    print(f"✓ Rolled back to {previous_release}")

def status():
    """Check deployment status"""
    
    print("Checking deployment status...")
    
    # Check Nginx
    nginx_status = run('systemctl is-active nginx', warn_only=True)
    print(f"Nginx: {nginx_status}")
    
    # Check application
    app_status = run('systemctl is-active hbnb', warn_only=True)
    print(f"Application: {app_status}")
    
    # Check current release
    current_release = run('readlink /data/web_static/current', warn_only=True)
    print(f"Current release: {current_release}")
    
    # Check disk usage
    disk_usage = run('df -h /data', warn_only=True)
    print(f"Disk usage:\n{disk_usage}")

# Usage examples:
# fab setup_server
# fab deploy
# fab rollback
# fab status
```

### Monitoring and Maintenance

#### Health Check Script
```python
#!/usr/bin/env python3
"""Health check and monitoring script"""

import requests
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import subprocess
import os

def check_web_service(url="http://localhost:5000"):
    """Check if web service is responding"""
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True, "Web service is healthy"
        else:
            return False, f"Web service returned status {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Web service error: {e}"

def check_database_connection():
    """Check database connectivity"""
    
    try:
        from models import storage
        from models.user import User
        
        # Try to query database
        users = storage.all(User)
        return True, f"Database healthy, {len(users)} users found"
        
    except Exception as e:
        return False, f"Database error: {e}"

def check_disk_space(threshold=80):
    """Check disk space usage"""
    
    try:
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        
        if len(lines) >= 2:
            parts = lines[1].split()
            usage_percent = int(parts[4].rstrip('%'))
            
            if usage_percent > threshold:
                return False, f"Disk usage high: {usage_percent}%"
            else:
                return True, f"Disk usage normal: {usage_percent}%"
        
        return False, "Could not parse disk usage"
        
    except Exception as e:
        return False, f"Disk check error: {e}"

def check_log_errors(log_file="/var/log/hbnb.log", max_errors=10):
    """Check for recent errors in log file"""
    
    try:
        if not os.path.exists(log_file):
            return True, "Log file not found (may be normal)"
        
        # Count ERROR lines in last 100 lines
        result = subprocess.run(['tail', '-100', log_file], capture_output=True, text=True)
        error_count = result.stdout.count('ERROR')
        
        if error_count > max_errors:
            return False, f"High error count in logs: {error_count}"
        else:
            return True, f"Log errors normal: {error_count}"
            
    except Exception as e:
        return False, f"Log check error: {e}"

def send_alert(subject, message, to_email="admin@example.com"):
    """Send email alert"""
    
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = "monitor@hbnb.com"
        msg['To'] = to_email
        
        # Configure SMTP server
        server = smtplib.SMTP('localhost')
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Failed to send alert: {e}")
        return False

def run_health_checks():
    """Run all health checks"""
    
    checks = [
        ("Web Service", check_web_service),
        ("Database", check_database_connection),
        ("Disk Space", check_disk_space),
        ("Log Errors", check_log_errors)
    ]
    
    results = []
    all_healthy = True
    
    print(f"Health Check Report - {datetime.now()}")
    print("=" * 50)
    
    for check_name, check_func in checks:
        try:
            healthy, message = check_func()
            status = "✓ PASS" if healthy else "✗ FAIL"
            print(f"{check_name}: {status} - {message}")
            
            results.append({
                'check': check_name,
                'healthy': healthy,
                'message': message
            })
            
            if not healthy:
                all_healthy = False
                
        except Exception as e:
            print(f"{check_name}: ✗ ERROR - {e}")
            results.append({
                'check': check_name,
                'healthy': False,
                'message': str(e)
            })
            all_healthy = False
    
    # Send alert if any checks failed
    if not all_healthy:
        failed_checks = [r for r in results if not r['healthy']]
        alert_message = "Health check failures:\n\n"
        
        for check in failed_checks:
            alert_message += f"- {check['check']}: {check['message']}\n"
        
        send_alert("HBNB Health Check Alert", alert_message)
    
    return all_healthy, results

if __name__ == "__main__":
    healthy, results = run_health_checks()
    exit_code = 0 if healthy else 1
    exit(exit_code)
```

## Advanced Scenarios

### Data Migration

#### File Storage to Database Migration
```python
#!/usr/bin/env python3
"""Migrate data from file storage to database"""

import json
import os
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

def migrate_file_to_db():
    """Migrate data from file.json to database"""
    
    print("Starting migration from file storage to database...")
    
    # Set up file storage
    file_storage = FileStorage()
    file_storage.reload()
    
    # Set up database storage
    os.environ['HBNB_TYPE_STORAGE'] = 'db'
    db_storage = DBStorage()
    db_storage.reload()
    
    # Get all objects from file storage
    all_objects = file_storage.all()
    
    print(f"Found {len(all_objects)} objects to migrate")
    
    # Migration order (to handle foreign key dependencies)
    migration_order = [
        ('User', User),
        ('State', State),
        ('Amenity', Amenity),
        ('City', City),
        ('Place', Place),
        ('Review', Review)
    ]
    
    migrated_count = 0
    
    for class_name, class_type in migration_order:
        print(f"Migrating {class_name} objects...")
        
        class_objects = [obj for obj in all_objects.values() 
                        if obj.__class__.__name__ == class_name]
        
        for obj in class_objects:
            try:
                # Create new object for database
                obj_dict = obj.to_dict()
                del obj_dict['__class__']  # Remove class info
                
                new_obj = class_type(**obj_dict)
                db_storage.new(new_obj)
                migrated_count += 1
                
            except Exception as e:
                print(f"Error migrating {class_name} {obj.id}: {e}")
        
        # Save batch
        try:
            db_storage.save()
            print(f"✓ {class_name} objects migrated")
        except Exception as e:
            print(f"✗ Error saving {class_name} objects: {e}")
    
    print(f"Migration complete. {migrated_count} objects migrated.")
    
    # Verify migration
    db_objects = db_storage.all()
    print(f"Database now contains {len(db_objects)} objects")
    
    db_storage.close()

if __name__ == "__main__":
    migrate_file_to_db()
```

### Performance Testing

#### Load Testing Script
```python
#!/usr/bin/env python3
"""Performance testing for AirBnB Clone"""

import time
import threading
import requests
import statistics
from concurrent.futures import ThreadPoolExecutor
from models import storage
from models.user import User
from models.place import Place

def time_function(func, *args, **kwargs):
    """Time a function execution"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def test_storage_performance():
    """Test storage operation performance"""
    
    print("Testing storage performance...")
    
    # Test object creation
    creation_times = []
    for i in range(100):
        user = User(email=f"test{i}@example.com", first_name=f"User{i}")
        _, duration = time_function(user.save)
        creation_times.append(duration)
    
    print(f"Object creation - Avg: {statistics.mean(creation_times):.4f}s, "
          f"Max: {max(creation_times):.4f}s")
    
    # Test queries
    query_times = []
    for i in range(50):
        _, duration = time_function(storage.all, User)
        query_times.append(duration)
    
    print(f"Query all users - Avg: {statistics.mean(query_times):.4f}s, "
          f"Max: {max(query_times):.4f}s")
    
    # Clean up
    users = storage.all(User)
    for user in users.values():
        if user.email.startswith("test"):
            user.delete()

def test_web_performance(base_url="http://localhost:5000", num_requests=100):
    """Test web application performance"""
    
    print(f"Testing web performance with {num_requests} requests...")
    
    endpoints = [
        "/",
        "/states_list",
        "/api/states"
    ]
    
    def make_request(url):
        """Make a single request and return response time"""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            return {
                'url': url,
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'success': response.status_code == 200
            }
        except Exception as e:
            return {
                'url': url,
                'status_code': 0,
                'response_time': 0,
                'success': False,
                'error': str(e)
            }
    
    # Test each endpoint
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"\nTesting {endpoint}...")
        
        # Sequential requests
        sequential_times = []
        for _ in range(10):
            result = make_request(url)
            if result['success']:
                sequential_times.append(result['response_time'])
        
        if sequential_times:
            print(f"Sequential - Avg: {statistics.mean(sequential_times):.4f}s")
        
        # Concurrent requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request, url) for _ in range(num_requests)]
            results = [future.result() for future in futures]
        
        successful_results = [r for r in results if r['success']]
        failed_results = [r for r in results if not r['success']]
        
        if successful_results:
            response_times = [r['response_time'] for r in successful_results]
            print(f"Concurrent - Success: {len(successful_results)}/{num_requests}, "
                  f"Avg: {statistics.mean(response_times):.4f}s, "
                  f"Max: {max(response_times):.4f}s")
        
        if failed_results:
            print(f"Failed requests: {len(failed_results)}")

def stress_test_console():
    """Stress test console operations"""
    
    print("Stress testing console operations...")
    
    import subprocess
    
    def run_console_command(command):
        """Run console command and measure time"""
        start_time = time.time()
        process = subprocess.run(['python3', 'console.py'], 
                               input=f"{command}\nquit\n",
                               text=True, capture_output=True)
        end_time = time.time()
        
        return {
            'command': command,
            'duration': end_time - start_time,
            'success': process.returncode == 0,
            'output': process.stdout
        }
    
    # Test commands
    commands = [
        'create User email="stress@test.com" first_name="Stress"',
        'all User',
        'count User',
        'User.all()',
        'User.count()'
    ]
    
    for command in commands:
        print(f"\nTesting: {command}")
        
        times = []
        for _ in range(10):
            result = run_console_command(command)
            if result['success']:
                times.append(result['duration'])
        
        if times:
            print(f"Avg time: {statistics.mean(times):.4f}s, "
                  f"Max time: {max(times):.4f}s")

if __name__ == "__main__":
    print("AirBnB Clone Performance Testing")
    print("=" * 40)
    
    test_storage_performance()
    print()
    test_web_performance()
    print()
    stress_test_console()
    
    print("\nPerformance testing complete!")
```

## Testing Examples

### Unit Testing

#### Model Testing
```python
#!/usr/bin/env python3
"""Unit tests for models"""

import unittest
import os
import json
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models import storage

class TestBaseModel(unittest.TestCase):
    """Test BaseModel class"""
    
    def setUp(self):
        """Set up test environment"""
        self.model = BaseModel()
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("file.json"):
            os.remove("file.json")
    
    def test_init(self):
        """Test object initialization"""
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)
    
    def test_init_with_kwargs(self):
        """Test initialization with keyword arguments"""
        data = {
            "id": "test-id",
            "created_at": "2023-01-01T12:00:00.000000",
            "updated_at": "2023-01-01T12:00:00.000000",
            "name": "Test Model"
        }
        model = BaseModel(**data)
        
        self.assertEqual(model.id, "test-id")
        self.assertEqual(model.name, "Test Model")
        self.assertIsInstance(model.created_at, datetime)
    
    def test_str(self):
        """Test string representation"""
        string = str(self.model)
        self.assertIn("[BaseModel]", string)
        self.assertIn(self.model.id, string)
    
    def test_save(self):
        """Test save method"""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertGreater(self.model.updated_at, old_updated_at)
    
    def test_to_dict(self):
        """Test to_dict method"""
        model_dict = self.model.to_dict()
        
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(model_dict['id'], self.model.id)
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)

class TestUser(unittest.TestCase):
    """Test User class"""
    
    def setUp(self):
        """Set up test environment"""
        self.user = User()
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("file.json"):
            os.remove("file.json")
    
    def test_user_attributes(self):
        """Test User attributes"""
        self.assertTrue(hasattr(self.user, 'email'))
        self.assertTrue(hasattr(self.user, 'password'))
        self.assertTrue(hasattr(self.user, 'first_name'))
        self.assertTrue(hasattr(self.user, 'last_name'))
    
    def test_user_creation(self):
        """Test User creation with attributes"""
        user = User(
            email="test@example.com",
            password="testpass",
            first_name="Test",
            last_name="User"
        )
        
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

class TestStorage(unittest.TestCase):
    """Test storage functionality"""
    
    def setUp(self):
        """Set up test environment"""
        if os.path.exists("file.json"):
            os.remove("file.json")
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("file.json"):
            os.remove("file.json")
    
    def test_all(self):
        """Test all method"""
        user = User(email="test@example.com")
        user.save()
        
        all_objects = storage.all()
        self.assertIn(f"User.{user.id}", all_objects)
    
    def test_all_with_class(self):
        """Test all method with class filter"""
        user = User(email="test@example.com")
        state = State(name="Test State")
        user.save()
        state.save()
        
        users = storage.all(User)
        states = storage.all(State)
        
        self.assertEqual(len(users), 1)
        self.assertEqual(len(states), 1)
        self.assertIn(f"User.{user.id}", users)
        self.assertIn(f"State.{state.id}", states)
    
    def test_new_and_save(self):
        """Test new and save methods"""
        user = User(email="test@example.com")
        storage.new(user)
        storage.save()
        
        # Check file was created
        self.assertTrue(os.path.exists("file.json"))
        
        # Check content
        with open("file.json", 'r') as f:
            data = json.load(f)
        
        self.assertIn(f"User.{user.id}", data)
    
    def test_reload(self):
        """Test reload method"""
        user = User(email="test@example.com", first_name="Test")
        user.save()
        
        # Clear storage and reload
        storage._FileStorage__objects = {}
        storage.reload()
        
        # Check object was reloaded
        reloaded_users = storage.all(User)
        self.assertEqual(len(reloaded_users), 1)
        
        reloaded_user = list(reloaded_users.values())[0]
        self.assertEqual(reloaded_user.email, "test@example.com")
        self.assertEqual(reloaded_user.first_name, "Test")

if __name__ == '__main__':
    unittest.main()
```

#### Console Testing
```python
#!/usr/bin/env python3
"""Unit tests for console"""

import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.user import User
from models.state import State

class TestConsole(unittest.TestCase):
    """Test console functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        if os.path.exists("file.json"):
            os.remove("file.json")
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("file.json"):
            os.remove("file.json")
    
    def create_user(self):
        """Helper method to create a user"""
        user = User(email="test@example.com", first_name="Test")
        user.save()
        return user
    
    def test_help(self):
        """Test help command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help")
        
        output = f.getvalue()
        self.assertIn("Documented commands", output)
    
    def test_create_user(self):
        """Test create command for User"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create User email="test@example.com" first_name="Test"')
        
        output = f.getvalue().strip()
        self.assertTrue(len(output) > 0)  # Should print object ID
        
        # Verify object was created
        users = storage.all(User)
        self.assertEqual(len(users), 1)
    
    def test_create_invalid_class(self):
        """Test create command with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create InvalidClass")
        
        output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")
    
    def test_show_user(self):
        """Test show command"""
        user = self.create_user()
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show User {user.id}")
        
        output = f.getvalue().strip()
        self.assertIn(user.id, output)
        self.assertIn("test@example.com", output)
    
    def test_show_invalid_id(self):
        """Test show command with invalid ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show User invalid-id")
        
        output = f.getvalue().strip()
        self.assertEqual(output, "** no instance found **")
    
    def test_all_users(self):
        """Test all command"""
        user1 = User(email="user1@example.com")
        user2 = User(email="user2@example.com")
        user1.save()
        user2.save()
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
        
        output = f.getvalue().strip()
        self.assertIn(user1.id, output)
        self.assertIn(user2.id, output)
    
    def test_count(self):
        """Test count command"""
        user1 = User(email="user1@example.com")
        user2 = User(email="user2@example.com")
        user1.save()
        user2.save()
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("count User")
        
        output = f.getvalue().strip()
        self.assertEqual(output, "2")
    
    def test_update(self):
        """Test update command"""
        user = self.create_user()
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'update User {user.id} first_name "Updated"')
        
        # Verify update
        updated_user = storage.all(User)[f"User.{user.id}"]
        self.assertEqual(updated_user.first_name, "Updated")
    
    def test_destroy(self):
        """Test destroy command"""
        user = self.create_user()
        user_id = user.id
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"destroy User {user_id}")
        
        # Verify deletion
        users = storage.all(User)
        self.assertNotIn(f"User.{user_id}", users)
    
    def test_alternative_syntax(self):
        """Test alternative command syntax"""
        user1 = User(email="user1@example.com")
        user2 = User(email="user2@example.com")
        user1.save()
        user2.save()
        
        # Test User.all()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.all()")
        
        output = f.getvalue().strip()
        self.assertIn(user1.id, output)
        self.assertIn(user2.id, output)
        
        # Test User.count()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.count()")
        
        output = f.getvalue().strip()
        self.assertEqual(output, "2")

if __name__ == '__main__':
    unittest.main()
```

This comprehensive documentation provides detailed examples for every aspect of the AirBnB Clone project, from basic model usage to advanced deployment scenarios. Each example includes practical code that can be run and modified to suit specific needs.