#!/bin/bash
# EC2 Backend Fix Script
# Run this on your EC2 server to fix WSGI import errors

echo "🔧 Fixing WSGI Import Error on EC2"
echo "===================================="

# Navigate to backend directory
cd /home/ubuntu/scholarship-backend || cd /var/www/scholarship-backend || cd ~/scholarship-backend

echo "📍 Current directory: $(pwd)"

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Activated .venv"
elif [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Activated venv"
else
    echo "❌ Virtual environment not found!"
    exit 1
fi

# Test WSGI import
echo ""
echo "🧪 Testing WSGI import..."
python -c "from scholarships_api.wsgi import application; print('✅ WSGI import successful!')" || {
    echo "❌ WSGI import failed!"
    echo ""
    echo "Checking Django installation..."
    pip list | grep -i django
    echo ""
    echo "Reinstalling dependencies..."
    pip install -r requirements.txt --no-deps --force-reinstall Django djangorestframework
}

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "❌ manage.py not found in current directory!"
    echo "Please cd to the correct directory containing manage.py"
    exit 1
fi

# Test Django can run
echo ""
echo "🧪 Testing Django..."
python manage.py check || {
    echo "❌ Django check failed!"
    exit 1
}

echo ""
echo "✅ All checks passed!"
echo ""
echo "📝 Next steps:"
echo "1. Update systemd service WorkingDirectory to: $(pwd)"
echo "2. sudo nano /etc/systemd/system/scholarship-backend.service"
echo "3. Set: WorkingDirectory=$(pwd)"
echo "4. Set: Environment=\"PATH=$(pwd)/.venv/bin\" (or venv path)"
echo "5. sudo systemctl daemon-reload"
echo "6. sudo systemctl restart scholarship-backend"
echo "7. sudo systemctl status scholarship-backend"
