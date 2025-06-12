from django.urls import path
from . import views
from .views import lawyer_register
from django.conf import settings
from django.conf.urls.static import static
from .views import consultation_requests_view, update_consultation_status, client_consultations_view,Notification
from .views import delete_consultation



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
        
    path('lawyer/consultation-requests/', consultation_requests_view, name='consultation_requests'),
    path('update-consultation-status/<int:consultation_id>/', update_consultation_status, name='update_consultation_status'),


    path('lawyer/consultation/<int:pk>/', views.consultation_detail_view, name='consultation_detail'),
    
    path('request-consultation/<int:lawyer_id>/', views.request_consultation, name='request_consultation'),

    path('my-consultations/', client_consultations_view, name='client_consultations'),

    # path('delete-consultation/<int:consultation_id>/', delete_consultation, name='delete_consultation'),

    path('delete-consultation/<int:consultation_id>/', views.delete_consultation, name='delete_consultation'),
    path('client/logout/', views.client_logout, name='client_logout'),

    path('consultation-history/', views.consultation_history_view, name='consultation_history'),

    path('client/consultations/', views.client_consultations_view, name='client_consultations_view'),

    path('client/notifications/', views.client_notifications, name='client_notifications'),


    path('client/find-lawyer/', views.find_lawyer, name='find_lawyer'),

    path('client/provide-feedback/', views.provide_feedback, name='provide_feedback'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)