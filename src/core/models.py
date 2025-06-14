import requests
from django.db import models
from .utils import upload_image_to_imgur

class Category(models.Model):
    header = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    SIZES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('2XL', '2X Large'),
        ('3XL', '3X Large'),
        ('4XL', '4X Large'),
        ('5XL', '5X Large'),
        ('6XL', '6X Large'),
    ]
    sizes = models.TextField(
        blank=True,
        help_text="Comma-separated list of available sizes (e.g., S,M,L,XL)"
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.header

    def get_sizes_display(self):
        """Return a list of human-readable size names for the category."""
        if not self.sizes:
            return []
        size_dict = dict(self.SIZES)
        return [size_dict.get(size.strip(), size.strip()) for size in self.sizes.split(',') if size.strip()]

    def save(self, *args, **kwargs):
        image_file = kwargs.pop('image_file', None)
        if image_file:
            self.image = upload_image_to_imgur(image_file)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    header = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_available_sizes_display(self):
        """Return a list of human-readable size names."""
        if not self.available_sizes:
            return []

        # Create a dict mapping size codes to their display names
        size_dict = dict(self.SIZES)
        return [size_dict.get(size, size) for size in self.available_sizes]

    def clean(self):
        """Validate that the product has at least one color."""
        from django.core.exceptions import ValidationError

        # Skip validation for new products (not yet saved)
        if self.pk:
            if not self.colors.exists():
                raise ValidationError("A product must have at least one color.")

        super().clean()

    def __str__(self):
        return self.header

class ProductColor(models.Model):
    # Define the 10 most popular colors with their hex codes
    COLOR_CHOICES = [
        ('FF0000', 'Red'),
        ('0000FF', 'Blue'),
        ('008000', 'Green'),
        ('FFFF00', 'Yellow'),
        ('FFA500', 'Orange'),
        ('800080', 'Purple'),
        ('FFC0CB', 'Pink'),
        ('A52A2A', 'Brown'),
        ('000000', 'Black'),
        ('FFFFFF', 'White'),
    ]

    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=COLOR_CHOICES, help_text="Select a color")
    color_code = models.CharField(max_length=7, editable=False)  # Will be set automatically based on name
    image = models.URLField(blank=True, null=True)  # Store Imgur link as 'image'
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        image_file = kwargs.pop('image_file', None)
        if image_file:
            self.image = upload_image_to_imgur(image_file)
        for code, _ in self.COLOR_CHOICES:
            if self.name == code:
                self.color_code = f'#{code}'
                break
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deleting the last color of a product."""
        from django.core.exceptions import ValidationError

        # Check if this is the last color for the product
        if self.product.colors.count() <= 1:
            raise ValidationError("Cannot delete the last color of a product. A product must have at least one color.")

        # If it's not the last color, proceed with deletion
        return super().delete(*args, **kwargs)

    def get_color_display_name(self):
        """Return the display name for the selected color."""
        for code, display_name in self.COLOR_CHOICES:
            if self.name == code:
                return display_name
        return self.name

    def __str__(self):
        return f"{self.product.header} - {self.get_color_display_name()}"

class Review(models.Model):
    name = models.CharField(max_length=100)
    job_description = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)  # Store Imgur link as 'image'
    review = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    feedback = models.TextField()
    view = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        image_file = kwargs.pop('image_file', None)
        if image_file:
            self.image = upload_image_to_imgur(image_file)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.review}/5)"

class Email(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    topic = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.topic} ({self.email})"
