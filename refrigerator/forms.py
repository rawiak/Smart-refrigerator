from django import forms

class CategoryForm(forms.Form):
    category_name = forms.CharField(label = 'Nazwa kategorii: ', max_length=64)

class ProductForm(forms.Form):
    name = forms.CharField(max_length=64, label = "Nazwa produktu: ")
    description = forms.CharField(widget = forms.Textarea)
    quantity = forms.IntegerField()
    expiration_date = forms.DateTimeField(label = "Data ważności: ")

class SearchForm(forms.Form):
    search = forms.CharField(max_length=64)
