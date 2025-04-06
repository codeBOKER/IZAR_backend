from django import forms
from .models import Product, ProductColor
from .widgets import ColorCircleWidget

class ProductAdminForm(forms.ModelForm):
    """Custom form for Product in admin with user-friendly size selection."""

    # Create a multiple choice field for sizes
    sizes = forms.MultipleChoiceField(
        choices=Product.SIZES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select the available sizes for this product."
    )

    class Meta:
        model = Product
        fields = ['header', 'category', 'description', 'price', 'is_active']
        exclude = ['available_sizes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we're editing an existing product, initialize the sizes field
        if self.instance.pk and self.instance.available_sizes:
            self.initial['sizes'] = self.instance.available_sizes

    def save(self, commit=True):
        # Save the selected sizes to the JSONField
        product = super().save(commit=False)
        product.available_sizes = self.cleaned_data.get('sizes', [])

        if commit:
            product.save()

        return product

class ProductColorAdminForm(forms.ModelForm):
    """Custom form for ProductColor in admin with color circles."""

    class Meta:
        model = ProductColor
        fields = ['product', 'name', 'image', 'is_available']
        widgets = {
            'name': ColorCircleWidget(attrs={'class': 'color-circle-widget'})
        }
