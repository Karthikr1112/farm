from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('submit-inquiry/', views.submit_inquiry, name='submit_inquiry'),
    path('orders/', views.orders_dashboard, name='orders_dashboard'),
    path('orders/<int:order_id>/complete/', views.complete_order, name='complete_order'),
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('orders/export/', views.export_orders_csv, name='export_orders_csv'),
    path('order/', views.order_page, name='order_page'),
]
