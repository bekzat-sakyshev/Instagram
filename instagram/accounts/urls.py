from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('user/<int:id>/', views.UserDetailView.as_view(), name='profile'),
    path('update', views.UserUpdateView.as_view(), name='user_update'),
    path('change_password', views.ChangePasswordView.as_view(), name='change_password'),
    path('users/followers/<int:id>', views.UserListView.as_view(), name='users_followers'),
    path('users/subscriptions/<int:id>', views.UserListView.as_view(), name='users_sub'),
]
