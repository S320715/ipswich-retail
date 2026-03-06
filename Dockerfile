FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=ipswich_retail.settings

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput
RUN python manage.py load_sample_data
RUN python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipswich_retail.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin123').exists():
    User.objects.create_superuser('admin123', 'admin@gmail.com', 'admin123')
"

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "ipswich_retail.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
