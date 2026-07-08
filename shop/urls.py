from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('management/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]