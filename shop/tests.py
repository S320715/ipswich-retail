"""Automated tests for the shop application."""

from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Category


class ProductModelTests(TestCase):
    """Unit tests for the Product model."""

    def setUp(self):
        """Create a sample product for testing."""
        self.product = Product.objects.create(
            name='Rainbow Stripe T-Shirt',
            description='A colourful t-shirt for kids.',
            price=Decimal('8.99'),
            category='t-shirts',
            age_range='2-4y',
            sizes='2Y, 3Y, 4Y',
            featured=True,
        )

    def test_product_creation(self):
        """Test that a product can be created and saved."""
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.name, 'Rainbow Stripe T-Shirt')

    def test_product_string_representation(self):
        """Test that str(product) returns the product name."""
        self.assertEqual(str(self.product), 'Rainbow Stripe T-Shirt')

    def test_product_price(self):
        """Test that the price is stored correctly as a decimal."""
        self.assertEqual(self.product.price, Decimal('8.99'))

    def test_category_assignment(self):
        """Test that the category is assigned correctly."""
        self.assertEqual(self.product.category, 't-shirts')

    def test_featured_flag(self):
        """Test that the featured filter works."""
        featured = Product.objects.filter(featured=True)
        self.assertEqual(featured.count(), 1)
        self.assertIn(self.product, featured)

    def test_get_sizes_list(self):
        """Test that sizes are returned as a list."""
        sizes = self.product.get_sizes_list()
        self.assertEqual(sizes, ['2Y', '3Y', '4Y'])

    def test_get_absolute_url(self):
        """Test that the product URL is generated correctly."""
        url = self.product.get_absolute_url()
        self.assertEqual(url, f'/products/{self.product.pk}/')


class CategoryModelTests(TestCase):
    """Unit tests for the Category model."""

    def setUp(self):
        self.category = Category.objects.create(name='T-Shirts', slug='t-shirts')

    def test_category_creation(self):
        """Test that a category can be created."""
        self.assertEqual(Category.objects.count(), 1)

    def test_category_string_representation(self):
        """Test that str(category) returns the name."""
        self.assertEqual(str(self.category), 'T-Shirts')


class HomepageTests(TestCase):
    """Integration tests for the homepage."""

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('9.99'),
            category='t-shirts',
            age_range='2-4y',
            sizes='2Y, 3Y',
            featured=True,
        )

    def test_homepage_loads(self):
        """Test that the homepage returns status 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        """Test that the home view uses home.html."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_shows_featured_products(self):
        """Test that featured products appear on homepage."""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Test Product')


class ProductListTests(TestCase):
    """Integration tests for the product listing page."""

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Dress',
            price=Decimal('14.99'),
            category='dresses',
            age_range='2-4y',
            sizes='2Y, 3Y',
        )

    def test_product_list_loads(self):
        """Test that /products/ returns status 200."""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_uses_correct_template(self):
        """Test that product list uses product_list.html."""
        response = self.client.get(reverse('product_list'))
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_product_list_shows_products(self):
        """Test that products appear in the listing."""
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, 'Test Dress')

    def test_product_list_category_filter(self):
        """Test that category filtering works."""
        response = self.client.get(reverse('product_list') + '?category=dresses')
        self.assertContains(response, 'Test Dress')

        response = self.client.get(reverse('product_list') + '?category=jackets')
        self.assertNotContains(response, 'Test Dress')


class ProductDetailTests(TestCase):
    """Integration tests for the product detail page."""

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Detail Test Product',
            description='A wonderful product.',
            price=Decimal('19.99'),
            category='jackets',
            age_range='5-7y',
            sizes='5Y, 6Y, 7Y',
        )

    def test_product_detail_loads(self):
        """Test that /products/<id>/ returns status 200."""
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_shows_info(self):
        """Test that product details are displayed."""
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product.pk}))
        self.assertContains(response, 'Detail Test Product')
        self.assertContains(response, '19.99')


class CartTests(TestCase):
    """Integration tests for the shopping cart."""

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Cart Test Product',
            price=Decimal('12.99'),
            category='t-shirts',
            age_range='2-4y',
            sizes='2Y, 3Y, 4Y',
        )

    def test_cart_page_loads(self):
        """Test that /cart/ returns status 200."""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        """Test that adding a product to cart works."""
        response = self.client.post(
            reverse('add_to_cart', kwargs={'pk': self.product.pk}),
            {'size': '3Y', 'quantity': '1'}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after add

        # Check cart in session
        cart = self.client.session.get('cart', {})
        self.assertIn(str(self.product.pk), cart)

    def test_cart_shows_correct_items(self):
        """Test that after adding, cart displays the product."""
        self.client.post(
            reverse('add_to_cart', kwargs={'pk': self.product.pk}),
            {'size': '3Y', 'quantity': '1'}
        )
        response = self.client.get(reverse('cart'))
        self.assertContains(response, 'Cart Test Product')

    def test_remove_from_cart(self):
        """Test that removing an item from cart works."""
        # Add first
        self.client.post(
            reverse('add_to_cart', kwargs={'pk': self.product.pk}),
            {'size': '3Y', 'quantity': '1'}
        )
        # Then remove
        self.client.post(reverse('remove_from_cart', kwargs={'pk': self.product.pk}))
        cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.pk), cart)

    def test_empty_cart_message(self):
        """Test that empty cart shows friendly message."""
        response = self.client.get(reverse('cart'))
        self.assertContains(response, 'Your cart is empty')
