from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from feedback import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(
        template_name='feedback/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='/login/'
    ), name='logout'),

    # Home (role based)
    path('', views.home, name='home'),

    # Feedback
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
]
