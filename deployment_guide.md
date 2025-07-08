SEBPO Scraper Deployment Guide
Deploy the SEBPO Scraper Django project on Ubuntu with Gunicorn, Nginx, Systemd (or Supervisor), PostgreSQL, and static/media files.
Assumptions

Ubuntu 22.04/24.04 with SSH.
Project: /home/user/sebpo-scraper, Virtualenv: /home/user/sebpo-scraper/venv.
Replace user, server_ip, sebpo.com with your username, server IP, or domain.

1. Server Setup
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git nginx postgresql postgresql-contrib supervisor

2. PostgreSQL Setup
sudo -u postgres psql -c "CREATE DATABASE sebpo_scraper_db;"
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'etl';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sebpo_scraper_db TO postgres;"

Export local DB:
pg_dump -U postgres -h localhost sebpo_scraper_db > sebpo_scraper_db.dump
scp sebpo_scraper_db.dump user@server_ip:/home/user/

Import on server:
psql -U postgres -h localhost sebpo_scraper_db < /home/user/sebpo_scraper_db.dump

3. Django Project Setup
cd /home/user
git clone https://github.com/MarufSwe/sebpo-scraper.git sebpo-scraper
cd sebpo-scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn psycopg2-binary

Update sebpo_scraper/settings.py:
DEBUG = False
ALLOWED_HOSTS = ['sebpo.com', 'server_ip', 'localhost']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sebpo_scraper_db',
        'USER': 'postgres',
        'PASSWORD': 'etl',
        'HOST': 'localhost',
        'PORT': '',
    }
}
STATIC_URL = '/static/'
STATIC_ROOT = '/home/user/sebpo-scraper/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/user/sebpo-scraper/media/'

Run migrations and collect static files:
python manage.py migrate
python manage.py collectstatic

4. Gunicorn with Systemd
Test Gunicorn:
gunicorn --bind 0.0.0.0:8000 sebpo_scraper.wsgi:application

Create /etc/systemd/system/gunicorn.service:
[Unit]
Description=Gunicorn for SEBPO Scraper
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/sebpo-scraper
Environment="PATH=/home/user/sebpo-scraper/venv/bin"
ExecStart=/home/user/sebpo-scraper/venv/bin/gunicorn --workers 3 --bind unix:/home/user/sebpo-scraper/sebpo-scraper.sock sebpo_scraper.wsgi:application

[Install]
WantedBy=multi-user.target

Start Gunicorn:
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

5. Nginx Setup
Create /etc/nginx/sites-available/sebpo-scraper:
server {
    listen 80;
    server_name sebpo.com server_ip;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ { root /home/user/sebpo-scraper; }
    location /media/ { root /home/user/sebpo-scraper; }
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/sebpo-scraper/sebpo-scraper.sock;
    }
}

Enable and restart Nginx:
sudo ln -s /etc/nginx/sites-available/sebpo-scraper /etc/nginx/sites-enabled
sudo chown -R user:www-data /home/user/sebpo-scraper/{static,media}
sudo chmod -R 755 /home/user/sebpo-scraper/{static,media}
sudo nginx -t
sudo systemctl restart nginx

6. Secure Server
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d sebpo.com
sudo chown -R user:www-data /home/user/sebpo-scraper
sudo chmod -R 750 /home/user/sebpo-scraper

7. Test Deployment
Access http://sebpo.com or http://server_ip. Check logs:
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u gunicorn  # Systemd
sudo tail -f /var/log/sebpo-scraper.err.log  # Supervisor
