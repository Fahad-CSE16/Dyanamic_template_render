from django import forms
from userapp.models import BaseModel

class BaseModelForm(forms.ModelForm):
    class Meta:
        model = BaseModel
        exclude = ['created_at', 'updated_at', 'created_by', 'updated_by']