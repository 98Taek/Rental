from django.urls import path, include

from account import views

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
]
