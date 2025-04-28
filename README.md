# 🎧 FluxBeat – Headphone E-Commerce Platform

**FluxBeat** is a complete e-commerce platform for buying high-quality headphones. Built entirely using Django and styled with plain CSS, this project includes OTP-based authentication, offer management, Razorpay integration, and a custom admin panel for business insights.

---

## 🚀 Features

- 🛍️ Product listing with multiple color variants
- 🔎 Filter and search products by category
- 🎁 Manage offers, coupons, and referral bonuses
- 🔐 Email OTP-based login and authentication
- 📦 Order tracking and detailed user profiles
- 💳 Razorpay integration, wallet system & Cash on Delivery
- 🧑‍💼 Admin dashboard for sales reporting and management
---

## 🛠️ Tech Stack

- **Backend**: Django (Python), PostgreSQL
- **Frontend**: Django Templates (HTML), CSS
- **Authentication**: Email OTP
- **Payments**: Razorpay

---

## 📂 Project Structure
fluxbeat
    ├── fluxbeat/                  # Main Django project configuration
    │   ├── __init__.py
    │   ├── settings.py            # Django settings (DB, media, static, etc.)
    │   ├── urls.py                # Root URL routing
    │   ├── asgi.py
    │   └── wsgi.py
    │
    ├── fluxadmin/                 # Admin app (manage products, categories, offers)
    │   ├── migrations/
    │   ├── admin.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── ...
    │
    ├── user/                      # User-facing app (shop, cart, profile, etc.)
    │   ├── migrations/
    │   ├── admin.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── ...
    │
    ├── templates/                 # Global HTML templates (base.html, login, etc.)
    │   ├── base.html
    │   ├── home.html
    │   └── ...
    │
    ├── static/                    # Static files (CSS, JS, Images)
    │   ├── css/
    │   ├── js/
    │   └── images/
    │
    ├── media/                     # Uploaded media files (product images, etc.)
    │
    ├── manage.py
    └── requirements.txt

    
To run the project
_______________________

git clone https://github.com/vishnudas-max/ecomerce_website.git
cd ecomerce_website/fluxbeat

🐍 2. Create and Activate Virtual Environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

📦 3. Install Dependencies

pip install -r requirements.txt
⚙️ 4. Configure Database (SQLite used by default)
Create migrations and apply them:

python manage.py makemigrations
python manage.py migrate

👤 5. Create Superuser (for Admin Login)

python manage.py createsuperuser


python manage.py runserver

Then open your browser and go to:
http://127.0.0.1:8000/
Admin panel available at:

http://127.0.0.1:8000/flux_admin/
