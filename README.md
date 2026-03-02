# 🧒 Ipswich Retail — Little Ones Collection

A children's clothing e-commerce application built with Django, demonstrating modern DevOps practices.

## Overview

Ipswich Retail is a proof-of-concept online shop selling children's clothing (ages 0–12). It features a polished, child-friendly design with a pastel colour scheme and fully functional shopping cart.

## Features

- **Homepage** — Hero banner with featured product showcase
- **Product Listing** — Filterable product grid by category
- **Product Detail** — Full product info with size selection and add-to-cart
- **Shopping Cart** — Session-based cart with quantity controls and order summary
- **Admin Panel** — Django admin for managing products and categories
- **Responsive Design** — Works on mobile, tablet, and desktop

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Django 4.2+ (Python 3.11) |
| Frontend | HTML5, Bootstrap 5, Custom CSS |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Server | Gunicorn |
| Static Files | WhiteNoise |
| Containerisation | Docker |
| CI/CD | GitHub Actions |
| Deployment | Render.com |

## Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/ipswich-retail.git
cd ipswich-retail

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load sample products
python manage.py load_sample_data

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit http://localhost:8000 to see the app.

### Docker

```bash
docker-compose up --build
```

## Running Tests

```bash
python manage.py test shop -v 2
```

With coverage:

```bash
pip install coverage
coverage run manage.py test shop
coverage report --show-missing
```

## Project Structure

```
ipswich-retail/
├── ipswich_retail/     # Django project settings
├── shop/              # Main app (models, views, tests)
├── templates/         # HTML templates (MVT)
├── static/            # CSS, JS, images
├── media/             # Uploaded product images
├── Dockerfile         # Container config
├── docker-compose.yml # Local Docker setup
└── .github/workflows/ # CI/CD pipeline
```

## DevOps Practices

- **Version Control** — Git with branching strategy (main + dev + feature)
- **Containerisation** — Docker for consistent environments
- **CI/CD** — GitHub Actions for automated testing and deployment
- **Testing** — 14+ automated tests (unit + integration)
- **Monitoring** — Django logging to console and file
- **Deployment** — Auto-deploy to Render.com

## Licence

This project was created for educational purposes as part of a DevOps module.
