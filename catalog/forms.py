# catalog/forms.py

from django import forms
from django.forms import modelformset_factory
from .models import UnitOfMeasure

# A ModelForm for a single UoM
class UnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ('name', 'abbreviation')

# A formset to edit/create/delete multiple UoMs at once
UnitOfMeasureFormSet = modelformset_factory(
    UnitOfMeasure,
    form=UnitOfMeasureForm,
    extra=2,          # two blank forms to start
    can_delete=True   # allow marking rows for deletion
)

# Create Brands
from django import forms
from django.core.exceptions import ValidationError
from .models import Brand

class BrandForm(forms.ModelForm):
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

