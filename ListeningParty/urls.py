"""Music URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path, include
from home.views import home_view
from login.views import login_view, logout_view, signup_view
from search.views import search_view
from party.views import party_view

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('logout/', logout_view),
    path('search/', search_view),
    path('signup/', signup_view),
    re_path(r"^p/(?P<party_name>[\w.@+-0123456789]+)$", party_view)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)