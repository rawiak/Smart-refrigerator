from django.views import View
from .models import Product, Category
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import ProductForm, CategoryForm, SearchForm, AuthForm, RegisterProfileForm
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta, date

class ProductsView(LoginRequiredMixin, View):

    def get(self, request):
        products = Product.objects.all().order_by('expiration_date')

        ctx = {'products':products}
        return render(request, 'refrigerator/products.html', ctx)





class ProductView(LoginRequiredMixin, View):

    def get(self, request, id):
        product=Product.objects.get(pk=id)
        date_now = date.today()
        end_date = product.expiration_date
        date = date_now - end_date
        ctx = {'product': product,
                'date':date}
        return render(request, 'refrigerator/product.html', ctx)

    def post(self, request, id):
        product = Product.objects.get(pk=id)
        form = ProductForm(data = request.POST)
        ctx = {'product': product}
        if request.POST.get('wyjmij'):
            if product.quantity == 1:
                product.delete()
                return HttpResponseRedirect('/')
            else:
                product.quantity = product.quantity - 1
                product.save()
                return render(request,'refrigerator/product.html', ctx)


class CategoryView(LoginRequiredMixin, View):

    def get(self, request, id):
        category = Category.objects.get(pk=id)
        products = Product.objects.filter(categories=category)
        ctx = { 'category':category,
                'products': products}
        return render(request, 'refrigerator/category.html', ctx)

class CategoriesView(LoginRequiredMixin, View):

    def get(self, request):
        categories = Category.objects.all().order_by('category_name')
        ctx = {'categories':categories}
        return render(request, 'refrigerator/categories.html', ctx)


class ProductSearchView(LoginRequiredMixin, View):

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

class ModifyCategoryView(LoginRequiredMixin, View):

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

class AddProductView(LoginRequiredMixin, View):
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

class AddCategoryView(LoginRequiredMixin, View):

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

class DeleteProductView(LoginRequiredMixin, View):
    pass

class RecipesView(LoginRequiredMixin, View):

    def get(self, request):
        products = Product.objects.all().order_by('name')
        ctx = {'products':products}
        return render(request, 'refrigerator/recipes.html', ctx)

class RecipesDinnerView(LoginRequiredMixin, View):
    pass
class RecipesSupperView(LoginRequiredMixin, View):
    pass
class RecipesBreakfastView(LoginRequiredMixin, View):
    pass
class AddRecipesView(LoginRequiredMixin, View):
    pass


class RegisterProfileView(View):

    def get(self, request):
        form = RegisterProfileForm()
        ctx = {'form':form}
        return render(request, 'refrigerator/register_profile_form.html', ctx)

    def post(self, request):
        form = RegisterProfileForm(data=request.POST)
        ctx = {'form':form}
        if form.is_valid():
            profile = form.save()
            login(request, profile)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'refrigerator/register_profile_form.html', ctx)


class LoginView(View):
    def get(self, request):
        form = AuthForm()
        ctx={'form':AuthForm()}
        return render(request, 'refrigerator/login.html', ctx)

    def post(self, request):
        form = AuthForm(data = request.POST)
        ctx = {'form':form}
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'refrigerator/login.html', ctx)

class LogoutView(View):

    def get(self, request):
        request.user.is_authenticated
        logout(request)
        return HttpResponseRedirect(reverse('login'))
