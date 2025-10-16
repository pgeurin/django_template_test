from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('debug/oauth/', views.debug_oauth, name='debug_oauth'),
    path('api/example/', views.api_example, name='api_example'),
    path('api/protected/', views.api_protected, name='api_protected'),
]