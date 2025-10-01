# Models

This project defines ORM-backed models inheriting from `models.base_model.BaseModel` and mapped with SQLAlchemy `Base`.

## BaseModel
- Module: `models/base_model.py`
- Columns: `id: String(60)`, `created_at: DateTime`, `updated_at: DateTime`
- Methods: `__init__`, `__str__`, `save`, `to_dict`, `delete`

Example
```python
from models.base_model import BaseModel
obj = BaseModel(); obj.save()
print(obj.id); print(obj.to_dict())
```

## User
- Module: `models/user.py`
- Inherits: `BaseModel`, `Base`
- Table: `users`
- Columns: `email`, `password`, `first_name`, `last_name`
- Relationships: `places`, `reviews`

## State
- Module: `models/state.py`
- Table: `states`
- DB columns: `name`; DB relationship: `cities`
- File backend: `cities` property lists related `City`

## City
- Module: `models/city.py`
- Table: `cities`
- DB columns: `name`, `state_id` FK `states.id`
- DB relationship: `places`

## Amenity
- Module: `models/amenity.py`
- Table: `amenities`
- Columns: `name`
- Relationship: `place_amenities` (many-to-many via `place_amenity`)

## Place
- Module: `models/place.py`
- Table: `places`
- Columns: `city_id`, `user_id`, `name`, `description`, `number_rooms`, `number_bathrooms`, `max_guest`, `price_by_night`, `latitude`, `longitude`
- DB relationships: `reviews`, `amenities`

## Review
- Module: `models/review.py`
- Table: `reviews`
- Columns: `text`, `place_id`, `user_id`

Create instances via console
```bash
$ python3 console.py
(hbnb) create User email="me@example.com" password="pass123"
(hbnb) all User
```