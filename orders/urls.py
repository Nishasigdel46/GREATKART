from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('review/<str:order_number>/', views.review_order, name='review_order'),
    path ('payments/', views.payments, name='payments'),
    path('order-complete/<str:order_number>/', views.order_complete, name='order_complete'),

]
