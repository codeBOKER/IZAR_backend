from django import forms
from .models import Product, ProductColor, Category
from .widgets import ColorCircleWidget

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['header', 'category', 'description', 'price', 'is_active']


class ProductColorAdminForm(forms.ModelForm):
    """Custom form for ProductColor in admin with color circles and file upload."""
    image_upload = forms.FileField(required=False, label="Upload Image (will be uploaded to Imgur)")

    class Meta:
        model = ProductColor
        fields = ['product', 'name', 'image', 'is_available']
        widgets = {
            'name': ColorCircleWidget(attrs={'class': 'color-circle-widget'})
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image_upload')
        if image_file:
            from .utils import upload_image_to_imgur
            instance.image = upload_image_to_imgur(image_file)
        if commit:
            instance.save()
        return instance


class CategoryAdminForm(forms.ModelForm):
    sizes = forms.MultipleChoiceField(
        choices=Category.SIZES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Available Sizes"
    )
    image_upload = forms.FileField(required=False, label="Upload Image (will be uploaded to Imgur)")

    class Meta:
        model = Category
        fields = ['header', 'description', 'image', 'is_active', 'sizes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.sizes:
            self.initial['sizes'] = [s.strip() for s in self.instance.sizes.split(',') if s.strip()]

    def clean_sizes(self):
        return ','.join(self.cleaned_data['sizes'])

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image_upload')
        if image_file:
            from .utils import upload_image_to_imgur
            instance.image = upload_image_to_imgur(image_file)
        if commit:
            instance.save()
        return instance
