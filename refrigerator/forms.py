from django import forms
from .models import Product, Category, Profile
from django.contrib.admin import widgets
import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .validators import valid_range


category_choices = Category.objects.all().values_list('id','category_name').order_by('category_name')

class CategoryForm(forms.Form):
    category_name = forms.CharField(label = 'Nazwa kategorii: ', max_length=64)

class ProductForm(forms.Form):
    name = forms.CharField(max_length=64, label = "Nazwa produktu: ")
    description = forms.CharField(label ='Opis', required = False)
    quantity = forms.IntegerField(label ='Ilość:', validators=[valid_range])
    expiration_date = forms.DateField(widget = SelectDateWidget, label = "Data ważności: ")
    category = forms.ChoiceField(choices=category_choices, label='Kategoria')

class SearchForm(forms.Form):
    name = forms.CharField(label = "Nazwa produktu", max_length=64)


class AuthForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """
        Metoda dorzuca do cleaned_data instancję użytkownika podkluczem 'user'
        """
        cleaned_data = super().clean()

        login = cleaned_data['login']
        password = cleaned_data['password']
        user = authenticate(
            username=login, password=password
        )
        if user is None:
            raise forms.ValidationError('Nieprawidłowy login albo hasło')
        cleaned_data['user'] = user
        return cleaned_data


class RegisterProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

    def clean(self):
        cleaned_data = super().clean()
        raw_password = cleaned_data['password']
        cleaned_data['password'] = make_password(raw_password)

        return cleaned_data
