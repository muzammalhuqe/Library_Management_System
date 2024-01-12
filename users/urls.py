from django.urls import path, include
from . import views
urlpatterns = [
    path('singup/', views.SignUpView.as_view(), name = 'singup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # path('profile/edit', views.edit_profile, name='edit_profile'),
]
