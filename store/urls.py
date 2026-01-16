from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),  # main store page
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
        path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),  # <- this is required
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart')

]


