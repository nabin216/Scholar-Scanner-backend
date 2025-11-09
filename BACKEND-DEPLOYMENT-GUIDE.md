# 🚀 Django Backend Deployment Guide - Complete Setup

## 📋 Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [AWS EC2 Deployment (Free Tier)](#aws-ec2-deployment-free-tier)
3. [Render Deployment (Free Tier)](#render-deployment-free-tier)
4. [Environment Configuration](#environment-configuration)
5. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Development Setup

### Prerequisites
- Python 3.8+ installed
- Git installed
- Code editor (VS Code recommended)

### Step-by-Step Setup

#### 1. Clone and Navigate
```powershell
cd D:\ScholarshipPortal\scholarship-backend
```

#### 2. Create Virtual Environment
```powershell
# Create venv
py -m venv .venv

# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source .venv/bin/activate
```

#### 3. Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Create `.env` File (Optional for Local)
Create `D:\ScholarshipPortal\scholarship-backend\.env`:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
FRONTEND_URL=http://localhost:3000
```

Generate SECRET_KEY:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 5. Run Migrations
```powershell
python manage.py migrate
```

#### 6. Create Superuser (Admin)
```powershell
python manage.py createsuperuser
# Enter email, password when prompted
```

#### 7. Collect Static Files
```powershell
python manage.py collectstatic --noinput
```

#### 8. Start Development Server
```powershell
python manage.py runserver
```

**Server running at:**
- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

#### 9. Test API Endpoints
Open browser or use curl:
```powershell
# Test API root
curl http://127.0.0.1:8000/api/

# Test scholarships endpoint
curl http://127.0.0.1:8000/api/scholarships/
```

---

## ☁️ AWS EC2 Deployment (Free Tier)

### Part 1: Create EC2 Instance

#### 1.1 Launch Instance
1. Log into [AWS Console](https://console.aws.amazon.com/)
2. Navigate to **EC2 Dashboard**
3. Click **"Launch Instance"**
4. Configure:
   - **Name**: `scholarship-backend`
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance Type**: `t2.micro` (1 vCPU, 1GB RAM)
   - **Key Pair**: Create new or select existing
     - Download `.pem` file and save securely
   - **Storage**: 8-30 GB gp3

#### 1.2 Configure Security Group
Create/select security group with these **Inbound Rules**:

| Type  | Protocol | Port | Source          | Description       |
|-------|----------|------|-----------------|-------------------|
| SSH   | TCP      | 22   | My IP           | SSH access        |
| HTTP  | TCP      | 80   | 0.0.0.0/0       | Public HTTP       |
| HTTPS | TCP      | 443  | 0.0.0.0/0       | Public HTTPS      |
| Custom| TCP      | 8000 | 0.0.0.0/0       | Django (dev only) |

#### 1.3 Allocate Elastic IP (Recommended)
1. **EC2 → Elastic IPs → Allocate**
2. **Associate** with your instance
3. **Note the IP** for later use

### Part 2: Connect to EC2

#### Windows (PowerShell)
```powershell
# Set permissions on .pem file
icacls "scholarship-backend.pem" /inheritance:r
icacls "scholarship-backend.pem" /grant:r "$($env:USERNAME):(R)"

# Connect
ssh -i "scholarship-backend.pem" ubuntu@YOUR_EC2_IP
```

#### Linux/Mac
```bash
chmod 400 scholarship-backend.pem
ssh -i scholarship-backend.pem ubuntu@YOUR_EC2_IP
```

### Part 3: Deploy on EC2

#### 3.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
```

#### 3.2 Install System Dependencies
```bash
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    git \
    postgresql-client \
    libpq-dev \
    supervisor
```

#### 3.3 Clone Repository
```bash
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/scholarship-portal.git
cd scholarship-portal/scholarship-backend
```

#### 3.4 Setup Python Environment
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3.5 Configure Environment
Create `/home/ubuntu/scholarship-portal/scholarship-backend/.env`:
```bash
nano .env
```

Add:
```env
# Django Core
SECRET_KEY=generate-a-new-secret-key-here
DEBUG=False
ALLOWED_HOSTS=YOUR_EC2_IP,your-domain.com

# Database (SQLite by default, or PostgreSQL)
# DATABASE_URL=postgres://user:pass@localhost:5432/scholarships

# CORS - Add your frontend URL
CORS_ALLOWED_ORIGINS=https://nabin216.github.io,https://nabin216.github.io/scholarship-portal
FRONTEND_URL=https://nabin216.github.io/scholarship-portal

# Security
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
CSRF_TRUSTED_ORIGINS=http://YOUR_EC2_IP

# AWS SES Email (Optional)
AWS_SES_REGION=eu-north-1
AWS_SES_FROM_EMAIL=your-email@example.com
# AWS_SES_SMTP_USERNAME=your-smtp-username
# AWS_SES_SMTP_PASSWORD=your-smtp-password

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080
```

Generate SECRET_KEY:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 3.6 Run Django Setup
```bash
# Create necessary directories
mkdir -p logs staticfiles media

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

#### 3.7 Setup Gunicorn Service
Create `/etc/systemd/system/scholarship-backend.service`:
```bash
sudo nano /etc/systemd/system/scholarship-backend.service
```

Add:
```ini
[Unit]
Description=Scholarship Portal Django Backend
After=network.target

[Service]
Type=notify
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/scholarship-portal/scholarship-backend
Environment="PATH=/home/ubuntu/scholarship-portal/scholarship-backend/.venv/bin"
EnvironmentFile=/home/ubuntu/scholarship-portal/scholarship-backend/.env
ExecStart=/home/ubuntu/scholarship-portal/scholarship-backend/.venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/ubuntu/scholarship-portal/scholarship-backend/gunicorn.sock \
    --timeout 120 \
    --access-logfile /home/ubuntu/scholarship-portal/scholarship-backend/logs/gunicorn-access.log \
    --error-logfile /home/ubuntu/scholarship-portal/scholarship-backend/logs/gunicorn-error.log \
    scholarships_api.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable scholarship-backend
sudo systemctl start scholarship-backend
sudo systemctl status scholarship-backend
```

#### 3.8 Setup Nginx
Create `/etc/nginx/sites-available/scholarship-backend`:
```bash
sudo nano /etc/nginx/sites-available/scholarship-backend
```

Add:
```nginx
server {
    listen 80;
    server_name YOUR_EC2_IP your-domain.com;

    client_max_body_size 20M;

    # Static files
    location /static/ {
        alias /home/ubuntu/scholarship-portal/scholarship-backend/staticfiles/;
        expires 30d;
    }

    # Media files
    location /media/ {
        alias /home/ubuntu/scholarship-portal/scholarship-backend/media/;
        expires 7d;
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://unix:/home/ubuntu/scholarship-portal/scholarship-backend/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/scholarship-backend /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

#### 3.9 Set Permissions
```bash
sudo chown -R ubuntu:www-data /home/ubuntu/scholarship-portal/scholarship-backend
sudo chmod -R 755 /home/ubuntu/scholarship-portal/scholarship-backend
```

#### 3.10 Test Deployment
```bash
# Check services
sudo systemctl status scholarship-backend
sudo systemctl status nginx

# View logs
sudo tail -f /home/ubuntu/scholarship-portal/scholarship-backend/logs/gunicorn-error.log
```

Visit: `http://YOUR_EC2_IP/admin/`

### Part 4: Setup HTTPS (Optional)

#### 4.1 Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

#### 4.2 Get SSL Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### 4.3 Update .env for HTTPS
```bash
nano /home/ubuntu/scholarship-portal/scholarship-backend/.env
```

Update:
```env
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://your-domain.com
```

Restart:
```bash
sudo systemctl restart scholarship-backend
sudo systemctl restart nginx
```

---

## 🌐 Render Deployment (Free Tier)

### Prerequisites
- GitHub repository
- Render account (free)

### Step 1: Prepare Repository

Ensure `render.yaml` exists at repo root:
```yaml
services:
  - type: web
    name: scholarship-backend
    env: python
    plan: free
    rootDir: scholarship-backend
    buildCommand: "pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput"
    startCommand: "gunicorn scholarships_api.wsgi:application --bind 0.0.0.0:$PORT --workers=3"
    autoDeploy: true
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "False"
      - key: ALLOWED_HOSTS
        value: "scholarship-backend.onrender.com"
      - key: CORS_ALLOWED_ORIGINS
        value: "https://nabin216.github.io"
      - key: FRONTEND_URL
        value: "https://nabin216.github.io/scholarship-portal"

databases:
  - name: scholarship-db
    plan: free
    region: ohio
```

### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. **Connect GitHub** repository
4. Render will detect `render.yaml`
5. Click **"Apply"**
6. Wait for deployment (5-10 minutes)

### Step 3: Configure Environment

In Render Dashboard → Service → Environment:
- Add any additional env vars (AWS SES, etc.)
- DATABASE_URL is auto-generated

### Step 4: Run Migrations (if needed)

In Render Dashboard → Service → Shell:
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 🔧 Environment Configuration

### Required Environment Variables

```env
# Core Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-ec2-ip

# Database (optional - defaults to SQLite)
DATABASE_URL=postgres://user:pass@host:5432/dbname

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-url.com
FRONTEND_URL=https://your-frontend-url.com

# Security (production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://your-domain.com

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# AWS SES (optional - for email)
AWS_SES_REGION=eu-north-1
AWS_SES_FROM_EMAIL=noreply@yourdomain.com
AWS_SES_SMTP_USERNAME=your-smtp-username
AWS_SES_SMTP_PASSWORD=your-smtp-password
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

### Generate Secure Keys

```bash
# SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# JWT_SECRET_KEY (if different from SECRET_KEY)
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Error / Module Not Found
**Problem**: `ModuleNotFoundError: No module named 'X'`

**Solution**:
```bash
pip install -r requirements.txt
# Or install specific package
pip install package-name
```

#### 2. Database Migration Errors
**Problem**: `django.db.utils.OperationalError`

**Solution**:
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

#### 3. Static Files Not Loading
**Problem**: CSS/JS 404 errors

**Solution**:
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx  # If using Nginx
```

#### 4. Permission Denied
**Problem**: Can't write to files/directories

**Solution**:
```bash
sudo chown -R ubuntu:www-data /path/to/app
sudo chmod -R 755 /path/to/app
sudo chmod 775 /path/to/app/media
```

#### 5. 502 Bad Gateway (Nginx)
**Problem**: Nginx can't connect to backend

**Solution**:
```bash
# Check Gunicorn is running
sudo systemctl status scholarship-backend

# Check socket exists
ls -l /path/to/gunicorn.sock

# View logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /path/to/logs/gunicorn-error.log

# Restart services
sudo systemctl restart scholarship-backend
sudo systemctl restart nginx
```

#### 6. WSGI Application Error
**Problem**: `ImproperlyConfigured: WSGI application could not be loaded`

**Solution**:
```bash
# Ensure you're in the correct directory
cd /path/to/scholarship-backend

# Test import manually
python -c "import scholarships_api.wsgi"

# Check DJANGO_SETTINGS_MODULE
echo $DJANGO_SETTINGS_MODULE

# Verify wsgi.py exists
ls scholarships_api/wsgi.py
```

### Useful Commands

#### Service Management
```bash
# Restart backend
sudo systemctl restart scholarship-backend

# View logs
sudo journalctl -u scholarship-backend -f
sudo tail -f logs/gunicorn-error.log

# Check status
sudo systemctl status scholarship-backend
sudo systemctl status nginx
```

#### Django Management
```bash
# Activate venv first
source .venv/bin/activate

# Database
python manage.py migrate
python manage.py dbshell
python manage.py showmigrations

# Users
python manage.py createsuperuser
python manage.py changepassword username

# Static files
python manage.py collectstatic --noinput

# Shell
python manage.py shell
```

#### System Monitoring
```bash
# Disk space
df -h

# Memory usage
free -m

# Running processes
ps aux | grep gunicorn
ps aux | grep nginx

# Network connections
sudo netstat -tulpn | grep LISTEN
```

---

## 📊 Architecture Overview

### Local Development
```
Browser → Django Dev Server (8000) → SQLite
```

### Production (EC2)
```
Browser → Nginx (80/443) → Gunicorn → Django → PostgreSQL/SQLite
```

### Production (Render)
```
Browser → Render Edge → Gunicorn → Django → PostgreSQL
```

---

## 🔐 Security Checklist

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS with SSL certificate
- [ ] Enable SECURE_SSL_REDIRECT
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Set CSRF_COOKIE_SECURE=True
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Configure CORS_ALLOWED_ORIGINS
- [ ] Use strong database passwords
- [ ] Keep dependencies updated
- [ ] Regular backups of database
- [ ] Monitor logs for suspicious activity
- [ ] Use environment variables for secrets
- [ ] Restrict SSH access (EC2 security group)

---

## 📚 Additional Resources

- [Django Deployment Docs](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Render Documentation](https://render.com/docs)

---

## 🎯 Quick Reference

### Local Development
```bash
cd scholarship-backend
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac
python manage.py runserver
```

### EC2 Update Deployment
```bash
cd /home/ubuntu/scholarship-portal
git pull origin main
source scholarship-backend/.venv/bin/activate
pip install -r scholarship-backend/requirements.txt
python scholarship-backend/manage.py migrate
python scholarship-backend/manage.py collectstatic --noinput
sudo systemctl restart scholarship-backend
```

### View Logs
```bash
# EC2
sudo tail -f /home/ubuntu/scholarship-portal/scholarship-backend/logs/gunicorn-error.log

# Render
# Use Render Dashboard → Logs
```

---

**✨ Your Django backend is now ready for deployment! Choose EC2 for full control or Render for simplicity.**
