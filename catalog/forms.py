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

from .models import UnitOfMeasure

class UnitOfMeasureForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model  = UnitOfMeasure
        fields = ['name', 'abbreviation']
        widgets = {
            'name':         forms.TextInput(attrs={'placeholder':'UoM name'}),
            'abbreviation': forms.TextInput(attrs={'placeholder':'e.g. kg, pcs'}),
        }

from django import forms
from .models import TaxRate
from .forms import BootstrapFormMixin  # your mixin from before

class TaxRateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model  = TaxRate
        fields = ['name', 'rate']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'GST Name'}),
            'rate': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g. 18.00'}),
        }
