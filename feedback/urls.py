from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('company/<int:company_id>/', views.detail, name='detail'),
    path('company/<int:company_id>/feedback/', views.add_feedback, name='add_feedback'),
    path('fusion/', views.fusion_chart, name='fusion_chart'),
]
