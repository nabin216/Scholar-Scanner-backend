#!/bin/bash
# Pull the latest code and restart the backend.
# Called by GitHub Actions (.github/workflows/deploy-oracle.yml) on every push to master.
# Can also be run by hand on the VM: bash ~/scholarship-backend/deploy/oracle-deploy.sh

set -e

APP_DIR="$HOME/scholarship-backend"
BRANCH="master"

cd "$APP_DIR"

echo "==> Pulling latest code from GitHub ($BRANCH)"
git fetch origin "$BRANCH"
git reset --hard "origin/$BRANCH"   # .env, logs/ and staticfiles/ are gitignored and kept

echo "==> Installing dependencies"
.venv/bin/pip install -q -r requirements.txt

echo "==> Running migrations"
.venv/bin/python manage.py migrate --noinput

echo "==> Loading scholarships (adds missing ones and their images, never overwrites edits)"
.venv/bin/python manage.py load_real_scholarships

echo "==> Collecting static files"
.venv/bin/python manage.py collectstatic --noinput

echo "==> Restarting service"
sudo systemctl restart scholarship-backend

sleep 5
if systemctl is-active --quiet scholarship-backend; then
    echo "==> Deployed $(git rev-parse --short HEAD) successfully"
else
    echo "==> Service failed to start:"
    sudo journalctl -u scholarship-backend -n 50 --no-pager
    exit 1
fi
