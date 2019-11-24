"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("account/", views.account, name="account"),
    path("userpage/", views.userpage, name="userpage"),
    path("friends_form/", views.friends_form, name="friends_form"),
    path("friendspage/", views.friendspage, name="friendspage"),
    path("transaction_form/", views.transaction_form, name="transaction_form"),
    path("flist/", views.flist, name="flist"),
    path("insight", views.insight, name="insight"),
    path("thokka/<str:name>", views.thokka, name="thokka"),
    re_path("get_user_profile/", views.get_user_profile, name="get_user_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
