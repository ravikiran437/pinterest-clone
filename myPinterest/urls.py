from django.urls import path

from . import views

urlpatterns = [
    path('signin/', views.signin_view, name="signin"),
    path('signup/', views.signup_view, name="signup"),
    path('home/', views.home_view, name="home"),
    path('logout/', views.logout_view, name='logout'),
    path('pin/<int:pin_id>/', views.specific_view, name='specific'),
    path('user-details/',views.user_view,name="user-details"),
    path('toggle-save/<int:pin_id>/', views.toggle_save, name='toggle_save'),
    path('like/<int:pin_id>/', views.likes_view, name='like'),
    path('comment/<int:pin_id>/', views.comments_view, name='comments_views'),
    path('create-post',views.create_view,name="create-post"),
    path('download-pin/', views.download_pin, name='download_pin'),
]
