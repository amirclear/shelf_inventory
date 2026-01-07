from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Landing and Auth
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Detection
    path('upload-detect/', views.upload_detect, name='upload_detect'),
    path('detect-result/<int:pk>/', views.detect_result, name='detect_result'),
    path('generate-invoice/<int:detection_pk>/', views.generate_invoice, name='generate_invoice'),
    
    # Invoices
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
]

