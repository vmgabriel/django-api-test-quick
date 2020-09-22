"""
Module for use of Bills Urls
"""

# Libraries
from django.urls import path, include
from django.http import Http404

# Views
from . import views

urlpatterns = [
    # Client
    path('clients', views.ClientListView.as_view(), name='clients'),
    path(
        'clients/<int:pk>',
        views.ClientDetailView.as_view(),
        name='client_by_id'
    ),

    # Product
    path('products', views.ProductListView.as_view(), name='products'),
    path(
        'products/<int:pk>',
        views.ProductDetailView.as_view(),
        name='product_by_id'
    ),

    # Bill
    path('bills', views.BillListView.as_view(), name='bills'),
    path(
        'bills/<int:pk>',
        views.BillDetailView.as_view(),
        name='bill_by_id'
    ),
]
