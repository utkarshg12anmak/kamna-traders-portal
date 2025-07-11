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
