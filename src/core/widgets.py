from django.forms.widgets import Select
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class ColorCircleWidget(Select):
    template_name = 'admin/widgets/color_circle.html'
    
    def __init__(self, attrs=None, choices=()):
        attrs = attrs or {}
        attrs['class'] = f"{attrs.get('class', '')} color-circle-widget".strip()
        super().__init__(attrs, choices)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if 'id' not in attrs:
            context['widget']['attrs']['id'] = f'id_{name}'
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(render_to_string(self.template_name, context))
