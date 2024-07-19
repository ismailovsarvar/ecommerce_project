from django.urls import path

from customer.views.auth import LoginPageView, logout_page, RegisterView, activate
from customer.views.customer_views import (
    CustomerTemplateView,
    AddCustomerTemplateView,
    DeleteCustomerTemplateView,
    EditCustomerTemplateView,
    ExportDataTemplateView,
)

urlpatterns = [
    path('customer-list/', CustomerTemplateView.as_view(), name='customers'),
    path('add-customer/', AddCustomerTemplateView.as_view(), name='add_customer'),
    path('customer/<int:pk>/delete', DeleteCustomerTemplateView.as_view(), name='delete'),
    path('customer/<int:pk>/update', EditCustomerTemplateView.as_view(), name='edit'),
    # Authentication path
    path('login-page/', LoginPageView.as_view(), name='login'),
    path('logout-page/', logout_page, name='logout'),
    path('register-page/', RegisterView.as_view(), name='register'),
    path('export-data/', ExportDataTemplateView.as_view(), name='export_data'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
