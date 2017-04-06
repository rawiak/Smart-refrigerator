from django.views import View
from .models import Product, Category
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ProductForm, CategoryForm, SearchForm
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy

class ProductsView(View):

    def get(self, request):
        products = Product.objects.all().order_by('name')
        ctx = {'products':products}
        return render(request, 'refrigerator/products.html', ctx)

class ProductView(View):

    def get(self, request, id):
        product=Product.objects.get(pk=id)
        ctx = {'product': product}
        return render(request, 'refrigerator/product.html', ctx)

class CategoryView(View):

    def get(self, request, id):
        category = Category.objects.get(pk=id)
        products = Product.objects.filter(categories=category)
        ctx = { 'category':category,
                'products': products}
        return render(request, 'refrigerator/category.html', ctx)

class CategoriesView(View):

    def get(self, request):
        categories = Category.objects.all().order_by('category_name')
        ctx = {'categories':categories}
        return render(request, 'refrigerator/categories.html', ctx)


class ProductSearchView(View):

    def get(self, request):
        ctx = {'form': SearchForm()}
        return render(request, 'refrigerator/product_search.html', ctx)

    def post(self, request):
        form = SearchForm(data=request.POST)
        ctx = {'form':form}
        if form.is_valid():
            name = form.cleaned_data['name']
            products = Product.objects.filter(name__icontains = name)
            ctx ['results'] = products

        return render(request,'refrigerator/product_result.html', ctx)

class ModifyCategoryView(View):

    def get(self, request, id):
        category=Category.objects.get(id=id)
        form = CategoryForm(initial={
        'category_name':category.category_name,
        'id':category.id})
        ctx = {'form':form,
                'category':category}
        return render(request, 'refrigerator/modify_category.html', ctx)

    def post(self, request, id):
        category=Category.objects.get(id=id)
        form = CategoryForm(data = request.POST)
        ctx = {'form':form,
                'category':category}

        if form.is_valid():
            category.category_name = form.cleaned_data['category_name']
            category.id = form.cleaned_data['id']
            category.save()
            return HttpResponseRedirect('/')

        return render(request,'refrigerator/categories.html', ctx)

class AddProductView(View):
    def get(self, request):
        ctx = {'form': ProductForm()}
        return render(request, 'refrigerator/add_product.html', ctx)

    def post(self, request):
        form = ProductForm(data = request.POST)
        ctx = {'form':form}
        if form.is_valid():
            product_name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            quantity = form.cleaned_data['quantity']
            expiration_date = form.cleaned_data['expiration_date']
            category_id=form.cleaned_data['category']
            category=Category.objects.get(id=category_id)
            try:
                product = Product.objects.get(name=product_name)
                product.quantity += quantity
                product.save()
            except Exception:
                product = Product.objects.create(
                name=product_name,
                description=description,
                quantity=quantity,
                expiration_date=expiration_date,
                category_id=category.id
            )

            return HttpResponseRedirect('/')

        return render(request,'refrigerator/add_product.html', ctx)

class AddCategoryView(View):

    def get(self, request):
        form = CategoryForm()
        ctx = {'form':form}
        return render(request, 'refrigerator/add_category.html', ctx)

    def post(self, request):
        form = CategoryForm(data = request.POST)
        ctx = {'form':form}
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = Category.objects.create(
                category_name=category_name,
            )

            return HttpResponseRedirect('/')

        return render(request,'refrigerator/categories.html', ctx)

class DeleteProductView(DeleteView):
    model = Product
    success_url = reverse_lazy ('products')
