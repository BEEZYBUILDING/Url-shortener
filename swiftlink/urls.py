from django.urls import path 
from . import views

app_name = 'swiftlink'

urlpatterns = [
    path('<str:short_key>/', views.redirect_url, name='redirect')
]