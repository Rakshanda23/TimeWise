from unicodedata import name
from django.urls import path, re_path
from . import views
import django.contrib.auth.views as views_aut

app_name = "generator"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "login/",
        views_aut.LoginView.as_view(template_name="generator/login.html"),
        name="login",
    ),
    path("home/", views.home, name="home"),
    path("teacher/", views.teacher, name="teacher"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("form1/<res_name>/", views.form1_view, name="form1"),
    path("form2/<res_name>/", views.form2_view, name="form2"),
    re_path(r"^timetable/(?P<resname>\d+)/$", views.generate_timetables, name="gen"),
]
