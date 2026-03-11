from django import forms
from .models import Category, Entry

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['term', 'definition']