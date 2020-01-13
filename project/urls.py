from django.contrib import admin
from django.urls import path, re_path
from tradeApi.views import *

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'auth/login/', LoginView.as_view(), name="auth-login"),
    re_path(r'auth/register/', RegisterUsersView.as_view(), name="auth-register"),
    re_path(r'user/get/by/token/', GetUserByTokenView.as_view(), name="user/get/by/token"),
    re_path(r'user/change/password/', ChangePasswordView.as_view(), name="user/change/password"),
    re_path(r'email/send/', SendEmailView.as_view(), name="email/send"),

    re_path(r'profile/create/', ProfileCreateView.as_view(), name="profile/create"),
    re_path(r'profile/rud/(?P<pk>\d+)/$', ProfileRudView.as_view(), name="profile/rud"),
    re_path(r'profile/get/by/user/(?P<user>\d+)/$', ProfileGetByUserView.as_view(), name="profile/get/by/user"),
    re_path(r'profile/list/', ProfileListView.as_view(), name="profile/list"),
    re_path(r'user/list/', UserListView.as_view(), name="user/list"),

    re_path(r'package/create/', PackageCreateView.as_view(), name="package/create"),
    re_path(r'package/rud/(?P<pk>\d+)/$', PackageRudView.as_view(), name="package/rud"),
    re_path(r'package/list/', PackageListView.as_view(), name="package/list"),
    re_path(r'robot/buy/', RobotBuyView.as_view(), name="robot/buy"),
    re_path(r'robot/finish/', RobotFinishedView.as_view(), name="robot/finish"),

    re_path(r'transaction/create/', TransactionCreateView.as_view(), name="transaction/create"),
    re_path(r'transaction/rud/(?P<pk>\d+)/$', TransactionRudView.as_view(), name="transaction/rud"),
    re_path(r'transaction/list/', TransactionListView.as_view(), name="transaction/list"),
]