from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

app_name = 'swiftlink'

urlpatterns = [
    path('', views.shortener, name='home'),
    path('register/', views.register, name='register'),
    #path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='swiftlink/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<str:short_key>/', views.redirect_url, name='redirect'),
]