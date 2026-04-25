"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from accounts import views

# Override admin default permission logic:
# Ensure only users with explicitly given role 'admin' can access /admin/
def custom_has_permission(request):
    if not request.user.is_authenticated:
        return False
    # You are allowed in if you are a superuser OR your role is admin
    return request.user.is_superuser or getattr(request.user, 'role', '') == 'admin'

admin.site.has_permission = custom_has_permission

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
]