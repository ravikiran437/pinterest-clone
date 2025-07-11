from django.urls import path

from . import views

urlpatterns = [
    path('signin/', views.signin_view, name="signin"),
    path('signup/', views.signup_view, name="signup"),
    path('home/', views.home_view, name="home"),
    path('logout/', views.logout_view, name='logout'),
    path('pin/<int:pin_id>/', views.specific_view, name='specific'),
    path('user-details/',views.user_view,name="user-details"),
]
