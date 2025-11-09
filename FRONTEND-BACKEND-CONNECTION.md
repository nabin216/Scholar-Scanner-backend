# 🔗 Frontend-Backend Connection Guide

## 📋 Overview
This guide connects your Next.js frontend (GitHub Pages/Custom Domain) with your Django backend (EC2).

**Current Setup:**
- **Frontend**: https://scholarscanner.com (GitHub Pages)
- **Backend**: https://api.scholarscanner.com (AWS EC2 with SSL) ✅

---

## 🎯 Step 1: Configure Backend (EC2)

### 1.1 SSH into EC2
```bash
ssh -i your-key.pem ubuntu@15.206.225.71
```

### 1.2 Navigate to Backend Directory
```bash
cd /var/www/scholarship-portal/scholarship-backend
# OR if you used the new deployment:
cd /home/ubuntu/scholarship-portal/scholarship-backend
```

### 1.3 Update .env File
```bash
nano .env
```

Add/Update these values:
```env
# Django Core
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=api.scholarscanner.com,scholarscanner.com,www.scholarscanner.com

# CORS - Allow your frontend domains
CORS_ALLOWED_ORIGINS=https://scholarscanner.com,https://www.scholarscanner.com,https://nabin216.github.io

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://scholarscanner.com,https://www.scholarscanner.com,https://nabin216.github.io,https://api.scholarscanner.com

# Frontend URL
FRONTEND_URL=https://scholarscanner.com

# Security (HTTPS is enabled)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

Generate SECRET_KEY if needed:
```bash
source .venv/bin/activate  # or: source venv/bin/activate
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 1.4 Restart Backend Service
```bash
# If using systemd:
sudo systemctl restart scholarship-backend
sudo systemctl restart gunicorn  # or whatever your service is named

# If using PM2:
pm2 restart all

# If running manually, restart the server
```

### 1.5 Verify Backend is Running
```bash
# Check service status
sudo systemctl status scholarship-backend

# Test API endpoint
curl http://localhost:8000/api/
curl http://15.206.225.71/api/
```

---

## 🌐 Step 2: Configure Frontend (GitHub Pages)

### 2.1 Frontend Configuration Already Updated ✅
The GitHub Actions workflow now uses:
```yaml
NEXT_PUBLIC_API_URL: https://api.scholarscanner.com/api
NEXT_PUBLIC_BASE_URL: https://api.scholarscanner.com
```

### 2.2 Trigger Deployment
The changes are already pushed. Monitor deployment:
```bash
# Check GitHub Actions
# https://github.com/nabin216/scholarship-portal/actions
```

### 2.3 Wait for Deploy (3-5 minutes)
- Build completes
- Pages deploys
- Site updates at https://scholarscanner.com

---

## 🔒 Step 3: Setup HTTPS for Backend (Recommended)

### Why HTTPS?
- Secure data transmission
- Avoid "Mixed Content" warnings
- Required for production

### Option A: Using Domain for Backend

If you have a subdomain like `api.scholarscanner.com`:

#### 3.1 Add DNS Record
```
Type: A
Name: api
Value: 15.206.225.71
```

#### 3.2 Update Nginx on EC2
```bash
sudo nano /etc/nginx/sites-available/scholarship-backend
```

Change:
```nginx
server_name api.scholarscanner.com;
```

#### 3.3 Install SSL Certificate
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.scholarscanner.com
```

#### 3.4 Update Backend .env
```env
ALLOWED_HOSTS=15.206.225.71,api.scholarscanner.com,scholarscanner.com
CSRF_TRUSTED_ORIGINS=https://scholarscanner.com,https://api.scholarscanner.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### 3.5 Update Frontend to Use HTTPS API
Update GitHub Actions workflow:
```yaml
NEXT_PUBLIC_API_URL: https://api.scholarscanner.com/api
NEXT_PUBLIC_BASE_URL: https://api.scholarscanner.com
```

### Option B: Using Cloudflare (Free SSL)

1. Add EC2 IP to Cloudflare DNS
2. Enable "Flexible SSL" or "Full SSL"
3. Cloudflare handles SSL termination
4. Backend sees HTTP from Cloudflare

---

## ✅ Step 4: Test Connection

### 4.1 Test Backend API
```bash
# From your local machine
curl https://api.scholarscanner.com/api/
curl https://api.scholarscanner.com/api/scholarships/

# Should return JSON data
```

### 4.2 Test Frontend Connection
1. Open: https://scholarscanner.com
2. Open Browser DevTools (F12)
3. Go to **Network** tab
4. Interact with the site (search scholarships, etc.)
5. Look for API calls to `https://api.scholarscanner.com/api/`
6. Verify **Status: 200 OK** and **🔒 HTTPS secure**

### 4.3 Test CORS
Check browser console for CORS errors:
- ❌ "Access-Control-Allow-Origin" error = CORS issue
- ✅ API calls succeed = CORS configured correctly

---

## 🐛 Troubleshooting

### Issue 1: CORS Error
**Error**: `Access to fetch at 'https://api.scholarscanner.com/api/' from origin 'https://scholarscanner.com' has been blocked by CORS policy`

**Solution**:
```bash
# On EC2, check .env
cat .env | grep CORS_ALLOWED_ORIGINS

# Should include: https://scholarscanner.com
nano .env
# Add: CORS_ALLOWED_ORIGINS=https://scholarscanner.com,...

sudo systemctl restart scholarship-backend
```

### Issue 2: API Not Reachable
**Error**: `Failed to fetch` or `ERR_CONNECTION_REFUSED`

**Solution**:
```bash
# Check backend is running
sudo systemctl status scholarship-backend
sudo systemctl status nginx

# Check port is open
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :80

# Check EC2 Security Group
# Ensure port 80 (HTTP) is open to 0.0.0.0/0
```

### Issue 3: 403 Forbidden / CSRF Error
**Error**: `CSRF verification failed`

**Solution**:
```bash
# Update .env on EC2
nano .env

# Add frontend URL to CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS=https://scholarscanner.com,https://nabin216.github.io

sudo systemctl restart scholarship-backend
```

### Issue 4: Mixed Content Warning ✅ RESOLVED
**Warning**: `Mixed Content: The page at 'https://...' was loaded over HTTPS, but requested an insecure resource 'http://...'`

**Solution**: ✅ Already using HTTPS with api.scholarscanner.com domain

### Issue 5: Backend Returns 500 Error
**Solution**:
```bash
# Check backend logs
sudo tail -f /home/ubuntu/scholarship-portal/scholarship-backend/logs/gunicorn-error.log

# Common causes:
# - Missing migrations: python manage.py migrate
# - Missing static files: python manage.py collectstatic --noinput
# - Wrong permissions: sudo chown -R ubuntu:www-data /path/to/app
```

---

## 📊 Architecture Diagram

```
┌─────────────────┐
│   Browser       │
│  (User)         │
└────────┬────────┘
         │
         │ HTTPS
         ▼
┌─────────────────────────┐
│  GitHub Pages           │
│  scholarscanner.com     │
│  (Next.js Static Site)  │
└────────┬────────────────┘
         │
         │ HTTP API Calls
         ▼
┌─────────────────────────┐
│  AWS EC2                │
│  api.scholarscanner.com │
│  (15.206.225.71)        │
│  ┌─────────────────┐    │
│  │  Nginx (80)     │    │
│  └────────┬────────┘    │
│           │             │
│           ▼             │
│  ┌─────────────────┐    │
│  │  Gunicorn       │    │
│  │  (Django)       │    │
│  └────────┬────────┘    │
│           │             │
│           ▼             │
│  ┌─────────────────┐    │
│  │  SQLite/        │    │
│  │  PostgreSQL     │    │
│  └─────────────────┘    │
└─────────────────────────┘
```

---

## 🔧 Quick Command Reference

### EC2 Backend Commands
```bash
# Restart backend
sudo systemctl restart scholarship-backend
sudo systemctl restart nginx

# View logs
sudo tail -f /home/ubuntu/scholarship-portal/scholarship-backend/logs/gunicorn-error.log
sudo tail -f /var/log/nginx/error.log

# Test API
curl http://localhost:8000/api/
curl https://api.scholarscanner.com/api/

# Update code
cd /home/ubuntu/scholarship-portal
git pull origin main
source scholarship-backend/.venv/bin/activate
pip install -r scholarship-backend/requirements.txt
python scholarship-backend/manage.py migrate
python scholarship-backend/manage.py collectstatic --noinput
sudo systemctl restart scholarship-backend
```

### Local Testing Commands
```bash
# Test backend from local machine
curl https://api.scholarscanner.com/api/

# Test with authentication
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.scholarscanner.com/api/scholarships/
```

---

## ✅ Verification Checklist

- [x] Backend hosted at api.scholarscanner.com with SSL ✅
- [ ] Backend .env updated with correct CORS_ALLOWED_ORIGINS
- [ ] Backend .env includes CSRF_TRUSTED_ORIGINS and api.scholarscanner.com
- [ ] Backend .env has correct ALLOWED_HOSTS
- [ ] Backend .env has SSL security enabled (SECURE_SSL_REDIRECT=True)
- [ ] Backend service restarted
- [ ] Backend API accessible: https://api.scholarscanner.com/api/
- [ ] Frontend workflow updated with backend URL
- [ ] Frontend deployed successfully
- [ ] Frontend can fetch data from backend (check DevTools Network tab)
- [ ] No CORS errors in browser console
- [ ] No Mixed Content warnings (both using HTTPS) ✅
- [ ] Test authentication flow (login/register)
- [ ] Test scholarship search/filtering

---

## 🚀 Next Steps

1. **Monitor First Deployment**
   - Watch GitHub Actions: https://github.com/nabin216/scholarship-portal/actions
   - Check for build errors

2. **Test Live Site**
   - Visit: https://scholarscanner.com
   - Test all features (search, filter, authentication)

3. **Setup HTTPS for Backend** (Recommended)
   - Get subdomain: api.scholarscanner.com
   - Install SSL certificate
   - Update frontend to use HTTPS API

4. **Setup Database Backups**
   - Regular backups of SQLite or PostgreSQL
   - Use AWS snapshots or cron jobs

5. **Monitor and Optimize**
   - Set up CloudWatch for EC2
   - Monitor API response times
   - Add caching (Redis) if needed

---

## 📞 Support Resources

- Django CORS: https://github.com/adamchainz/django-cors-headers
- Next.js Env Variables: https://nextjs.org/docs/basic-features/environment-variables
- AWS EC2 Security Groups: https://docs.aws.amazon.com/ec2/
- Nginx Configuration: https://nginx.org/en/docs/

---

**✨ Your frontend and backend are now configured to work together!**

Check GitHub Actions for deployment status, then test the live site.
