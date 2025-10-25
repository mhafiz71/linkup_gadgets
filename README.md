
# LinkUp Gadgets - Multi-Vendor E-commerce Platform

![LinkUp Gadgets Homepage](https://linkup-gadgets.onrender.com/static/images/banner.png)

LinkUp Gadgets is a full-featured, multi-vendor e-commerce marketplace built with Django and modern frontend technologies. The platform is designed to connect electronics vendors in Ghana with customers, providing a secure and seamless online shopping experience. It features individual vendor storefronts, integrated payments with Paystack, a complete shopping cart, a product review system, and dedicated dashboards for both customers and vendors.

**Live Site:** [LinkUp Gadgets on Render](https://linkup-gadgets.onrender.com)

---

## Key Features

-   **Multi-Vendor Architecture:** Allows multiple independent vendors to register, create a profile, and list products.
-   **Individual Vendor Storefronts:** Each vendor gets a public-facing page with their banner, logo, information, and product listings.
-   **Vendor Dashboard:** A secure, private dashboard for vendors to manage their products (add, edit, delete) and view their sales.
-   **Customer Accounts & Profiles:** Users can register, edit their profiles, and view a complete history of their past orders, with the ability to cancel unpaid orders.
-   **Full Shopping Cart System:** A session-based cart for both guests and logged-in users, with functionality to add, remove, and update item quantities.
-   **Secure Payment Integration:** Integrated with **Paystack** for secure online payments, supporting Mobile Money and cards in Ghana (GHS).
-   **Product Reviews & Ratings:** Customers who purchase an item can leave a star rating and a text review, with average ratings displayed on product cards.
-   **Dynamic Shop Page:** A central shop page with live search and category filtering to easily find products.
-   **Automated Email Notifications:** Sends professional, HTML-formatted emails for user registration and order confirmation using Google SMTP.
-   **Help & FAQ Page:** An interactive accordion-style FAQ page to assist users.
-   **Production-Ready & Deployed:** Configured for a production environment with Gunicorn, WhiteNoise for static files, and environment variables for security.

---

## Tech Stack

### Backend
-   **Framework:** Django 4.2+
-   **Database:** PostgreSQL (Production on Render) / SQLite3 (Development)
-   **Web Server:** Gunicorn
-   **Payments:** `django-paystack`
-   **Static Files:** `whitenoise`

### Frontend
-   **Styling:** Tailwind CSS
-   **Interactivity:** Alpine.js (for dropdowns and accordions)
-   **Templating:** Django Template Language with `django-widget-tweaks`

### Deployment
-   **Platform:** Render
-   **Database:** Render PostgreSQL
-   **Version Control:** Git & GitHub

---

## Local Development Setup

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.10+
-   `pip` and `venv`
-   Git

### 1. Clone the Repository

```bash
git clone https://github.com/[mhafiz71]/linkup_gadgets].git
cd [linkup_gadgets]
```

### 2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The project uses a `.env` file to manage secret keys and configuration.

-   Create a new file named `.env` in the project root.
-   Copy the contents of `.env.example` (or the block below) into your new `.env` file.

```ini
# .env file for local development

SECRET_KEY=your-django-secret-key-goes-here-make-it-long-and-random
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=sqlite:///db.sqlite3

# Use Paystack's TEST keys for development
PAYSTACK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PAYSTACK_PUBLIC_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PAYSTACK_CURRENCY=GHS

# Use Django's console email backend for development (prints emails to the terminal)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=LinkUp Gadgets <noreply@example.com>
```
**Note:** The `console.EmailBackend` is perfect for development as it prints email content directly to your terminal instead of sending a real email.

### 5. Run Database Migrations

Apply the database schema to your local SQLite database.

```bash
python manage.py migrate
```

### 6. Create a Superuser

Create an admin account to access the Django admin dashboard.

```bash
python manage.py createsuperuser
```
Follow the prompts to set up your username and password.

### 7. Run the Development Server

You're all set! Start the development server.

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`. You can access the Django admin panel at `http://127.0.0.1:8000/admin`.

---

## Author

-   **mhafiz71** - _Initial work & development_ - [Your GitHub Profile](https://github.com/mhafiz71/)
