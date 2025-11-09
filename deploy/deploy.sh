#!/bin/bash
# EC2 Deployment Script for Scholarship Portal Django Backend
# Run this on your EC2 instance after initial setup

set -e  # Exit on error

echo "=========================================="
echo "Scholarship Portal Backend - EC2 Deploy"
echo "=========================================="

# Configuration
APP_DIR="/home/ubuntu/scholarship-backend"
VENV_DIR="$APP_DIR/.venv"
REPO_URL="https://github.com/nabin216/scholarship-portal.git"  # Update with your repo
BRANCH="main"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}[1/8]${NC} Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

echo -e "${GREEN}[2/8]${NC} Installing system dependencies..."
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    git \
    postgresql-client \
    libpq-dev \
    supervisor \
    certbot \
    python3-certbot-nginx

echo -e "${GREEN}[3/8]${NC} Cloning/updating repository..."
if [ -d "$APP_DIR" ]; then
    echo "Directory exists, pulling latest..."
    cd $APP_DIR
    git pull origin $BRANCH
else
    echo "Cloning repository..."
    git clone -b $BRANCH $REPO_URL $APP_DIR
    cd $APP_DIR/scholarship-backend
fi

echo -e "${GREEN}[4/8]${NC} Creating virtual environment..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

echo -e "${GREEN}[5/8]${NC} Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}[6/8]${NC} Creating necessary directories..."
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/staticfiles
mkdir -p $APP_DIR/media

echo -e "${YELLOW}[7/8]${NC} Setting up environment file..."
if [ ! -f "$APP_DIR/.env" ]; then
    echo "Creating .env file (you'll need to edit this manually)..."
    cat > $APP_DIR/.env << 'EOF'
# Django Settings
SECRET_KEY=your-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=your-ec2-ip,your-domain.com

# Database (use RDS or local PostgreSQL)
DATABASE_URL=postgres://user:password@localhost:5432/scholarships

# CORS
CORS_ALLOWED_ORIGINS=https://nabin216.github.io,https://nabin216.github.io/scholarship-portal
FRONTEND_URL=https://nabin216.github.io/scholarship-portal

# AWS SES (Optional - for email)
AWS_SES_REGION=eu-north-1
AWS_SES_FROM_EMAIL=your-email@example.com
AWS_SES_SMTP_USERNAME=your-smtp-username
AWS_SES_SMTP_PASSWORD=your-smtp-password

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://your-domain.com

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080
EOF
    echo -e "${YELLOW}⚠️  Please edit $APP_DIR/.env with your actual values!${NC}"
else
    echo ".env already exists, skipping..."
fi

echo -e "${GREEN}[8/8]${NC} Running Django management commands..."
python manage.py collectstatic --noinput
python manage.py migrate

echo ""
echo -e "${GREEN}✓ Initial setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit $APP_DIR/.env with your actual configuration"
echo "2. Run: sudo bash $APP_DIR/deploy/setup-services.sh"
echo "3. Create superuser: python manage.py createsuperuser"
echo ""
