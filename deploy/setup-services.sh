#!/bin/bash
# Setup systemd services and Nginx for Scholarship Portal Backend

set -e

APP_DIR="/home/ubuntu/scholarship-backend"

echo "Setting up Gunicorn systemd service..."
sudo cp $APP_DIR/deploy/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn --no-pager

echo ""
echo "Setting up Nginx..."
sudo cp $APP_DIR/deploy/nginx-scholarship-backend.conf /etc/nginx/sites-available/scholarship-backend
sudo ln -sf /etc/nginx/sites-available/scholarship-backend /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default  # Remove default site

echo "Testing Nginx configuration..."
sudo nginx -t

echo "Restarting Nginx..."
sudo systemctl restart nginx
sudo systemctl enable nginx

echo ""
echo "Setting proper permissions..."
sudo chown -R ubuntu:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod 775 $APP_DIR/media
sudo chmod 775 $APP_DIR/logs

echo ""
echo "✓ Services configured successfully!"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status gunicorn    # Check Gunicorn status"
echo "  sudo systemctl restart gunicorn   # Restart backend"
echo "  sudo systemctl status nginx       # Check Nginx status"
echo "  sudo tail -f $APP_DIR/logs/gunicorn-error.log  # View logs"
echo ""
