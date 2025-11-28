from django.urls import path
from . import views

urlpatterns = [
    path('', views.billing_page, name='billing_page'),
    path('purchases/', views.previous_purchases, name='previous_purchases'),
    path('purchases/<int:bill_id>/', views.purchase_detail, name='purchase_detail'),
]
