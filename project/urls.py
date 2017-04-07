"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from refrigerator.views import(
    AddProductView,
    ProductsView,
    ProductView,
    ProductSearchView,
    CategoryView,
    CategoriesView,
    ModifyCategoryView,
    AddCategoryView,
    DeleteProductView,
    RecipesView,
    RecipesDinnerView,
    RecipesSupperView,
    RecipesBreakfastView,
    AddRecipesView,
    LoginView,
    LogoutView,
    RegisterProfileView
    )

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ProductsView.as_view(), name=""),
    url(r'^category/(?P<id>(\d)+)/$', CategoryView.as_view(), name='category'),
    url(r'^product/(?P<id>(\d)+)/$', ProductView.as_view(), name='product'),
    url(r'^add_product/$', AddProductView.as_view(), name='add-product'),
    url(r'^categories/', CategoriesView.as_view(), name='categories'),
    url(r'^product_search', ProductSearchView.as_view(), name='product-search'),
    url(r'^add_category/$', AddCategoryView.as_view(), name='add-category'),
    url(r'^modify_category/(?P<id>(\d)+)/$', ModifyCategoryView.as_view(), name='modify-category'),
    url(r'^delete_product/(?P<id>(\d)+)/$', DeleteProductView.as_view(), name='delete-product'),
    url(r'^recipes_breakfast/$', RecipesBreakfastView.as_view(), name='recipes-breakfast'),
    url(r'^recipes_dinner/$', RecipesDinnerView.as_view(), name='recipes-dinner'),
    url(r'^recipes_supper/$', RecipesSupperView.as_view(), name='recipes-supper'),
    url(r'^recipes/$', RecipesView.as_view(), name='recipes'),
    url(r'^add_recipes/$', AddRecipesView.as_view(), name='add-recipes'),

    url(r'^register/', RegisterProfileView.as_view(), name='register-profile'),
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^logout', LogoutView.as_view(), name='logout'),

]
