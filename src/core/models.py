import requests
from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import upload_image_to_imgur

class Category(models.Model):
    header = models.CharField(_('العنوان'), max_length=100)
    description = models.TextField(_('الوصف'))
    image = models.URLField(_('الصورة'), blank=True, null=True)
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاريخ التحديث'), auto_now=True)
    is_active = models.BooleanField(_('نشط'), default=True)
    SIZES = [
        ('S', _('صغير')),
        ('M', _('متوسط')),
        ('L', _('كبير')),
        ('XL', _('كبير جدًا')),
        ('2XL', _('2X كبير')),
        ('3XL', _('3X كبير')),
        ('4XL', _('4X كبير')),
        ('5XL', _('5X كبير')),
        ('6XL', _('6X كبير')),
    ]
    sizes = models.TextField(
        _('المقاسات'),
        blank=True,
        help_text=_('قائمة المقاسات المتوفرة مفصولة بفواصل (مثال: S,M,L,XL)')
    )

    class Meta:
        verbose_name = _('القسم')
        verbose_name_plural = _('الاقسام')

    def __str__(self):
        return self.header

    def get_sizes_display(self):
        """Return a list of human-readable size names for the category."""
        if not self.sizes:
            return []
        size_dict = dict(self.SIZES)
        return [str(size_dict.get(size.strip(), size.strip())) for size in self.sizes.split(',') if size.strip()]

    def save(self, *args, **kwargs):
        image_file = kwargs.pop('image_file', None)
        if image_file:
            uploaded_url = upload_image_to_imgur(image_file)
            if uploaded_url:
                self.image = uploaded_url
            else:
                from .utils import handle_image_upload_failure
                handle_image_upload_failure(self, 'image')
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name=_('القسم'))
    header = models.CharField(_('العنوان'), max_length=200)
    description = models.TextField(_('الوصف'))
    price = models.DecimalField(_('السعر'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاريخ التحديث'), auto_now=True)
    is_active = models.BooleanField(_('نشط'), default=True)

    def get_available_sizes_display(self):
        """Return a list of human-readable size names."""
        if not self.available_sizes:
            return []

        # Create a dict mapping size codes to their display names
        size_dict = dict(Category.SIZES)
        return [str(size_dict.get(size, size)) for size in self.available_sizes]

    def clean(self):
        """Validate that the product has at least one color."""
        from django.core.exceptions import ValidationError

        # Skip validation for new products (not yet saved)
        if self.pk:
            if not self.colors.exists():
                raise ValidationError(_('يجب أن يحتوي المنتج على لون واحد على الأقل.'))

        super().clean()

    def __str__(self):
        return self.header
    
    class Meta:
        verbose_name = _('المنتج')
        verbose_name_plural = _('المنتجات')

class ProductColor(models.Model):
    # Define the 10 most popular colors with their hex codes
    COLOR_CHOICES = [
        ('FF0000', _('أحمر')),
        ('0000FF', _('أزرق')),
        ('008000', _('أخضر')),
        ('FFFF00', _('أصفر')),
        ('FFA500', _('برتقالي')),
        ('800080', _('بنفسجي')),
        ('FFC0CB', _('وردي')),
        ('A52A2A', _('بني')),
        ('000000', _('أسود')),
        ('FFFFFF', _('أبيض')),
    ]

    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE, verbose_name=_('المنتج'))
    name = models.CharField(_('اللون'), max_length=50, choices=COLOR_CHOICES, help_text=_('اختر لونًا'))
    color_code = models.CharField(_('كود اللون'), max_length=7, editable=False)  # Will be set automatically based on name
    image = models.URLField(_('الصورة'), blank=True, null=True)  # Store Imgur link as 'image'
    is_available = models.BooleanField(_('متوفر'), default=True)

    def save(self, *args, **kwargs):
        image_file = kwargs.pop('image_file', None)
        if image_file:
            uploaded_url = upload_image_to_imgur(image_file)
            if uploaded_url:
                self.image = uploaded_url
            else:
                from .utils import handle_image_upload_failure
                handle_image_upload_failure(self, 'image')
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
            raise ValidationError(_('لا يمكن حذف آخر لون للمنتج. يجب أن يحتوي المنتج على لون واحد على الأقل.'))

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
    class Meta:
        verbose_name = _('اللون')
        verbose_name_plural = _('الالوان')    

class Review(models.Model):
    name = models.CharField(_('الاسم'), max_length=100)
    job_description = models.CharField(_('المسمى الوظيفي'), max_length=100)
    image = models.URLField(_('الصورة'), blank=True, null=True)  # Store Imgur link as 'image'
    review = models.PositiveSmallIntegerField(_('التقييم'), choices=[(i, str(i)) for i in range(1, 6)])
    feedback = models.TextField(_('الملاحظات'))
    view = models.BooleanField(_('مرئي'), default=False)

    def save(self, *args, **kwargs):
        image_file = kwargs.pop('image_file', None)
        if image_file:
            uploaded_url = upload_image_to_imgur(image_file)
            if uploaded_url:
                self.image = uploaded_url
            else:
                from .utils import handle_image_upload_failure
                handle_image_upload_failure(self, 'image')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.review}/5)"
    
    class Meta:
        verbose_name = _('التقيم')
        verbose_name_plural = _('التقيمات')

class Email(models.Model):
    name = models.CharField(_('الاسم'), max_length=100)
    email = models.EmailField(_('البريد الإلكتروني'))
    phone_number = models.CharField(_('رقم الهاتف'), max_length=20)
    topic = models.CharField(_('الموضوع'), max_length=200)
    message = models.TextField(_('الرسالة'))
    created_at = models.DateTimeField(_('تاريخ الإرسال'), auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.topic} ({self.email})"
    
    class Meta:
        verbose_name = _('الايميل')
        verbose_name_plural = _('الايميلات')
