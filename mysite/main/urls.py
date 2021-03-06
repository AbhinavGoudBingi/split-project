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
    url(r'^select2/', include('django_select2.urls')),
    path("settleup_ingroup/<str:group_name>", views.settleup_ingroup, name="settleup_ingroup"),
    path("group_form/", views.group_form, name="group_form"),
    path("process_group_form/", views.process_group_form, name="process_group_form"),
    # path("group_transaction_form/<str:thisgroup_name>", views.group_transaction_form, name="group_transaction_form"),
    path("process_group_transaction/<str:thisgroup_name>", views.process_group_transaction, name="process_group_transaction"),
    path("groupslistpage/", views.groupslistpage, name="groupslistpage"),
    path("grouppage/<str:group_name>", views.grouppage, name="grouppage"),
    path("ouredirect/<str:name>", views.ouredirect, name="ouredirect"),
    path("settleup/<str:name>", views.settleup, name="settleup"),
    path("leave_group/<str:group_name>",views.leave_group,name="leave_group"),
    path("delete_group/<str:group_name>",views.delete_group,name="delete_group"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
