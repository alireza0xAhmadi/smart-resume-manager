# سیستم رزومه‌ساز اختصاصی

## 📋 مشخصات فنی

### نیازمندی‌های سیستم
- **Docker:** v28.1.1+
- **Docker Compose:** v2.36.0+
- **Python:** 3.11+
- **Django:** 5.0.1
- **MariaDB:** 11.4

### پورت‌های اختصاصی
- **🌐 سایت اصلی:** `80` (Nginx)
- **🗄️ دیتابیس MariaDB:** `3307`
- **🔧 Adminer:** `8085`
- **🔧 phpMyAdmin:** `8086`
- **🐳 Portainer:** `9000` (HTTP enabled)
- **⚙️ Django Container:** `8500` (internal)

## 🚀 راه‌اندازی سریع

### 1. تنظیم دامنه محلی
```bash
# اضافه کردن my.local به hosts
sudo echo "127.0.0.1    my.local" >> /etc/hosts

# یا استفاده از اسکریپت خودکار
./setup-domain.sh
```

### 2. راه‌اندازی Docker
```bash
# بررسی ورژن Docker
docker --version
docker compose version

# ساخت و اجرای تمام سرویس‌ها
docker compose up --build -d

# مشاهده وضعیت کانتینرها
docker compose ps

# مشاهده لاگ‌ها
docker compose logs -f

# لاگ سرویس خاص
docker compose logs -f web
docker compose logs -f db
```

### 3. راه‌اندازی دیتابیس
```bash
# اجرای مایگریشن‌ها
docker compose exec web python manage.py migrate

# ایجاد superuser (اختیاری)
docker compose exec web python manage.py createsuperuser

# جمع‌آوری فایل‌های static
docker compose exec web python manage.py collectstatic --noinput
```

### 4. دسترسی به سرویس‌ها
| سرویس | آدرس | توضیحات |
|--------|-------|----------|
| **سایت اصلی** | http://my.local | رابط کاربری اصلی |
| **پنل ادمین Django** | http://my.local/admin | مدیریت محتوا (admin/admin123) |
| **Adminer** | http://my.local:8085 | مدیریت دیتابیس |
| **phpMyAdmin** | http://my.local:8086 | مدیریت دیتابیس |
| **لیست رزومه‌ها** | http://my.local/resumes | مشاهده رزومه‌ها |
| **ایجاد رزومه** | http://my.local/create | ایجاد رزومه جدید |
| **چاپ رزومه** | http://my.local/resumes/[ID]/pdf/ | نمایش رزومه برای چاپ |
| **Portainer** | http://my.local:9000 | مدیریت کانتینرها |
| **Health Check** | http://my.local/health | بررسی سلامت سیستم |

## 🗄️ اتصال به دیتابیس

### اطلاعات اتصال MariaDB
```
Host: localhost
Port: 3307
Database: resume_db
Username: resume_user
Password: resume_pass123
Root Password: root_pass123
```

### اتصال از طریق Adminer
1. مراجعه به http://my.local:8085
2. انتخاب نوع دیتابیس: `MySQL`
3. وارد کردن اطلاعات بالا

### اتصال مستقیم از CLI
```bash
# اتصال به MariaDB از خارج کانتینر
mysql -h 127.0.0.1 -P 3307 -u resume_user -p resume_db

# اتصال داخل کانتینر
docker compose exec db mysql -u resume_user -p resume_db
```

## 🐳 مدیریت کانتینرها با Portainer

### نحوه استفاده از Portainer
1. **دسترسی:** https://my.local:9443
2. **اولین بار:** ایجاد حساب کاربری admin
3. **امکانات:**
   - مشاهده وضعیت کانتینرها
   - مدیریت volumes و networks
   - مشاهده لاگ‌ها در رابط گرافیکی
   - restart/stop/start کانتینرها
   - مانیتورینگ resource usage

### دستورات مفید Portainer
```bash
# Reset کردن Portainer data
docker compose down
docker volume rm resume_portainer_data
docker compose up -d portainer

# بررسی وضعیت Portainer
docker compose logs portainer
```

## 🛠️ دستورات توسعه

### Docker Commands
```bash
# متوقف کردن تمام سرویس‌ها
docker compose down

# پاک کردن volumes (احتیاط! داده‌ها حذف می‌شوند)
docker compose down -v

# rebuild کردن فقط یک سرویس
docker compose up --build web

# دسترسی به shell Django
docker compose exec web python manage.py shell

# دسترسی به bash کانتینر
docker compose exec web bash

# دسترسی به MariaDB shell
docker compose exec db mysql -u root -p

# مشاهده resource usage
docker stats
```

### Django Commands
```bash
# ایجاد app جدید
docker compose exec web python manage.py startapp app_name

# ایجاد مایگریشن
docker compose exec web python manage.py makemigrations

# اعمال مایگریشن‌ها
docker compose exec web python manage.py migrate

# تست کردن
docker compose exec web python manage.py test

# ایجاد superuser
docker compose exec web python manage.py createsuperuser
```

### Database Commands
```bash
# backup دیتابیس
docker compose exec db mysqldump -u root -p resume_db > backup.sql

# restore دیتابیس
docker compose exec -T db mysql -u root -p resume_db < backup.sql

# پاک کردن تمام داده‌ها (احتیاط!)
docker compose exec db mysql -u root -p -e "DROP DATABASE resume_db; CREATE DATABASE resume_db;"
```

## 📁 ساختار پروژه
```
resume/
├── docker-compose.yml      # تنظیمات تمام سرویس‌ها
├── Dockerfile              # Django container
├── requirements.txt        # پکیج‌های Python
├── .env                    # متغیرهای محیطی
├── nginx/
│   └── nginx.conf          # تنظیمات Nginx
├── resume_builder/         # تنظیمات Django
│   ├── settings.py         # تنظیمات اصلی
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI config
├── resumes/               # اپلیکیشن اصلی
├── templates/             # قالب‌های HTML
├── staticfiles/           # فایل‌های static
├── media/                 # فایل‌های آپلود شده
└── README.md              # این فایل
```

## 🔍 مشکلات متداول و راه‌حل

### 1. مشکل اتصال به دیتابیس
```bash
# بررسی وضعیت MariaDB
docker compose logs db

# restart کردن دیتابیس
docker compose restart db

# بررسی network connectivity
docker compose exec web ping db
```

### 2. مشکل دسترسی به my.local
```bash
# بررسی hosts file
cat /etc/hosts | grep my.local

# اضافه کردن دوباره
echo "127.0.0.1    my.local" | sudo tee -a /etc/hosts

# flush DNS cache (macOS)
sudo dscacheutil -flushcache
```

### 3. مشکل Static Files
```bash
# جمع‌آوری مجدد static files
docker compose exec web python manage.py collectstatic --noinput --clear

# بررسی Nginx configuration
docker compose exec nginx nginx -t

# restart Nginx
docker compose restart nginx
```

### 4. مشکل Port در استفاده
```bash
# بررسی پورت‌های در حال استفاده
lsof -i :9080
lsof -i :3307
lsof -i :8085
lsof -i :9443

# kill کردن process اشغال‌کننده
sudo kill -9 <PID>
```

### 5. مشکل Permission در macOS/Linux
```bash
# اضافه کردن کاربر به گروه docker
sudo usermod -aG docker $USER

# logout و login مجدد یا:
newgrp docker

# تغییر ownership فایل‌ها
sudo chown -R $USER:$USER .
```

### 6. مشکل در Portainer
```bash
# reset کامل Portainer
docker compose stop portainer
docker volume rm resume_portainer_data
docker compose up -d portainer

# دسترسی به endpoint جدید
# https://my.local:9443 -> Add Environment -> Docker
```

## 🔐 امنیت

### تنظیمات امنیتی پیشنهادی:
- تغییر passwordهای پیش‌فرض در `.env`
- محدود کردن دسترسی به پورت‌ها از طریق firewall
- استفاده از SSL در production
- backup منظم دیتابیس

### تغییر passwordها:
```bash
# ویرایش فایل .env
nano .env

# تغییر دادن:
DB_PASSWORD=your_new_strong_password
SECRET_KEY=your_new_django_secret_key

# rebuild کانتینرها
docker compose down && docker compose up --build -d
```

## 📊 مانیتورینگ

### بررسی عملکرد:
```bash
# مشاهده resource usage
docker stats

# مشاهده logs در real-time
docker compose logs -f

# بررسی disk usage
docker system df

# cleanup unused resources
docker system prune -a --volumes
```

## 🚀 Production Deployment

### برای استقرار در سرور:
1. تغییر `DEBUG=False` در `.env`
2. تنظیم `ALLOWED_HOSTS` مناسب
3. استفاده از SSL certificate
4. تنظیم backup خودکار دیتابیس
5. راه‌اندازی monitoring

---

## 📞 پشتیبانی

در صورت بروز مشکل:
1. ابتدا بخش "مشکلات متداول" را بررسی کنید
2. لاگ‌های سیستم را چک کنید: `docker compose logs -f`
3. وضعیت سرویس‌ها را بررسی کنید: `docker compose ps`