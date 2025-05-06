from django.urls import path
from . import views
from .views import delete_lawyer, view_lawyer_profile

urlpatterns = [
    path('', views.admin_dashboard, name='admin-dashboard'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-lawyers/', views.manage_lawyers, name='manage_lawyers'),
    path('verify-lawyer/<int:lawyer_id>/', views.verify_lawyer, name='verify_lawyer'),
    path('adminpanel/lawyers/delete/<int:lawyer_id>/', delete_lawyer, name='delete_lawyer'),
    path('admin/lawyers/<int:lawyer_id>/view/', views.view_lawyer_profile, name='view_lawyer_profile'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('manage-clients/', views.admin_clients_view, name='admin_clients'),
    path('clients/view/<int:client_id>/', views.admin_view_client, name='admin_view_client'),
    path('clients/delete/<int:client_id>/', views.admin_delete_client, name='admin_delete_client'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin/articles/add/', views.admin_add_article, name='admin_add_article'),


 
]
