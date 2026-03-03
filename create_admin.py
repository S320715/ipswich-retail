import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipswich_retail.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin123').exists():
    User.objects.create_superuser('admin123', 'admin@gmail.com', 'admin123')
    print("Admin created!")
