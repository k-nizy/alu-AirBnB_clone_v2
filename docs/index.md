---
title: AirBnB Clone – Project Documentation
---

# AirBnB Clone – Documentation

Welcome to the project documentation. This site covers public APIs, classes, storage engines, the interactive console, and web routes.

- See `models.md` for data models and their attributes/methods.
- See `storage.md` for storage engines (`FileStorage`, `DBStorage`).
- See `console.md` for CLI commands and examples.
- See `web_flask.md` for Flask routes and usage.

Quickstart

1. Set environment variables as needed for DB storage:
   - `HBNB_TYPE_STORAGE`, `HBNB_MYSQL_USER`, `HBNB_MYSQL_PWD`, `HBNB_MYSQL_HOST`, `HBNB_MYSQL_DB`, `HBNB_ENV`
2. Start the console:
   - `python3 console.py`
3. Start a Flask app example:
   - `python3 web_flask/4-number_route.py`

Project Layout

- `models/` – ORM base and data classes
- `models/engine/` – storage backends
- `console.py` – interactive CLI
- `web_flask/` – Flask route examples and templates

