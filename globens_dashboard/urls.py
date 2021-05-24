"""globens_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('pp/', views.handle_privacy_policy, name='privacy-policy'),

    path('', views.handle_main_page, name='main-page'),
    path('contents/', views.handle_contents_page, name='contents-page'),
    path('approve/', views.handle_product_approve, name='approve'),
    path('disapprove/', views.handle_product_disapprove, name='disapprove'),

    path('accounts/login/', views.handle_login_api, name='login'),
    path('accounts/logout/', views.handle_logout_api, name='logout'),
]
