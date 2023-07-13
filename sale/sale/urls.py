"""sale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home_view),
    path('register/', sabte_name),
    path('', log_in),
    path('forgot/', forgot_pass),
    path('order/', ordering),
    path('paneladmin/', panel_admin),
    path('add/', add_good),
    path('del/', delete_good),
    path('newUsers/', Registering_Users),
    path('log-in-admin/', log_in_admin),
    path('edit-info/', edit_info),
    path('newadmin/', new_admin),
    path('allorders/', all_orders),
    path('last-orders/', last_orders),
    path('edit-admin/', edit_info_admin),
    # path('edit-order/', edit_order),
    path('details/', show_details_order),
    path('user-order-details/', show_details_order2_user),
    path('new-order/', new_row_order),
]
