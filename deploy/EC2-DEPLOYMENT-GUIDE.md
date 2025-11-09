# AWS EC2 Deployment Guide - Scholarship Portal Backend

## Prerequisites
- AWS account with free tier eligibility
- Domain name (optional but recommended)
- GitHub repository with your code

## Part 1: Create EC2 Instance

### 1.1 Launch EC2 Instance
1. Log into AWS Console → EC2 Dashboard
2. Click "Launch Instance"
3. **Name**: `scholarship-backend`
4. **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
5. **Instance Type**: `t2.micro` (1 vCPU, 1GB RAM - Free tier)
6. **Key Pair**: Create new or select existing (download `.pem` file)
7. **Storage**: 8-30 GB gp3 (Free tier: up to 30GB)

### 1.2 Configure Security Group
Create security group with these inbound rules:

| Type  | Protocol | Port | Source    | Description          |
|-------|----------|------|-----------|----------------------|
| SSH   | TCP      | 22   | My IP     | SSH access           |
| HTTP  | TCP      | 80   | 0.0.0.0/0 | Public HTTP          |
| HTTPS | TCP      | 443  | 0.0.0.0/0 | Public HTTPS         |

### 1.3 Allocate Elastic IP (Optional but recommended)
1. EC2 → Elastic IPs → Allocate
2. Associate with your instance
3. Note the IP address

## Part 2: Connect to EC2

### Windows (PowerShell)
```powershell
# Set permissions on .pem file
icacls "scholarship-backend.pem" /inheritance:r
icacls "scholarship-backend.pem" /grant:r "$($env:USERNAME):(R)"

# Connect
ssh -i "scholarship-backend.pem" ubuntu@YOUR_EC2_IP
```

### Linux/Mac
```bash
chmod 400 scholarship-backend.pem
ssh -i scholarship-backend.pem ubuntu@YOUR_EC2_IP
```

## Part 3: Initial Server Setup

### 3.1 Update system
```bash
sudo apt update && sudo apt upgrade -y
```

### 3.2 Clone your repository
```bash
cd /home/ubuntu
git clone https://github.com/nabin216/scholarship-portal.git scholarship-backend
cd scholarship-backend/scholarship-backend
```

### 3.3 Run deployment script
```bash
chmod +x deploy/deploy.sh
bash deploy/deploy.sh
```

### 3.4 Configure environment
```bash
nano /home/ubuntu/scholarship-backend/.env
```

**Required .env values:**
```env
SECRET_KEY=generate-with-python-secrets-module
DEBUG=False
ALLOWED_HOSTS=YOUR_EC2_IP,your-domain.com

# Database (SQLite for now, or use RDS PostgreSQL)
# DATABASE_URL=postgres://user:pass@host:5432/scholarships

CORS_ALLOWED_ORIGINS=https://nabin216.github.io,https://nabin216.github.io/scholarship-portal
FRONTEND_URL=https://nabin216.github.io/scholarship-portal

# AWS SES for email (optional)
AWS_SES_REGION=eu-north-1
AWS_SES_FROM_EMAIL=your-verified-email@example.com
AWS_SES_SMTP_USERNAME=your-smtp-username
AWS_SES_SMTP_PASSWORD=your-smtp-password

SECURE_SSL_REDIRECT=False  # Set to True after HTTPS setup
CSRF_TRUSTED_ORIGINS=http://YOUR_EC2_IP
```

Generate SECRET_KEY:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.5 Update Nginx config with your IP/domain
```bash
sudo nano /home/ubuntu/scholarship-backend/deploy/nginx-scholarship-backend.conf
# Change: server_name YOUR_EC2_IP;
```

### 3.6 Setup services
```bash
chmod +x deploy/setup-services.sh
sudo bash deploy/setup-services.sh
```

### 3.7 Create Django superuser
```bash
cd /home/ubuntu/scholarship-backend/scholarship-backend
source ../.venv/bin/activate
python manage.py createsuperuser
```

## Part 4: Verify Deployment

1. **Check Gunicorn**: `sudo systemctl status gunicorn`
2. **Check Nginx**: `sudo systemctl status nginx`
3. **View logs**: `sudo tail -f /home/ubuntu/scholarship-backend/logs/gunicorn-error.log`
4. **Test API**: Open `http://YOUR_EC2_IP/admin/` in browser

## Part 5: Optional - Setup HTTPS with Let's Encrypt

```bash
# Install certbot (already done in deploy.sh)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Update .env
nano /home/ubuntu/scholarship-backend/.env
# Set: SECURE_SSL_REDIRECT=True
# Set: CSRF_TRUSTED_ORIGINS=https://your-domain.com

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

Certbot will auto-renew. Test renewal:
```bash
sudo certbot renew --dry-run
```

## Part 6: Database Options

### Option A: SQLite (Default - included)
- Already configured
- Good for small traffic
- Data stored on instance

### Option B: RDS PostgreSQL (Recommended for production)
1. Create RDS PostgreSQL instance (free tier: db.t3.micro)
2. Security group: allow port 5432 from EC2 security group
3. Update `.env`:
   ```env
   DATABASE_URL=postgres://username:password@rds-endpoint:5432/scholarships
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```

## Part 7: Update Frontend to Use EC2 Backend

In `scholarship-portal/.env.production`:
```env
NEXT_PUBLIC_API_URL=https://your-domain.com/api
NEXT_PUBLIC_BASE_URL=https://your-domain.com
```

Or if using IP:
```env
NEXT_PUBLIC_API_URL=http://YOUR_EC2_IP/api
NEXT_PUBLIC_BASE_URL=http://YOUR_EC2_IP
```

Redeploy frontend to GitHub Pages.

## Useful Commands

### Service Management
```bash
# Restart backend
sudo systemctl restart gunicorn

# View logs
sudo tail -f /home/ubuntu/scholarship-backend/logs/gunicorn-error.log
sudo tail -f /var/log/nginx/scholarship-backend-error.log

# Check status
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### Updates
```bash
cd /home/ubuntu/scholarship-backend
git pull origin main
source .venv/bin/activate
pip install -r scholarship-backend/requirements.txt
python scholarship-backend/manage.py migrate
python scholarship-backend/manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Django Management
```bash
cd /home/ubuntu/scholarship-backend/scholarship-backend
source ../.venv/bin/activate
python manage.py shell          # Django shell
python manage.py dbshell        # Database shell
python manage.py createsuperuser
```

## Monitoring & Maintenance

### Check disk space
```bash
df -h
```

### Check memory
```bash
free -m
```

### View active connections
```bash
sudo netstat -tulpn | grep LISTEN
```

### Security best practices
1. Keep system updated: `sudo apt update && sudo apt upgrade`
2. Use strong passwords
3. Enable firewall: `sudo ufw enable`
4. Regular backups of database and media files
5. Monitor logs for suspicious activity

## Troubleshooting

### 502 Bad Gateway
- Check Gunicorn: `sudo systemctl status gunicorn`
- Check logs: `sudo tail -f /home/ubuntu/scholarship-backend/logs/gunicorn-error.log`
- Verify socket: `ls -l /home/ubuntu/scholarship-backend/gunicorn.sock`

### Static files not loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Database migrations fail
```bash
python manage.py showmigrations  # See migration status
python manage.py migrate --fake-initial  # If needed
```

### Permission errors
```bash
sudo chown -R ubuntu:www-data /home/ubuntu/scholarship-backend
sudo chmod -R 755 /home/ubuntu/scholarship-backend
```

## Cost Estimate (Free Tier)
- **EC2 t2.micro**: 750 hours/month (free for 12 months)
- **EBS Storage**: 30GB (free for 12 months)
- **Data Transfer**: 15GB out/month (always free)
- **RDS db.t3.micro** (optional): 750 hours/month + 20GB storage (free for 12 months)

**After free tier**: ~$10-15/month for t2.micro + storage

## Next Steps
1. Set up automated backups
2. Configure monitoring with CloudWatch
3. Set up CI/CD with GitHub Actions
4. Consider adding Redis for caching
5. Set up log rotation

## Support
- Django Docs: https://docs.djangoproject.com/
- AWS EC2 Docs: https://docs.aws.amazon.com/ec2/
- Nginx Docs: https://nginx.org/en/docs/
