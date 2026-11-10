# Trinials — Company Portfolio Website

A modern, high-performance company portfolio website for **Trinials**, built with Python and Django. Features a refined **Dark Olive Green** liquid glassmorphism design system, animated opening brand splash screen, interactive 3D perspective tilt visual art canvases, accessible semantic HTML5 components, fluid typography, responsive layout across all device viewports, interactive contact form with Gmail SMTP notification and client auto-response, and integrated Django Admin for inquiry management.

---

## 1. System Requirements

- **Python**: `3.10+` (Developed and tested with Python 3.13)
- **Django**: `6.1.2`
- **Database**: SQLite (default local) or PostgreSQL / MySQL / MariaDB (production-ready)
- **Operating System**: Cross-platform (Windows, macOS, Linux)

---

## 2. Quickstart & Local Development

### Step 1: Clone and Set Up Virtual Environment
```bash
# Clone the repository
git clone <repository-url>
cd "Trinails Group Protfolio"

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy the example environment configuration:
```bash
# Windows:
copy .env.example .env
# Linux / macOS:
cp .env.example .env
```
Edit `.env` to configure your settings (Gmail SMTP credentials, allowed hosts, etc.). For local development, defaults work out of the box.

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create a Superuser (For Django Admin)
```bash
python manage.py createsuperuser
```

### Step 6: Start the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 3. Brand Identity & Design System

- **Palette**: Dark Olive Green
  - `#002400`: Deepest Forest Midnight Black-Green (High emphasis typography)
  - `#273B09`: Deep Forest Olive Green (Sticky navbar, footer, buttons)
  - `#58641D`: Rich Dark Olive / Moss Green (Primary brand accent, icons)
  - `#7B904B`: Medium Sage / Olive Green (Borders, interactive focus rings)
  - `#BBCF8D`: Light Olive / Celadon Green (Badges, accents, progress bars)
  - `#E8E9E4`: Warm Alabaster Cream (Main surface canvas background)
- **Visual Art Canvases**:
  - Interactive 3D perspective tilt driven by mouse pointer coordinates.
  - Specular glass highlight sheen that tracks cursor movement.
  - Floating badges with independent floating motion.
  - Central sun orb with clickable pulse ring waves.
- **Intro Loader**:
  - Fullscreen branded opening splash animation with radial olive atmosphere, logo shimmer, and progress track.
- **Featured Client Projects**:
  - **Cherupuzha River Rafting** (`https://cherupuzhariverrafting.in`): Premier tourism & adventure booking platform.
  - **FancyStore**: Modern e-commerce apparel and lifestyle online retail destination.
  - **ElectroKart**: Full-scale electrical supplies store integrated with enterprise resource planning (ERP) inventory management.

---

## 4. Running Automated Tests

The project includes an automated test suite covering view rendering, section landmarks, navigation integrity, contact backend validation, honeypot protection, admin actions, and email resilience:

```bash
# Run standard system checks
python manage.py check

# Run all automated tests
python manage.py test
```

---

## 5. Production Deployment Guide

### A. Environment Configuration (`.env`)
In production, adjust the following critical environment variables:

| Variable | Recommended Production Value | Description |
| :--- | :--- | :--- |
| `DEBUG` | `False` | **Mandatory:** Disables Django debug tracebacks. |
| `SECRET_KEY` | *(50+ char random string)* | **Mandatory:** Cryptographically secure secret key. |
| `ALLOWED_HOSTS` | `trinials.com,www.trinials.com` | **Mandatory:** Allowed domain names. |
| `CSRF_TRUSTED_ORIGINS` | `https://trinials.com,https://www.trinials.com` | Trusted origins for CSRF POST requests. |
| `SECURE_SSL_REDIRECT` | `True` | Forces all HTTP traffic to HTTPS. |
| `SESSION_COOKIE_SECURE`| `True` | Transmits session cookies exclusively over HTTPS. |
| `CSRF_COOKIE_SECURE` | `True` | Transmits CSRF cookies exclusively over HTTPS. |
| `SECURE_HSTS_SECONDS` | `31536000` | Enables HTTP Strict Transport Security (1 year). |

Generate a secure production secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### B. Static Asset Collection
Collect all static files into `staticfiles/`:
```bash
python manage.py collectstatic --noinput
```

### C. Database Setup (Production)
To connect to an external production database (e.g., PostgreSQL):
```bash
# In your .env file:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=trinials_db
DB_USER=trinials_user
DB_PASSWORD=your_secure_db_password
DB_HOST=127.0.0.1
DB_PORT=5432
```
Then run migrations:
```bash
python manage.py migrate
```

### D. Production WSGI / ASGI Server
Do not use `runserver` in production. Use a production WSGI server:

**Linux / Unix (Gunicorn):**
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**Windows Server (Waitress):**
```bash
pip install waitress
waitress-serve --port=8000 config.wsgi:application
```

**ASGI (Uvicorn):**
```bash
pip install uvicorn
uvicorn config.asgi:application --host 0.0.0.0 --port 8000
```

### E. Email Notification Setup (Gmail SMTP)
Whenever a visitor submits an inquiry through the Contact form, notifications are dispatched to your team and an auto-confirmation is sent to the client:
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_USE_TLS=False
GMAIL_EMAIL=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=Trinials <your_gmail@gmail.com>
CONTACT_NOTIFICATION_EMAIL=johnpaulalex85@gmail.com, trinial26@gmail.com, Jojogeorge.trinials@gmail.com, joejoseph1235@gmail.com
CONTACT_EMAIL=trinial26@gmail.com
CONTACT_PHONE_NUMBER=+91 85908 21155
CONTACT_PHONE_NUMBER_SECONDARY=+91 94003 25570
CONTACT_WHATSAPP_URL=https://wa.me/918590821155
```

---

## 6. Website Pages & Routes

| Path | View | Purpose |
| :--- | :--- | :--- |
| `/` | `views.home` | Homepage containing Hero, About, Services, Work, Process, Contact |
| `/about/` | `views.about_page` | Dedicated About Us page detailing Trinials story, philosophy & leadership |
| `/privacy-policy/` | `views.privacy_policy` | Privacy Policy outlining inquiry data handling, bot prevention & user rights |
| `/terms-and-conditions/` | `views.terms_conditions` | Terms & Conditions covering studio services, IP ownership & governance |
| `/contact/` | `views.contact_submit` | POST endpoint for processing inquiries with validation, DB logging & emails |
| `/admin/` | `django.contrib.admin` | Secure administration panel for managing inquiries & contact submissions |

---

## 7. Deployment to Render (Render.com)

This repository includes [`build.sh`](file:///d:/Trinails Group/Trinails Group Protfolio/build.sh) and [`render.yaml`](file:///d:/Trinails Group/Trinails Group Protfolio/render.yaml) preconfigured for Render deployment:

1. **Create Web Service on Render**:
   - Log into [Render Dashboard](https://dashboard.render.com).
   - Click **New +** &rarr; **Web Service**.
   - Connect your GitHub repository (`Trinials-Website`).
2. **Build & Start Commands**:
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`
3. **Environment Variables**:
   Add the following in Render's Environment section:
   - `DEBUG`: `False`
   - `SECRET_KEY`: `<generate-a-strong-secret-key>`
   - `GMAIL_EMAIL`: `dummy11248@gmail.com`
   - `GMAIL_APP_PASSWORD`: `sxtu ldyf aayl yyvb`
   - `CONTACT_NOTIFICATION_EMAIL`: `johnpaulalex85@gmail.com, trinial26@gmail.com, Jojogeorge.trinials@gmail.com, joejoseph1235@gmail.com`
   - `RENDER_EXTERNAL_HOSTNAME`: *(Automatically set by Render)*
4. **Deploy**:
   Click **Create Web Service**. Render will install dependencies, collect static files with WhiteNoise, run migrations, and launch Gunicorn.

---

## 8. Deployment Verification Checklist

Run these checks before opening traffic to production:

- [ ] `python manage.py check` passes with 0 issues.
- [ ] `python manage.py check --deploy` passes without unexpected security warnings.
- [ ] `python manage.py makemigrations --check --dry-run` confirms no pending unapplied migrations.
- [ ] `python manage.py migrate --check` confirms all migrations are applied.
- [ ] `python manage.py test` passes all test cases.
- [ ] `python manage.py collectstatic --noinput` copies all assets cleanly.
- [ ] Custom `404.html` and `500.html` templates render as expected when `DEBUG=False`.
- [ ] Superuser created and verified at `/admin/`.
"# Trinials-Website" 
