"""
URL configuration for medi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('user_reg/', views.user_reg),
    path('pharmacy_reg/', views.pharmacy_reg),
    
    # Pharmacy
    path('pharmacy_home/', views.pharmacy_home),
    path('add_medicine/', views.add_medicine),
    path('manage_medicine/', views.manage_medicine),
    path('edit_medicine/', views.edit_medicine),
    path('delete_medicine/', views.delete_medicine),
    path('pharmacy_bookings/', views.pharmacy_bookings),
    path('pharmacy_booking_details/', views.pharmacy_booking_details),
    path('pharmacy_feedbacks/', views.pharmacy_feedbacks),
    path('add_delivery_boy/', views.add_delivery_boy),
    path('view_delivery_boys/', views.view_delivery_boys),
    path('delete_delivery_boy/', views.delete_delivery_boy),
    path('pharmacy_profile/', views.pharmacy_profile),
    
    # Delivery
    path('delivery_home/', views.delivery_home),
    path('delivery_deliveries/', views.delivery_deliveries),
    
    # User
    path('user_home/', views.user_home),
    path('view_shops/', views.view_shops),
    path('view_medicines/', views.view_medicines),
    path('book_medicine_qty/', views.book_medicine_qty),
    path('my_bookings/', views.my_bookings),
    path('cancel_booking/', views.cancel_booking),
    path('make_payment/', views.make_payment),
    path('bill/', views.bill),
    path('user_feedback/', views.user_feedback),
    path('user_report/', views.user_report),
    path('confirm_delivery/', views.confirm_delivery),
    path('user_profile/', views.user_profile),
    path('my_invoices/', views.my_invoices),
    
    # Admin
    path('admin_home/', views.admin_home),
    path('manage_pharmacy/', views.manage_pharmacy),
    path('view_users/', views.view_users),
    path('view_feedbacks/', views.view_feedbacks),
    path('view_reports/', views.view_reports),
    path('admin_view_deliveries/', views.admin_view_deliveries),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

