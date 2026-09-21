from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Game Logic
    path('', views.lobby_view, name='lobby'),
    path('create/', views.create_game_view, name='create_game'),
    path('game/<int:game_id>/', views.game_detail_view, name='game_detail'),
    path('game/<int:game_id>/join/', views.join_game_view, name='join_game'),
    path('game/<int:game_id>/start/', views.start_game_view, name='start_game'),

    # Profile & Stats Placeholder Views
    path('profile/', TemplateView.as_view(template_name="profile.html"), name='profile'),
    path('leaderboard/', TemplateView.as_view(template_name="base.html"), name='leaderboard'),
    path('stats/<str:username>/', TemplateView.as_view(template_name="base.html"), name='player_statistics'),
]
