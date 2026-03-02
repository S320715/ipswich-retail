"""Models for the shop application."""

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Product category model."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list') + f'?category={self.slug}'


class Product(models.Model):
    """Product model for children's clothing items."""

    CATEGORY_CHOICES = [
        ('t-shirts', 'T-Shirts'),
        ('dresses', 'Dresses'),
        ('jackets', 'Jackets'),
        ('trousers', 'Trousers'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
    ]

    AGE_RANGE_CHOICES = [
        ('0-6m', '0-6 Months'),
        ('6-12m', '6-12 Months'),
        ('1-2y', '1-2 Years'),
        ('2-4y', '2-4 Years'),
        ('5-7y', '5-7 Years'),
        ('8-10y', '8-10 Years'),
        ('11-12y', '11-12 Years'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    age_range = models.CharField(max_length=20, choices=AGE_RANGE_CHOICES)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    sizes = models.CharField(
        max_length=200,
        help_text='Comma-separated sizes, e.g. "2Y, 3Y, 4Y"'
    )
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def get_sizes_list(self):
        """Return sizes as a list."""
        return [s.strip() for s in self.sizes.split(',') if s.strip()]

    def get_category_display_name(self):
        """Return human-readable category name."""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)

    def get_age_range_display_name(self):
        """Return human-readable age range."""
        return dict(self.AGE_RANGE_CHOICES).get(self.age_range, self.age_range)
