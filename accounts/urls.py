from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.dashboard_view, name='dashboard'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('forgotPassword/', views.forgotPassword_views, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetpassword'),
    path('resetPassword_validate/<uidb64>/<token>/', views.resetPassword_validate, name='resetPassword_validate'),



]
