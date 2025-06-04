from django import forms
from .models import Product, ProductColor
from .widgets import ColorCircleWidget

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['header', 'category', 'description', 'price', 'is_active']


class ProductColorAdminForm(forms.ModelForm):
    """Custom form for ProductColor in admin with color circles."""

    class Meta:
        model = ProductColor
        fields = ['product', 'name', 'image', 'is_available']
        widgets = {
            'name': ColorCircleWidget(attrs={'class': 'color-circle-widget'})
        }
