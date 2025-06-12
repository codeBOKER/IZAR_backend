from django import forms
from .models import Product, ProductColor, Category
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


class CategoryAdminForm(forms.ModelForm):
    sizes = forms.MultipleChoiceField(
        choices=Category.SIZES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Available Sizes"
    )

    class Meta:
        model = Category
        fields = ['header', 'description', 'image', 'is_active', 'sizes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.sizes:
            self.initial['sizes'] = [s.strip() for s in self.instance.sizes.split(',') if s.strip()]

    def clean_sizes(self):
        return ','.join(self.cleaned_data['sizes'])
