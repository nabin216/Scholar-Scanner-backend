#!/bin/bash
# One-time setup of the Oracle Cloud VM (Oracle Linux 9, Always Free VM.Standard.E2.1.Micro).
# Run on the VM as the default 'opc' user:
#   curl -fsSL https://raw.githubusercontent.com/nabin216/Scholar-Scanner-backend/master/deploy/oracle-server-setup.sh | bash
# After this, every push to master is deployed by .github/workflows/deploy-oracle.yml

set -e

APP_USER="$(whoami)"
APP_DIR="$HOME/scholarship-backend"
MEDIA_DIR="/var/www/scholarship-media"   # outside $HOME so nginx can read it under SELinux
REPO_URL="https://github.com/nabin216/Scholar-Scanner-backend.git"
BRANCH="master"
DOMAIN="api.scholarscanner.com"
PYTHON="python3.12"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[1/9]${NC} Adding 2 GB swap (the Micro VM only has 1 GB RAM)..."
if ! swapon --show | grep -q /swapfile2g; then
    sudo rm -f /swapfile2g   # remove a half-written file from an interrupted run
    sudo sed -i '\|/swapfile2g|d' /etc/fstab
    sudo dd if=/dev/zero of=/swapfile2g bs=1M count=2048 status=none
    sudo chmod 600 /swapfile2g
    sudo mkswap /swapfile2g
    sudo swapon /swapfile2g
    echo '/swapfile2g none swap sw 0 0' | sudo tee -a /etc/fstab
fi

echo -e "${GREEN}[2/9]${NC} Installing system packages..."
# Skip large repos this server doesn't need; loading their metadata takes 10+ min on 1 GB RAM
sudo dnf config-manager --set-disabled ol9_oci_included ol9_ksplice ol9_UEKR8 || true
sudo dnf module enable -y postgresql:16
sudo dnf install -y oracle-epel-release-el9
sudo dnf install -y $PYTHON $PYTHON-devel gcc git nginx \
    postgresql-server postgresql-contrib \
    policycoreutils-python-utils certbot python3-certbot-nginx

echo -e "${GREEN}[3/9]${NC} Opening HTTP/HTTPS in firewalld and SELinux..."
sudo firewall-cmd --permanent --add-service=http --add-service=https
sudo firewall-cmd --reload
sudo setsebool -P httpd_can_network_connect 1   # let nginx proxy to gunicorn

echo -e "${GREEN}[4/9]${NC} Setting up PostgreSQL..."
if [ ! -f /var/lib/pgsql/data/PG_VERSION ]; then
    sudo postgresql-setup --initdb
    # Password logins over localhost instead of ident
    sudo sed -i -E 's/^(host\s+all\s+all\s+\S+\s+)ident/\1scram-sha-256/' /var/lib/pgsql/data/pg_hba.conf
fi
sudo systemctl enable --now postgresql
# Small footprint for a 1 GB VM
sudo -u postgres psql -qc "ALTER SYSTEM SET shared_buffers = '64MB';"
sudo -u postgres psql -qc "ALTER SYSTEM SET max_connections = '20';"
sudo systemctl restart postgresql

DB_NAME="scholarships"
DB_USER="scholarship_user"
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    DB_PASSWORD=$(openssl rand -hex 24)
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
    DATABASE_URL="postgres://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME"
    echo "Created PostgreSQL database '$DB_NAME' and user '$DB_USER'"
fi

echo -e "${GREEN}[5/9]${NC} Cloning repository from GitHub..."
if [ ! -d "$APP_DIR/.git" ]; then
    git clone -b "$BRANCH" "$REPO_URL" "$APP_DIR"
fi
cd "$APP_DIR"
mkdir -p logs staticfiles
sudo mkdir -p "$MEDIA_DIR"
sudo chown "$APP_USER":nginx "$MEDIA_DIR"
sudo chmod 775 "$MEDIA_DIR"

echo -e "${GREEN}[6/9]${NC} Creating virtual environment..."
[ -d .venv ] || $PYTHON -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo -e "${GREEN}[7/9]${NC} Creating .env (if missing)..."
if [ ! -f .env ]; then
    PUBLIC_IP=$(curl -s https://ifconfig.me || echo "")
    SECRET=$(.venv/bin/python -c "from django.core.management.utils import get_random_secret_key as k; print(k())")
    JWT_SECRET=$(.venv/bin/python -c "from django.core.management.utils import get_random_secret_key as k; print(k())")
    cat > .env <<EOF
SECRET_KEY=$SECRET
JWT_SECRET_KEY=$JWT_SECRET
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,$PUBLIC_IP,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://scholarscanner.com,https://www.scholarscanner.com,https://nabin216.github.io
CSRF_TRUSTED_ORIGINS=https://scholarscanner.com,https://www.scholarscanner.com,https://nabin216.github.io,https://$DOMAIN
FRONTEND_URL=https://scholarscanner.com

DATABASE_URL=${DATABASE_URL:-}
MEDIA_ROOT=$MEDIA_DIR

# Keep False until certbot has issued the HTTPS certificate, then set all three to True
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# Add the rest of your production secrets below (Google OAuth, email, AI keys...)
# GOOGLE_CLIENT_ID=
# GOOGLE_CLIENT_SECRET=
# GOOGLE_OAUTH_REDIRECT_URI=https://scholarscanner.com/Authentication/google-callback
# GMAIL_USER=
# GMAIL_APP_PASSWORD=
EOF
    chmod 600 .env
    echo -e "${YELLOW}Created .env - edit it later with: nano $APP_DIR/.env${NC}"
elif [ -n "${DATABASE_URL:-}" ] && ! grep -q '^DATABASE_URL=' .env; then
    echo "DATABASE_URL=$DATABASE_URL" >> .env
fi

echo -e "${GREEN}[8/9]${NC} Running migrations and collecting static files..."
.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput

echo -e "${GREEN}[9/9]${NC} Configuring Gunicorn and Nginx..."
sudo tee /etc/systemd/system/scholarship-backend.service > /dev/null <<EOF
[Unit]
Description=Scholarship Portal Django Gunicorn Service
After=network.target postgresql.service

[Service]
User=$APP_USER
Group=nginx
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/.venv/bin/gunicorn \\
    --workers 2 \\
    --bind 127.0.0.1:8000 \\
    --timeout 120 \\
    --max-requests 500 --max-requests-jitter 50 \\
    --access-logfile $APP_DIR/logs/gunicorn-access.log \\
    --error-logfile $APP_DIR/logs/gunicorn-error.log \\
    scholarships_api.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/nginx/conf.d/scholarship-backend.conf > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN $(curl -s https://ifconfig.me);

    client_max_body_size 20M;

    location /media/ {
        alias $MEDIA_DIR/;
        expires 7d;
    }

    # Static files are served by WhiteNoise through gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
    }
}
EOF

sudo semanage fcontext -a -t httpd_sys_rw_content_t "$MEDIA_DIR(/.*)?" 2>/dev/null || true
sudo restorecon -R "$MEDIA_DIR"
# SELinux blocks systemd from executing files in home directories; mark the venv binaries as executables
sudo semanage fcontext -a -t bin_t "$APP_DIR/.venv/bin(/.*)?" 2>/dev/null || true
sudo restorecon -R "$APP_DIR/.venv/bin"
sudo systemctl daemon-reload
sudo systemctl enable --now scholarship-backend
sudo nginx -t
sudo systemctl enable --now nginx
sudo systemctl reload nginx

echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo "Test:        curl http://localhost/api/"
echo "Admin user:  cd $APP_DIR && .venv/bin/python manage.py createsuperuser"
echo "HTTPS:       point the DNS A record of $DOMAIN to this server, then run:"
echo "             sudo certbot --nginx -d $DOMAIN"
