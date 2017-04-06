from django import forms
from .models import Product, Category
from django.contrib.admin import widgets
import datetime
from django.forms.extras.widgets import SelectDateWidget

category_choices = Category.objects.all().values_list('id','category_name').order_by('category_name')

class CategoryForm(forms.Form):
    category_name = forms.CharField(label = 'Nazwa kategorii: ', max_length=64)

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields =['name','description','quantity','expiration_date', 'category']

class ProductForm(forms.Form):
    name = forms.CharField(max_length=64, label = "Nazwa produktu: ")
    description = forms.CharField(label ='Opis')
    quantity = forms.IntegerField(label ='Ilość:')
    expiration_date = forms.DateField(widget = SelectDateWidget, label = "Data ważności: ")
    category = forms.ChoiceField(choices=category_choices, label='Kategoria')

class SearchForm(forms.Form):
    name = forms.CharField(label = "Nazwa produktu", max_length=64)
