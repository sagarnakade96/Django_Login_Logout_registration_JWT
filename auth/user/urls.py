from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from user import views
from .views import RegisterView, LoginView,LogoutView
urlpatterns = [
    path('admin/',admin.site.urls),
    path("",views.home,name="home"),
    path("registerView",RegisterView.as_view()),
    path("loginView",LoginView.as_view()),
    path("logoutView",LogoutView.as_view()),
    path("loginPage",views.loginPage,name="loginPage"),
    path("registerPage",views.registerPage,name="registerPage"),
    path("registerUser",views.createUser,name="Register"),
    path("loginUser",views.loginUser,name="LoginUser"),
    path("logoutUser",views.logoutUser,name="LoginOut"),
    path("users",views.users,name="users")
]
