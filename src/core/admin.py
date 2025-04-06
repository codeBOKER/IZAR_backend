from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductColor
from .forms import ProductAdminForm, ProductColorAdminForm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['header', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['header', 'description']

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    form = ProductColorAdminForm
    extra = 1  # Number of empty forms to display
    fields = ['name', 'image', 'is_available']
    min_num = 1  # Require at least one color
    validate_min = True  # Enforce the minimum number

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
    list_display = ['header', 'category', 'price', 'is_active', 'display_sizes', 'color_count']
    list_filter = ['category', 'is_active']
    search_fields = ['header', 'description']
    inlines = [ProductColorInline]

    fieldsets = [
        ('Basic Information', {
            'fields': ['header', 'category', 'description', 'price', 'is_active']
        }),
        ('Available Sizes', {
            'fields': ['sizes'],
            'classes': ['wide']
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

    def display_sizes(self, obj):
        """Display the available sizes as a comma-separated string."""
        sizes = obj.get_available_sizes_display()
        if not sizes:
            return '-'
        return ', '.join(sizes)
    display_sizes.short_description = 'Available Sizes'

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    form = ProductColorAdminForm
    list_display = ['product', 'color_display', 'is_available']
    list_filter = ['is_available']
    search_fields = ['name', 'product__header']

    def color_display(self, obj):
        """Display the color as a colored circle with the name."""
        return format_html(
            '<div style="display: flex; align-items: center;">' +
            '<div style="width: 20px; height: 20px; border-radius: 50%; ' +
            'background-color: #{0}; margin-right: 10px; border: 1px solid #ccc;"></div>' +
            '{1}</div>',
            obj.name, obj.get_color_display_name()
        )
    color_display.short_description = 'Color'

    def has_delete_permission(self, request, obj=None):
        """Check if this color can be deleted."""
        if obj is None:
            return True  # Allow access to the delete action in general

        # Prevent deleting if this is the last color for the product
        can_delete = obj.product.colors.count() > 1

        # Add a message if this is the last color
        if not can_delete and request:
            from django.contrib import messages
            messages.warning(request, f"Cannot delete the color '{obj.name}' as it is the last color for the product '{obj.product.header}'. A product must have at least one color.")

        return can_delete
