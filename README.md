# Full-Stack E-Commerce Platform

A production-ready full-stack e-commerce platform built with **Django**, **PostgreSQL**, **Redis**, **Celery**, **Tailwind CSS**, and **JavaScript**. It includes secure authentication, shopping cart, coupon system, payment workflow, multilingual support, and background task processing.

## Features

* Custom user authentication with email login
* Role-based access control (RBAC)
* Product & category management
* Session-based shopping cart
* Coupon & discount system
* Secure checkout and order management
* Payment receipt upload & verification
* PostgreSQL full-text product search
* Redis caching
* Celery background tasks
* PDF invoice generation
* Email notifications
* English & Arabic language support
* Responsive UI with Tailwind CSS

## Tech Stack

* Python
* Django
* PostgreSQL
* Redis
* Celery
* Tailwind CSS
* JavaScript
* HTML5 & CSS3

## Installation

```bash
git clone https://github.com/yourusername/fullstack-ecommerce-platform.git

cd fullstack-ecommerce-platform

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

## License

This project was built for learning, portfolio, and educational purposes.
