# catalog/forms.py

from django import forms
from django.forms import modelformset_factory
from .models import UnitOfMeasure

from django import forms

class BootstrapFormMixin:
    """
    Mixin to add 'form-control' to every field widget.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()

# Create Brands
from django import forms
from django.core.exceptions import ValidationError
from .models import Brand

class BrandForm(forms.ModelForm,BootstrapFormMixin):
    class Meta:
        model = Brand
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand name'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        # case‐insensitive check for duplicates
        if Brand.objects.filter(name__iexact=name).exists():
            raise ValidationError("A brand with this name already exists.")
        return name

