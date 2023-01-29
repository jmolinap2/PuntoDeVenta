from django.urls import path

from core.login.views import *

urlpatterns = [
    path('', LoginAuthView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    path('update/password/<str:token>/', UpdatePasswordView.as_view(), name='update_password')
]
