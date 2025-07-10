# catalog/forms.py

from django import forms
from .models import Brand  # ← make sure you have a Brand model

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = [
            "name",
            # add whatever other fields your Brand model has:
            # "description",
            # "status",
            # etc.
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            # customize other widgets if needed
        }
