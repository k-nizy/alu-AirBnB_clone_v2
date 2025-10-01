# AirBnB Clone - Deployment Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [Database Configuration](#database-configuration)
5. [Application Deployment](#application-deployment)
6. [Web Server Configuration](#web-server-configuration)
7. [Static Files Deployment](#static-files-deployment)
8. [Automated Deployment](#automated-deployment)
9. [Monitoring and Maintenance](#monitoring-and-maintenance)
10. [Troubleshooting](#troubleshooting)

## Overview

This guide covers the complete deployment process for the AirBnB Clone application, including:

- Setting up production servers
- Configuring databases (MySQL)
- Deploying the Python application
- Setting up web servers (Nginx)
- Managing static files
- Implementing automated deployment with Fabric
- Monitoring and maintenance procedures

### Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Web Server    │    │    Database     │
│     (Nginx)     │◄──►│    (Flask)      │◄──►│    (MySQL)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Static Files   │    │  Application    │    │   Data Storage  │
│   (/static/)    │    │    Code         │    │   (Persistent)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

### System Requirements

#### Minimum Server Specifications
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Ubuntu 20.04 LTS or later
- **Network**: Public IP address

#### Software Dependencies
- Python 3.8+
- MySQL 8.0+
- Nginx 1.18+
- Git
- Fabric3 (for deployment automation)

### Development Environment
```bash
# Install required packages locally
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git mysql-server nginx

# Install Python dependencies
pip3 install fabric3 flask sqlalchemy mysqlclient
```

## Environment Setup

### Server Preparation

#### 1. Initial Server Setup
```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Create application user
sudo adduser hbnb
sudo usermod -aG sudo hbnb

# Set up SSH key authentication
sudo mkdir -p /home/hbnb/.ssh
sudo cp ~/.ssh/authorized_keys /home/hbnb/.ssh/
sudo chown -R hbnb:hbnb /home/hbnb/.ssh
sudo chmod 700 /home/hbnb/.ssh
sudo chmod 600 /home/hbnb/.ssh/authorized_keys
```

#### 2. Install System Dependencies
```bash
# Install Python and development tools
sudo apt-get install -y python3 python3-pip python3-dev python3-venv
sudo apt-get install -y build-essential libssl-dev libffi-dev
sudo apt-get install -y git curl wget

# Install MySQL
sudo apt-get install -y mysql-server mysql-client
sudo apt-get install -y libmysqlclient-dev

# Install Nginx
sudo apt-get install -y nginx

# Install additional tools
sudo apt-get install -y htop tree vim
```

#### 3. Configure Firewall
```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH, HTTP, and HTTPS
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 3306  # MySQL (only if database is on separate server)

# Check status
sudo ufw status
```

### Directory Structure Setup

#### Create Application Directories
```bash
# Create main application directory
sudo mkdir -p /data/hbnb_app
sudo mkdir -p /data/web_static/releases
sudo mkdir -p /data/web_static/shared
sudo mkdir -p /data/logs

# Set ownership
sudo chown -R hbnb:hbnb /data

# Create symbolic link for current release
sudo ln -sf /data/web_static/releases/current /data/web_static/current
```

#### Directory Structure
```
/data/
├── hbnb_app/                 # Application code
│   ├── models/
│   ├── web_flask/
│   ├── console.py
│   ├── requirements.txt
│   └── config/
├── web_static/               # Static files
│   ├── releases/
│   │   ├── web_static_20231201120000/
│   │   └── web_static_20231201130000/
│   ├── shared/
│   └── current -> releases/web_static_20231201130000/
└── logs/                     # Application logs
    ├── hbnb.log
    ├── nginx_access.log
    └── nginx_error.log
```

## Database Configuration

### MySQL Setup

#### 1. Secure MySQL Installation
```bash
# Run MySQL secure installation
sudo mysql_secure_installation

# Follow prompts:
# - Set root password
# - Remove anonymous users
# - Disallow root login remotely
# - Remove test database
# - Reload privilege tables
```

#### 2. Create Database and User
```sql
-- Connect to MySQL as root
sudo mysql -u root -p

-- Create database
CREATE DATABASE hbnb_prod_db;

-- Create user
CREATE USER 'hbnb_prod'@'localhost' IDENTIFIED BY 'secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON hbnb_prod_db.* TO 'hbnb_prod'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_prod'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

#### 3. Database Configuration File
```bash
# Create MySQL configuration for application
sudo tee /data/hbnb_app/config/database.conf << EOF
[mysql]
host = localhost
port = 3306
database = hbnb_prod_db
username = hbnb_prod
password = secure_password_here
charset = utf8mb4
EOF

# Secure the configuration file
sudo chown hbnb:hbnb /data/hbnb_app/config/database.conf
sudo chmod 600 /data/hbnb_app/config/database.conf
```

#### 4. Test Database Connection
```bash
# Test connection
mysql -u hbnb_prod -p -h localhost hbnb_prod_db

# Run test query
SHOW TABLES;
SELECT VERSION();
EXIT;
```

### Database Backup Setup

#### Automated Backup Script
```bash
# Create backup script
sudo tee /usr/local/bin/backup_hbnb_db.sh << 'EOF'
#!/bin/bash

# Configuration
DB_NAME="hbnb_prod_db"
DB_USER="hbnb_prod"
DB_PASS="secure_password_here"
BACKUP_DIR="/data/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/hbnb_backup_$DATE.sql"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

# Remove backups older than 7 days
find $BACKUP_DIR -name "hbnb_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE.gz"
EOF

# Make script executable
sudo chmod +x /usr/local/bin/backup_hbnb_db.sh

# Add to crontab (daily backup at 2 AM)
sudo crontab -e
# Add line: 0 2 * * * /usr/local/bin/backup_hbnb_db.sh >> /data/logs/backup.log 2>&1
```

## Application Deployment

### Manual Deployment

#### 1. Clone Repository
```bash
# Switch to application user
sudo su - hbnb

# Clone repository
cd /data/hbnb_app
git clone https://github.com/your-username/AirBnB_clone.git .

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Application Configuration

##### Environment Variables
```bash
# Create environment file
tee /data/hbnb_app/.env << EOF
# Application settings
FLASK_APP=web_flask/100-hbnb.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Database settings
HBNB_TYPE_STORAGE=db
HBNB_MYSQL_USER=hbnb_prod
HBNB_MYSQL_PWD=secure_password_here
HBNB_MYSQL_HOST=localhost
HBNB_MYSQL_DB=hbnb_prod_db

# Logging
LOG_LEVEL=INFO
LOG_FILE=/data/logs/hbnb.log
EOF

# Secure environment file
chmod 600 /data/hbnb_app/.env
```

##### Application Configuration File
```python
# Create config.py
tee /data/hbnb_app/config.py << 'EOF'
#!/usr/bin/env python3
"""Application configuration"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Database
    HBNB_TYPE_STORAGE = os.environ.get('HBNB_TYPE_STORAGE', 'file')
    HBNB_MYSQL_USER = os.environ.get('HBNB_MYSQL_USER')
    HBNB_MYSQL_PWD = os.environ.get('HBNB_MYSQL_PWD')
    HBNB_MYSQL_HOST = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
    HBNB_MYSQL_DB = os.environ.get('HBNB_MYSQL_DB')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', '/data/logs/hbnb.log')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    HBNB_TYPE_STORAGE = 'file'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
EOF
```

#### 3. Initialize Database
```bash
# Set environment variables
source /data/hbnb_app/.env

# Initialize database tables
cd /data/hbnb_app
python3 -c "
from models import storage
from models.base_model import Base
storage.reload()
print('Database initialized successfully')
"
```

#### 4. Test Application
```bash
# Test console
python3 console.py
# (hbnb) create User email="test@example.com" first_name="Test"
# (hbnb) all User
# (hbnb) quit

# Test web application
python3 web_flask/100-hbnb.py &
curl http://localhost:5000/
kill %1
```

### Systemd Service Configuration

#### 1. Create Service File
```bash
# Create systemd service
sudo tee /etc/systemd/system/hbnb.service << EOF
[Unit]
Description=HBNB Flask Application
After=network.target mysql.service
Requires=mysql.service

[Service]
Type=simple
User=hbnb
Group=hbnb
WorkingDirectory=/data/hbnb_app
Environment=PATH=/data/hbnb_app/venv/bin
EnvironmentFile=/data/hbnb_app/.env
ExecStart=/data/hbnb_app/venv/bin/python web_flask/100-hbnb.py
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=5

# Logging
StandardOutput=append:/data/logs/hbnb.log
StandardError=append:/data/logs/hbnb.log

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/data

[Install]
WantedBy=multi-user.target
EOF
```

#### 2. Enable and Start Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable hbnb

# Start service
sudo systemctl start hbnb

# Check status
sudo systemctl status hbnb

# View logs
sudo journalctl -u hbnb -f
```

## Web Server Configuration

### Nginx Setup

#### 1. Remove Default Configuration
```bash
# Remove default site
sudo rm /etc/nginx/sites-enabled/default
```

#### 2. Create Application Configuration
```bash
# Create Nginx configuration
sudo tee /etc/nginx/sites-available/hbnb << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Logging
    access_log /data/logs/nginx_access.log;
    error_log /data/logs/nginx_error.log;
    
    # Static files
    location /static/ {
        alias /data/web_static/current/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # API endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Main application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF
```

#### 3. Enable Configuration
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/hbnb /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Enable Nginx
sudo systemctl enable nginx
```

#### 4. SSL Configuration (Optional)
```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

### Load Balancer Configuration (Multiple Servers)

#### Nginx Load Balancer
```bash
# Create load balancer configuration
sudo tee /etc/nginx/sites-available/hbnb-lb << 'EOF'
upstream hbnb_backend {
    server 10.0.1.10:5000 weight=1 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:5000 weight=1 max_fails=3 fail_timeout=30s;
    
    # Health check
    keepalive 32;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Static files (served from load balancer)
    location /static/ {
        alias /data/web_static/current/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Application
    location / {
        proxy_pass http://hbnb_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Connection settings
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check
    location /health {
        access_log off;
        proxy_pass http://hbnb_backend/health;
    }
}
EOF
```

## Static Files Deployment

### Manual Static File Deployment

#### 1. Prepare Static Files
```bash
# Create static files archive
cd /path/to/local/project
tar -czf web_static.tar.gz web_static/

# Upload to server
scp web_static.tar.gz hbnb@your-server:/tmp/
```

#### 2. Deploy Static Files
```bash
# On server
cd /data/web_static/releases

# Create release directory
RELEASE_DIR="web_static_$(date +%Y%m%d%H%M%S)"
mkdir $RELEASE_DIR

# Extract files
tar -xzf /tmp/web_static.tar.gz -C $RELEASE_DIR

# Update symlink
rm -f /data/web_static/current
ln -s /data/web_static/releases/$RELEASE_DIR/web_static /data/web_static/current

# Clean up
rm /tmp/web_static.tar.gz

# Restart Nginx
sudo systemctl reload nginx
```

### Automated Static File Deployment Script

```bash
# Create deployment script
tee /usr/local/bin/deploy_static.sh << 'EOF'
#!/bin/bash

set -e

# Configuration
STATIC_SOURCE="/path/to/local/web_static"
REMOTE_USER="hbnb"
REMOTE_HOST="your-server.com"
REMOTE_PATH="/data/web_static"

# Create timestamp
TIMESTAMP=$(date +%Y%m%d%H%M%S)
RELEASE_NAME="web_static_$TIMESTAMP"
ARCHIVE_NAME="$RELEASE_NAME.tar.gz"

echo "Starting static file deployment..."

# Create local archive
echo "Creating archive..."
cd $(dirname $STATIC_SOURCE)
tar -czf /tmp/$ARCHIVE_NAME $(basename $STATIC_SOURCE)/

# Upload archive
echo "Uploading archive..."
scp /tmp/$ARCHIVE_NAME $REMOTE_USER@$REMOTE_HOST:/tmp/

# Deploy on remote server
echo "Deploying on remote server..."
ssh $REMOTE_USER@$REMOTE_HOST << REMOTE_SCRIPT
    set -e
    
    # Create release directory
    mkdir -p $REMOTE_PATH/releases/$RELEASE_NAME
    
    # Extract archive
    tar -xzf /tmp/$ARCHIVE_NAME -C $REMOTE_PATH/releases/$RELEASE_NAME
    
    # Update symlink
    rm -f $REMOTE_PATH/current
    ln -s $REMOTE_PATH/releases/$RELEASE_NAME/web_static $REMOTE_PATH/current
    
    # Clean up old releases (keep last 5)
    cd $REMOTE_PATH/releases
    ls -t | tail -n +6 | xargs rm -rf
    
    # Clean up archive
    rm /tmp/$ARCHIVE_NAME
    
    # Reload Nginx
    sudo systemctl reload nginx
    
    echo "Deployment completed: $RELEASE_NAME"
REMOTE_SCRIPT

# Clean up local archive
rm /tmp/$ARCHIVE_NAME

echo "Static file deployment completed successfully!"
EOF

# Make script executable
chmod +x /usr/local/bin/deploy_static.sh
```

## Automated Deployment

### Fabric Deployment Scripts

#### 1. Install Fabric
```bash
# Install Fabric locally
pip3 install fabric3
```

#### 2. Create Fabric Configuration
```python
# fabfile.py
from fabric.api import env, local, run, put, cd, sudo, settings
from fabric.contrib.files import exists
from datetime import datetime
import os

# Server configuration
env.hosts = ['your-server.com']
env.user = 'hbnb'
env.key_filename = '~/.ssh/id_rsa'

# Paths
env.app_path = '/data/hbnb_app'
env.static_path = '/data/web_static'
env.venv_path = '/data/hbnb_app/venv'

def deploy_app():
    """Deploy application code"""
    
    print("Deploying application...")
    
    # Create backup of current version
    with settings(warn_only=True):
        run(f'cp -r {env.app_path} {env.app_path}.backup.$(date +%Y%m%d%H%M%S)')
    
    # Update code from repository
    with cd(env.app_path):
        run('git pull origin main')
        
        # Update dependencies
        run(f'{env.venv_path}/bin/pip install -r requirements.txt')
        
        # Run database migrations if needed
        run(f'{env.venv_path}/bin/python -c "from models import storage; storage.reload()"')
    
    # Restart application
    sudo('systemctl restart hbnb')
    
    # Check if service is running
    with settings(warn_only=True):
        result = sudo('systemctl is-active hbnb')
        if result.return_code == 0:
            print("✓ Application deployed successfully")
        else:
            print("✗ Application deployment failed")
            return False
    
    return True

def deploy_static():
    """Deploy static files"""
    
    print("Deploying static files...")
    
    # Create archive
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tar.gz"
    
    local(f'tar -czf /tmp/{archive_name} web_static/')
    
    # Upload archive
    put(f'/tmp/{archive_name}', '/tmp/')
    
    # Deploy on server
    release_dir = f'{env.static_path}/releases/web_static_{timestamp}'
    run(f'mkdir -p {release_dir}')
    run(f'tar -xzf /tmp/{archive_name} -C {release_dir}')
    run(f'mv {release_dir}/web_static/* {release_dir}/')
    run(f'rm -rf {release_dir}/web_static')
    
    # Update symlink
    run(f'rm -f {env.static_path}/current')
    run(f'ln -s {release_dir} {env.static_path}/current')
    
    # Clean up
    run(f'rm /tmp/{archive_name}')
    local(f'rm /tmp/{archive_name}')
    
    # Reload Nginx
    sudo('systemctl reload nginx')
    
    print("✓ Static files deployed successfully")

def deploy():
    """Full deployment"""
    
    print("Starting full deployment...")
    
    # Deploy application
    if not deploy_app():
        print("Application deployment failed, aborting")
        return
    
    # Deploy static files
    deploy_static()
    
    # Run health check
    health_check()
    
    print("✓ Full deployment completed successfully")

def rollback():
    """Rollback to previous version"""
    
    print("Rolling back deployment...")
    
    # Find backup directories
    with cd(env.app_path):
        backups = run('ls -t *.backup.* 2>/dev/null || echo ""').split()
    
    if not backups:
        print("No backup found")
        return
    
    latest_backup = backups[0]
    
    # Stop application
    sudo('systemctl stop hbnb')
    
    # Restore backup
    run(f'rm -rf {env.app_path}.rollback')
    run(f'mv {env.app_path} {env.app_path}.rollback')
    run(f'mv {latest_backup} {env.app_path}')
    
    # Start application
    sudo('systemctl start hbnb')
    
    print(f"✓ Rolled back to {latest_backup}")

def health_check():
    """Check application health"""
    
    print("Running health check...")
    
    # Check systemd service
    with settings(warn_only=True):
        app_status = sudo('systemctl is-active hbnb')
        nginx_status = sudo('systemctl is-active nginx')
        mysql_status = sudo('systemctl is-active mysql')
    
    print(f"Application: {app_status}")
    print(f"Nginx: {nginx_status}")
    print(f"MySQL: {mysql_status}")
    
    # Check HTTP response
    with settings(warn_only=True):
        http_check = run('curl -s -o /dev/null -w "%{http_code}" http://localhost/')
        print(f"HTTP Status: {http_check}")
    
    # Check disk space
    disk_usage = run('df -h /data | tail -1')
    print(f"Disk usage: {disk_usage}")

def setup_server():
    """Initial server setup"""
    
    print("Setting up server...")
    
    # Update system
    sudo('apt-get update && apt-get upgrade -y')
    
    # Install dependencies
    sudo('apt-get install -y python3 python3-pip python3-venv git mysql-server nginx')
    
    # Create directories
    sudo('mkdir -p /data/hbnb_app /data/web_static/releases /data/logs')
    sudo('chown -R hbnb:hbnb /data')
    
    # Clone repository
    with cd('/data/hbnb_app'):
        run('git clone https://github.com/your-username/AirBnB_clone.git .')
        run('python3 -m venv venv')
        run('venv/bin/pip install -r requirements.txt')
    
    print("✓ Server setup completed")

# Usage:
# fab setup_server
# fab deploy
# fab health_check
# fab rollback
```

#### 3. Run Deployment
```bash
# Initial server setup
fab setup_server

# Deploy application
fab deploy

# Check health
fab health_check

# Rollback if needed
fab rollback
```

### CI/CD Pipeline (GitHub Actions)

#### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: hbnb_test_db
        options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Set up test environment
      run: |
        export HBNB_TYPE_STORAGE=db
        export HBNB_MYSQL_USER=root
        export HBNB_MYSQL_PWD=root
        export HBNB_MYSQL_HOST=127.0.0.1
        export HBNB_MYSQL_DB=hbnb_test_db
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v --cov=models --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install Fabric
      run: pip install fabric3
    
    - name: Deploy to production
      env:
        DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
        DEPLOY_USER: ${{ secrets.DEPLOY_USER }}
        DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
      run: |
        echo "$DEPLOY_KEY" > deploy_key
        chmod 600 deploy_key
        fab -H $DEPLOY_USER@$DEPLOY_HOST -i deploy_key deploy
```

## Monitoring and Maintenance

### Log Management

#### 1. Logrotate Configuration
```bash
# Create logrotate configuration
sudo tee /etc/logrotate.d/hbnb << EOF
/data/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 hbnb hbnb
    postrotate
        systemctl reload nginx
        systemctl reload hbnb
    endscript
}
EOF
```

#### 2. Log Monitoring Script
```bash
# Create log monitoring script
tee /usr/local/bin/monitor_logs.sh << 'EOF'
#!/bin/bash

LOG_FILE="/data/logs/hbnb.log"
ERROR_COUNT_THRESHOLD=10
ALERT_EMAIL="admin@example.com"

# Count errors in last hour
ERROR_COUNT=$(grep "ERROR" $LOG_FILE | grep "$(date '+%Y-%m-%d %H')" | wc -l)

if [ $ERROR_COUNT -gt $ERROR_COUNT_THRESHOLD ]; then
    echo "High error count detected: $ERROR_COUNT errors in the last hour" | \
    mail -s "HBNB Alert: High Error Count" $ALERT_EMAIL
fi

# Check disk space
DISK_USAGE=$(df /data | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Disk usage is at $DISK_USAGE%" | \
    mail -s "HBNB Alert: High Disk Usage" $ALERT_EMAIL
fi
EOF

chmod +x /usr/local/bin/monitor_logs.sh

# Add to crontab (run every hour)
echo "0 * * * * /usr/local/bin/monitor_logs.sh" | sudo crontab -
```

### Performance Monitoring

#### 1. System Monitoring Script
```bash
# Create system monitoring script
tee /usr/local/bin/system_monitor.sh << 'EOF'
#!/bin/bash

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
MONITOR_LOG="/data/logs/system_monitor.log"

# CPU usage
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')

# Memory usage
MEM_USAGE=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')

# Disk usage
DISK_USAGE=$(df /data | tail -1 | awk '{print $5}' | sed 's/%//')

# Active connections
CONNECTIONS=$(netstat -an | grep :5000 | grep ESTABLISHED | wc -l)

# Log metrics
echo "$TIMESTAMP,CPU:$CPU_USAGE%,MEM:$MEM_USAGE%,DISK:$DISK_USAGE%,CONN:$CONNECTIONS" >> $MONITOR_LOG

# Alert if thresholds exceeded
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "High CPU usage: $CPU_USAGE%" | mail -s "HBNB Alert: High CPU" admin@example.com
fi

if (( $(echo "$MEM_USAGE > 80" | bc -l) )); then
    echo "High memory usage: $MEM_USAGE%" | mail -s "HBNB Alert: High Memory" admin@example.com
fi
EOF

chmod +x /usr/local/bin/system_monitor.sh

# Run every 5 minutes
echo "*/5 * * * * /usr/local/bin/system_monitor.sh" | crontab -
```

### Database Maintenance

#### 1. Database Optimization Script
```bash
# Create database maintenance script
tee /usr/local/bin/db_maintenance.sh << 'EOF'
#!/bin/bash

DB_NAME="hbnb_prod_db"
DB_USER="hbnb_prod"
DB_PASS="secure_password_here"

echo "Starting database maintenance..."

# Optimize tables
mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "
OPTIMIZE TABLE users;
OPTIMIZE TABLE states;
OPTIMIZE TABLE cities;
OPTIMIZE TABLE places;
OPTIMIZE TABLE amenities;
OPTIMIZE TABLE reviews;
OPTIMIZE TABLE place_amenity;
"

# Update statistics
mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "
ANALYZE TABLE users;
ANALYZE TABLE states;
ANALYZE TABLE cities;
ANALYZE TABLE places;
ANALYZE TABLE amenities;
ANALYZE TABLE reviews;
ANALYZE TABLE place_amenity;
"

echo "Database maintenance completed"
EOF

chmod +x /usr/local/bin/db_maintenance.sh

# Run weekly on Sunday at 3 AM
echo "0 3 * * 0 /usr/local/bin/db_maintenance.sh >> /data/logs/db_maintenance.log 2>&1" | crontab -
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Application Won't Start

**Symptoms:**
- Service fails to start
- "Connection refused" errors
- Import errors in logs

**Diagnosis:**
```bash
# Check service status
sudo systemctl status hbnb

# Check logs
sudo journalctl -u hbnb -n 50

# Check Python environment
sudo -u hbnb /data/hbnb_app/venv/bin/python -c "import models; print('OK')"
```

**Solutions:**
```bash
# Fix permissions
sudo chown -R hbnb:hbnb /data/hbnb_app

# Reinstall dependencies
sudo -u hbnb /data/hbnb_app/venv/bin/pip install -r /data/hbnb_app/requirements.txt

# Check environment variables
sudo -u hbnb cat /data/hbnb_app/.env
```

#### 2. Database Connection Issues

**Symptoms:**
- "Can't connect to MySQL server"
- Authentication errors
- Timeout errors

**Diagnosis:**
```bash
# Test MySQL connection
mysql -u hbnb_prod -p -h localhost hbnb_prod_db

# Check MySQL status
sudo systemctl status mysql

# Check MySQL logs
sudo tail -f /var/log/mysql/error.log
```

**Solutions:**
```bash
# Restart MySQL
sudo systemctl restart mysql

# Reset user password
sudo mysql -u root -p
# > ALTER USER 'hbnb_prod'@'localhost' IDENTIFIED BY 'new_password';
# > FLUSH PRIVILEGES;

# Check firewall
sudo ufw status
```

#### 3. Nginx Configuration Issues

**Symptoms:**
- 502 Bad Gateway
- 404 Not Found for static files
- SSL certificate errors

**Diagnosis:**
```bash
# Test Nginx configuration
sudo nginx -t

# Check Nginx status
sudo systemctl status nginx

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

**Solutions:**
```bash
# Fix configuration
sudo nginx -t
sudo systemctl reload nginx

# Check upstream servers
curl -I http://localhost:5000

# Fix SSL certificate
sudo certbot renew
```

#### 4. Performance Issues

**Symptoms:**
- Slow response times
- High CPU/memory usage
- Database query timeouts

**Diagnosis:**
```bash
# Check system resources
htop
free -h
df -h

# Check database performance
mysql -u hbnb_prod -p -e "SHOW PROCESSLIST;"

# Check application logs
grep "slow" /data/logs/hbnb.log
```

**Solutions:**
```bash
# Optimize database
sudo /usr/local/bin/db_maintenance.sh

# Add database indexes
mysql -u hbnb_prod -p hbnb_prod_db -e "
CREATE INDEX idx_places_city_id ON places(city_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
"

# Scale application
# Add more application servers
# Implement caching (Redis)
```

### Emergency Procedures

#### 1. Emergency Rollback
```bash
# Quick rollback script
sudo tee /usr/local/bin/emergency_rollback.sh << 'EOF'
#!/bin/bash

echo "EMERGENCY ROLLBACK INITIATED"

# Stop current application
sudo systemctl stop hbnb

# Find latest backup
BACKUP=$(ls -t /data/hbnb_app.backup.* | head -1)

if [ -z "$BACKUP" ]; then
    echo "No backup found!"
    exit 1
fi

# Restore backup
mv /data/hbnb_app /data/hbnb_app.failed
mv $BACKUP /data/hbnb_app

# Start application
sudo systemctl start hbnb

# Check status
sleep 5
if sudo systemctl is-active hbnb > /dev/null; then
    echo "ROLLBACK SUCCESSFUL"
else
    echo "ROLLBACK FAILED"
    exit 1
fi
EOF

chmod +x /usr/local/bin/emergency_rollback.sh
```

#### 2. Database Recovery
```bash
# Database recovery script
sudo tee /usr/local/bin/db_recovery.sh << 'EOF'
#!/bin/bash

DB_NAME="hbnb_prod_db"
BACKUP_DIR="/data/backups/mysql"

echo "DATABASE RECOVERY INITIATED"

# Find latest backup
LATEST_BACKUP=$(ls -t $BACKUP_DIR/hbnb_backup_*.sql.gz | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "No database backup found!"
    exit 1
fi

# Stop application
sudo systemctl stop hbnb

# Restore database
echo "Restoring from: $LATEST_BACKUP"
gunzip -c $LATEST_BACKUP | mysql -u root -p $DB_NAME

# Start application
sudo systemctl start hbnb

echo "DATABASE RECOVERY COMPLETED"
EOF

chmod +x /usr/local/bin/db_recovery.sh
```

This comprehensive deployment guide covers all aspects of deploying the AirBnB Clone application in a production environment, from initial server setup to ongoing maintenance and troubleshooting procedures.