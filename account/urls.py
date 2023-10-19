from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('referral-links/', views.referral_links, name='referral-links'),
]
