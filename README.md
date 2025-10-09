# AirBnB Clone v2 - Full Stack Web Application

![AirBnB Clone](https://img.shields.io/badge/AirBnB-Clone-orange) ![Python](https://img.shields.io/badge/Python-3.7+-blue) ![Flask](https://img.shields.io/badge/Flask-2.0+-green) ![HTML/CSS/JS](https://img.shields.io/badge/HTML%2FCSS%2FJS-Static%20Files-yellow)

##  Overview

**AirBnB Clone v2** is a comprehensive full-stack web application that replicates the core functionality of Airbnb. Built with Python, Flask, HTML/CSS/JavaScript, and featuring automated deployment capabilities, this project demonstrates advanced web development concepts and DevOps practices.

## 

##  Learning Objectives

This project covers essential web development and deployment concepts:

-  **Backend Development**: Python classes, object-oriented programming, and API design
-  **Web Frameworks**: Flask application development and routing
-  **Frontend Development**: HTML/CSS templating and responsive design
-  **Database Management**: Data modeling, storage abstraction, and MySQL integration
-  **DevOps & Deployment**: Fabric automation, Docker containerization, and load balancing
-  **System Administration**: Nginx configuration, SSH setup, and server management

##  Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │───▶│    Nginx        │───▶│   Flask App     │
│                 │    │   (Load         │    │   (Python)      │
│  (HTML/CSS/JS)  │    │   Balancer)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Static Files  │    │   MySQL         │
                       │   (HTML/CSS/JS) │    │   Database      │
                       └─────────────────┘    └─────────────────┘
```

##  Project Structure

### Core Components

#### **1. Command Line Interface** (`console.py`)
- Interactive shell for managing AirBnB objects
- Supports CRUD operations for all models
- Command: `python3 console.py`

#### **2. Backend Models** (`models/`)
```
models/
├── base_model.py      # Base class for all models
├── user.py           # User model
├── state.py          # State model
├── city.py           # City model
├── amenity.py        # Amenity model
├── place.py          # Place (listing) model
├── review.py         # Review model
└── engine/           # Storage engine abstractions
```

#### **3. Web Application** (`web_flask/`)
Progressive Flask applications demonstrating:
- **Routes 0-10**: Basic routing and templating
- **Routes 100+**: Full AirBnB clone with database integration
- **Templates**: Jinja2 HTML templates
- **Static Files**: CSS, JavaScript, and images

#### **4. Static Frontend** (`web_static/`)
- Pure HTML/CSS/JavaScript implementation
- Multiple iterations showing progressive complexity
- Responsive design with modern CSS

### Deployment & Infrastructure

#### **5. Deployment Scripts**
- **`0-setup_web_static.sh`**: Server preparation script
- **`1-pack_web_static.py`**: Archive creation with Fabric
- **`2-do_deploy_web_static.py`**: Remote deployment script
- **`3-deploy_web_static.py`**: Complete deployment workflow

#### **6. Containerization**
- **`Dockerfile`**: Application container definition
- **`docker-compose.yml`**: Multi-container orchestration
- **`haproxy.cfg`**: Load balancer configuration

##  Quick Start

### Prerequisites
- Python 3.7+
- MySQL 5.7+
- Nginx
- Fabric (for deployment)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd alu-AirBnB_clone_v2
   ```

2. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up the database:**
   ```bash
   cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p
   ```

4. **Configure environment variables:**
   ```bash
   export HBNB_MYSQL_USER=hbnb_dev
   export HBNB_MYSQL_PWD=hbnb_dev_pwd
   export HBNB_MYSQL_HOST=localhost
   export HBNB_MYSQL_DB=hbnb_dev_db
   export HBNB_TYPE_STORAGE=db
   ```

##  Usage

### Command Line Interface
```bash
# Start the interactive console
python3 console.py

# Create a new user
(hbnb) create User

# List all states
(hbnb) all State

# Show a specific place
(hbnb) show Place <id>
```

### Web Application
```bash
# Run the Flask application
python3 web_flask/100-hbnb.py

# Access at http://localhost:5000
```

### Static Files
```bash
# Serve static HTML files
cd web_static
python3 -m http.server 8000

# Access at http://localhost:8000/0-index.html
```

##  Deployment

### Automated Deployment with Fabric
```bash
# Create archive
fab -f 1-pack_web_static.py do_pack

# Deploy to servers
fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions/web_static_YYYYMMDDHHMMSS.tgz -i ssh_key -u ubuntu

# Full deployment (pack + deploy)
fab -f 3-deploy_web_static.py deploy -i ssh_key -u ubuntu
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

##  Database Models

| Model | Description | Key Attributes |
|-------|-------------|----------------|
| **User** | System users | email, password, first_name, last_name |
| **State** | States/Provinces | name |
| **City** | Cities | name, state_id |
| **Amenity** | Place amenities | name |
| **Place** | Rental listings | name, description, price, location |
| **Review** | User reviews | text, rating |

##  API Endpoints

### Flask Application Routes
- `/` - Home page
- `/hbnb` - States list
- `/states` - States page
- `/states/<id>` - State detail
- `/amenities/<id>` - Amenity detail
- `/places` - Places search
- `/places/<id>` - Place detail

##  Testing

```bash
# Run unit tests
python3 -m unittest discover tests/

# Run specific test file
python3 -m unittest tests/test_models/test_user.py

# Check PEP8 compliance
python3 -m pycodestyle models/
python3 -m pycodestyle web_flask/
```

##  Features

### Backend Features
-  Object-Relational Mapping (ORM)
-  Data validation and serialization
-  File-based and database storage engines
-  RESTful API design patterns

### Frontend Features
-  Responsive HTML/CSS design
-  Interactive JavaScript components
-  Dynamic content loading
-  Form handling and validation

### DevOps Features
-  Automated deployment pipelines
-  Container orchestration
-  Load balancing and scaling
-  Infrastructure as Code

##  Security Considerations

- Password hashing for user authentication
- Input validation and sanitization
- SQL injection prevention
- XSS protection measures
- Secure file upload handling

##  Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Install missing dependencies
pip3 install flask sqlalchemy mysqlclient
```

**Database Connection Issues:**
```bash
# Check MySQL service
sudo service mysql start

# Verify credentials
mysql -hlocalhost -uroot -p
```

**Fabric Deployment Issues:**
```bash
# Check SSH connectivity
ssh -i key_file ubuntu@server_ip

# Verify server setup
fab -f 0-setup_web_static.sh setup
```

##  Additional Resources

- [Python Documentation](https://docs.python.org/3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Fabric Documentation](http://www.fabfile.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)



