from django.urls import path, include
from . import views
urlpatterns = [
    path('singup/', views.SignUpView.as_view(), name = 'singup'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
]
