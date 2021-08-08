from django.urls.conf import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('user/', views.userPage, name='userpage'),
    path('settings/', views.settingsUser, name='settingsuser'),

    path('customer/<str:pk>/', views.customer, name='customer'),
    path('created_order/<str:pk>/', views.created_order, name='created_order'),
    path('upgrade_order/<str:pk>/', views.upgrade_order, name='upgrade_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name = 'password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name = 'password_reset_complete'),
]