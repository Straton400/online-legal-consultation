from django.urls import path
from . import views
from .views import lawyer_register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('lawyer-register/', lawyer_register, name='lawyer_register'),
    path('lawyer-login/', views.lawyer_login, name='lawyer_login'),
    path('dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer-logout/', views.lawyer_logout, name='lawyer_logout'),
    path('create-profile/', views.create_lawyer_profile, name='create_lawyer_profile'),
    path('lawyers/', views.lawyer_list, name='lawyer_list'),
    path('about/', views.about_page, name='about'),
    path('legal-news/', views.legal_news, name='legal_news'),
    path('legal-news/<int:pk>/', views.legal_news_detail, name='legal_news_detail'),
    path('client-register/', views.client_register, name='client_register'),
    path('client-login/', views.client_login, name='client_login'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)