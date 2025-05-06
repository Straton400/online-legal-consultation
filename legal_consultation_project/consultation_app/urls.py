from django.urls import path
from . import views
from .views import lawyer_register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('lawyer-register/', lawyer_register, name='lawyer_register'),
    path('lawyer-login/', views.lawyer_login, name='lawyer_login'),
    path('lawyer-dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer-logout/', views.lawyer_logout, name='lawyer_logout'),
    path('create-profile/', views.create_lawyer_profile, name='create_lawyer_profile'),
    path('lawyers-list/', views.lawyer_list, name='lawyer_list'),
    path('about/', views.about_page, name='about'),
    path('client-register/', views.client_register, name='client_register'),
    path('client-login/', views.client_login, name='client_login'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('legal-news/', views.legal_news_list, name='legal_news_list'),
    path('lawyer/<int:pk>/', views.lawyer_detail, name='lawyer_detail'),
    path('legal-news/<slug:slug>/', views.legal_news_detail, name='legal_news_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)