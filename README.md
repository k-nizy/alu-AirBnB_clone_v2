# AirBnB Clone - MySQL, Deployment & Web Framework

## Project Description

This project is a complete web application that integrates database storage, backend API, and server-side rendering. It's part of a comprehensive full-stack development curriculum, focusing on building an AirBnB clone with MySQL database integration, deployment automation, and a Flask web framework.

This repository covers:
- **Part 3**: MySQL Database Integration
- **Part 4**: Web Static Deployment
- **Part 5**: Web Framework (Flask)

##  Learning Objectives

- Implement Object-Relational Mapping (ORM) with SQLAlchemy
- Manage MySQL databases for development and testing environments
- Deploy static content to remote servers using Fabric
- Build dynamic web pages with Flask and Jinja2 templates
- Understand the difference between file-based and database storage
- Master Python packaging and module organization

##  Technologies & Tools

- **Language**: Python 3.8+
- **Web Framework**: Flask
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy 1.4.x
- **Deployment**: Fabric3, Nginx
- **Testing**: unittest
- **Style**: PEP 8 (pycodestyle)

##  Project Structure

```
.
├── models/                    # Data models and storage engines
│   ├── engine/
│   │   ├── file_storage.py   # File-based storage
│   │   └── db_storage.py     # MySQL database storage
│   ├── base_model.py         # Base class for all models
│   ├── user.py               # User model
│   ├── state.py              # State model
│   ├── city.py               # City model
│   ├── place.py              # Place model
│   ├── amenity.py            # Amenity model
│   └── review.py             # Review model
├── web_flask/                # Flask web application
│   ├── templates/            # Jinja2 HTML templates
│   └── static/               # CSS, images, JavaScript
├── web_static/               # Static HTML/CSS files
├── tests/                    # Unit tests
├── console.py                # Command-line interface
├── setup_mysql_dev.sql       # Development database setup
├── setup_mysql_test.sql      # Test database setup
├── 0-setup_web_static.sh     # Web server setup script
├── 1-pack_web_static.py      # Create deployment archive
├── 2-do_deploy_web_static.py # Deploy archive to servers
└── 3-deploy_web_static.py    # Full deployment pipeline
```

##  Database Schema

The application uses a relational database with the following models:

- **User**: User information (email, password, first_name, last_name)
- **State**: State/region information
- **City**: City information (linked to State)
- **Place**: Property listings (linked to City and User)
- **Amenity**: Property amenities
- **Review**: User reviews (linked to Place and User)

##  Getting Started

### Prerequisites

```bash
# Python 3.8+
python3 --version

# MySQL 8.0
mysql --version

# Install Python dependencies
pip3 install -r requirements.txt
```

### Database Setup

1. **Create MySQL databases**:
```bash
cat setup_mysql_dev.sql | mysql -uroot -p
cat setup_mysql_test.sql | mysql -uroot -p
```

2. **Set environment variables**:
```bash
export HBNB_MYSQL_USER=hbnb_dev
export HBNB_MYSQL_PWD=hbnb_dev_pwd
export HBNB_MYSQL_HOST=localhost
export HBNB_MYSQL_DB=hbnb_dev_db
export HBNB_TYPE_STORAGE=db
```

### Running the Console

```bash
# File storage mode
./console.py

# Database storage mode
HBNB_TYPE_STORAGE=db ./console.py
```

### Running the Flask Application

```bash
# Start development server
python3 -m web_flask.0-hello_route

# Access at http://0.0.0.0:5000/
```

##  Testing

Run the test suite:

```bash
# All tests
python3 -m unittest discover tests

# Specific test file
python3 -m unittest tests/test_models/test_base_model.py

# With environment variables for database tests
HBNB_ENV=test HBNB_TYPE_STORAGE=db python3 -m unittest discover tests
```

##  Deployment

Deploy static content to production servers:

```bash
# Pack web static files
python3 1-pack_web_static.py

# Deploy to servers
python3 3-deploy_web_static.py
```

##  Console Commands

The command-line interface supports:

- `create <class>`: Create a new instance
- `show <class> <id>`: Display an instance
- `destroy <class> <id>`: Delete an instance
- `all [class]`: Display all instances
- `update <class> <id> <attribute> <value>`: Update an instance
- `quit` or `EOF`: Exit the console

### Example Usage

```bash
(hbnb) create State name="California"
(hbnb) create City state_id="state-id" name="San Francisco"
(hbnb) all State
(hbnb) update User user-id email "newemail@example.com"
```

##  Configuration

Toggle between storage engines using environment variables:

- **File Storage**: Default mode, stores data in JSON file
- **Database Storage**: Set `HBNB_TYPE_STORAGE=db` for MySQL

##  Key Features

 Dual storage system (File & Database)  
 SQLAlchemy ORM integration  
 RESTful routing with Flask  
 Jinja2 templating engine  
 Automated deployment scripts  
 Comprehensive unit testing  
 PEP 8 compliant code  

##  Contributing

This is an educational project. For contributions:

1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Ensure all tests pass
5. Submit a pull request


##  Author

**Kevin Nizeyimana**
- GitHub: [@k-nizy](https://github.com/k-nizy)
  
