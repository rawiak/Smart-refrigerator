from django.views import View
from .models import Product, Category
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ProductForm, CategoryForm, SearchForm

class ProductsView(View):

    def get(self, request):
        products = Product.objects.all().order_by('name')
        ctx = {'products':products}
        return render(request, 'refrigerator/products.html', ctx)

class CategoryView(View):

    def get(self, request, id):
        category = Category.objects.get(pk=id)
        products = Product.objects.filter(categories=category)
        ctx = { 'category':category,
                'products': products}
        return render(request, 'refrigerator/category.html', ctx)

class ProductView(View):

    def get(self, request, id):
        product=Product.objects.get(pk=id)
        ctx = {'product': product}
        return render(request, 'refrigerator/product.html', ctx)

class AddProductView(View):

    def get(self, request):
        form = ProductForm()
        ctx = {'form':form}
        return render(request, 'refrigerator/add_product.html', ctx)

    def post(self, request):
        form = CategoryForm(data = request.POST)
        ctx = {'form':form}
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            quantity = form.cleaned_data['quantity']
            expiration_date = form.cleaned_data['expiration_date']

            product = Product.objects.create(
                name=name,
                description=description,
                quantity=quantity,
                expiration_date=expiration_date
            )

            return HttpResponseRedirect(product.get_absolute_url())

        return render(request,'refrigerator/add_product.html', ctx)
