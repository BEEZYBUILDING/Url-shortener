from django.urls import path
from . import views

app_name = 'swiftlink'

urlpatterns = [
    path('', views.shortener, name='home'),
    path('<str:short_key>/', views.redirect_url, name='redirect')
]