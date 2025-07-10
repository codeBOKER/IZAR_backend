from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductColor, Review, Email
from .forms import ProductAdminForm, ProductColorAdminForm, CategoryAdminForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['header', 'is_active', 'created_at', 'display_sizes']
    list_filter = ['is_active']
    search_fields = ['header', 'description']
    fields = ['header', 'description', 'image', 'image_upload', 'is_active', 'sizes']

    def display_sizes(self, obj):
        return ', '.join(obj.get_sizes_display())
    display_sizes.short_description = 'Sizes'

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    form = ProductColorAdminForm
    extra = 1  # Number of empty forms to display
    fields = ['name', 'color_preview', 'image', 'image_upload', 'is_available']
    readonly_fields = ['color_preview', 'image']
    min_num = 1  # Require at least one color
    validate_min = True  # Enforce the minimum number

    def color_preview(self, obj):
        if obj and obj.name:
            return format_html(
                '<div style="display: flex; align-items: center;">'
                '<div style="width: 24px; height: 24px; border-radius: 50%; background-color: #{}; margin-right: 8px; border: 1px solid #ccc;"></div>'
                '{}'
                '</div>',
                obj.name, obj.get_color_display_name()
            )
        return ""
    color_preview.short_description = 'Color Preview'

    def has_delete_permission(self, request, obj=None):
        """Prevent deleting the last color in the inline form."""
        # In the inline context, obj is the parent model (Product)
        if obj is None:
            return True

        # For the product, check if it has more than one color
        if hasattr(obj, 'colors'):
            # If this is a new product or it has multiple colors, allow delete
            if not obj.pk or obj.colors.count() > 1:
                return True

            # If it has only one color, show a message and prevent deletion
            if request:
                from django.contrib import messages
                messages.warning(request, f"Cannot delete the last color of product '{obj.header}'. A product must have at least one color.")
            return False

        # Default to allowing deletion
        return True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['header', 'category', 'price', 'is_active', 'color_count']
    list_filter = ['category', 'is_active']
    search_fields = ['header', 'description']
    inlines = [ProductColorInline]

    fieldsets = [
        ('Basic Information', {
            'fields': ['header', 'category', 'description', 'price', 'is_active']
        }),
    ]

    def color_count(self, obj):
        """Display the number of colors for this product."""
        return obj.colors.count()
    color_count.short_description = 'Colors'

    def save_model(self, request, obj, form, change):
        """Call full_clean to trigger the model's validation."""
        obj.full_clean()
        super().save_model(request, obj, form, change)

admin.site.register(Review)

admin.site.register(Email)