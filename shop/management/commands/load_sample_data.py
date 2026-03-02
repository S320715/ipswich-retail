"""Management command to load sample children's clothing products."""

from django.core.management.base import BaseCommand
from shop.models import Product, Category


SAMPLE_PRODUCTS = [
    {
        'name': 'Rainbow Stripe T-Shirt',
        'description': 'A cheerful rainbow-striped tee made from 100% organic cotton. Soft, breathable, and perfect for sunny days at the park.',
        'price': '8.99',
        'category': 't-shirts',
        'age_range': '2-4y',
        'sizes': '2Y, 3Y, 4Y',
        'featured': True,
    },
    {
        'name': 'Floral Summer Dress',
        'description': 'A beautiful floral dress with a twirly skirt that little ones will love. Lightweight fabric perfect for warm summer days.',
        'price': '14.99',
        'category': 'dresses',
        'age_range': '2-4y',
        'sizes': '3Y, 4Y, 5Y',
        'featured': True,
    },
    {
        'name': 'Denim Dungarees',
        'description': 'Classic denim dungarees with adjustable straps and handy front pockets. Durable enough for all their adventures.',
        'price': '18.99',
        'category': 'trousers',
        'age_range': '1-2y',
        'sizes': '1Y, 2Y, 3Y',
        'featured': True,
    },
    {
        'name': 'Cosy Teddy Bear Jacket',
        'description': 'An adorable fluffy jacket with teddy bear ears on the hood. Super soft sherpa lining keeps them warm and snug.',
        'price': '22.99',
        'category': 'jackets',
        'age_range': '2-4y',
        'sizes': '2Y, 3Y, 4Y, 5Y, 6Y',
        'featured': True,
    },
    {
        'name': 'Soft Cotton Joggers',
        'description': 'Comfy joggers in soft brushed cotton with an elasticated waist. Perfect for playtime, school, or lazy weekends.',
        'price': '10.99',
        'category': 'trousers',
        'age_range': '5-7y',
        'sizes': '4Y, 5Y, 6Y, 7Y, 8Y',
        'featured': True,
    },
    {
        'name': 'Unicorn Print Pyjamas',
        'description': 'Magical unicorn pyjamas in soft jersey fabric. A dreamy bedtime favourite with a fun all-over print.',
        'price': '12.99',
        'category': 'accessories',
        'age_range': '2-4y',
        'sizes': '3Y, 4Y, 5Y, 6Y, 7Y',
        'featured': True,
    },
    {
        'name': 'Canvas Velcro Trainers',
        'description': 'Easy-on, easy-off canvas trainers with velcro straps. Lightweight and flexible for little feet on the go.',
        'price': '16.99',
        'category': 'shoes',
        'age_range': '2-4y',
        'sizes': '2Y, 3Y, 4Y, 5Y',
        'featured': False,
    },
    {
        'name': 'Star Pattern Hoodie',
        'description': 'A cosy hoodie covered in sparkly stars. Features a kangaroo pocket and soft fleece lining for extra warmth.',
        'price': '15.99',
        'category': 'jackets',
        'age_range': '5-7y',
        'sizes': '5Y, 6Y, 7Y, 8Y, 9Y, 10Y',
        'featured': False,
    },
    {
        'name': 'Polka Dot Skirt',
        'description': 'A playful polka dot skirt with a comfortable elasticated waistband. Pairs beautifully with tees and cardigans.',
        'price': '9.99',
        'category': 'dresses',
        'age_range': '5-7y',
        'sizes': '4Y, 5Y, 6Y, 7Y, 8Y',
        'featured': False,
    },
    {
        'name': 'Dinosaur Graphic Tee',
        'description': 'A roar-some dinosaur t-shirt that little adventurers will love! Made from soft cotton with a cool printed design.',
        'price': '7.99',
        'category': 't-shirts',
        'age_range': '2-4y',
        'sizes': '2Y, 3Y, 4Y, 5Y, 6Y',
        'featured': False,
    },
    {
        'name': 'Waterproof Rain Coat',
        'description': 'A bright and cheerful waterproof coat with sealed seams. Keeps them dry in the heaviest downpour — a British essential!',
        'price': '24.99',
        'category': 'jackets',
        'age_range': '2-4y',
        'sizes': '3Y, 4Y, 5Y, 6Y, 7Y, 8Y',
        'featured': False,
    },
    {
        'name': 'Knitted Beanie Hat',
        'description': 'A soft knitted beanie with a cute pom-pom on top. Perfect for keeping little heads warm on chilly days.',
        'price': '5.99',
        'category': 'accessories',
        'age_range': '1-2y',
        'sizes': '1Y, 2Y, 3Y, 4Y, 5Y',
        'featured': False,
    },
]

CATEGORIES = [
    ('T-Shirts', 't-shirts'),
    ('Dresses', 'dresses'),
    ('Jackets', 'jackets'),
    ('Trousers', 'trousers'),
    ('Shoes', 'shoes'),
    ('Accessories', 'accessories'),
]


class Command(BaseCommand):
    help = 'Load sample children\'s clothing products into the database'

    def handle(self, *args, **options):
        # Create categories
        for name, slug in CATEGORIES:
            Category.objects.get_or_create(name=name, slug=slug)
        self.stdout.write(self.style.SUCCESS(f'Created {len(CATEGORIES)} categories'))

        # Create products
        created_count = 0
        for product_data in SAMPLE_PRODUCTS:
            _, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data,
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded {created_count} sample products ({Product.objects.count()} total)'
        ))
