from django.urls import path
from . import views

urlpatterns = [
    # ---------------- ROOT ----------------
    path('', views.home_redirect, name='home'),

    # ---------------- AUTH ----------------
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ---------------- RESIDENT ----------------
    path('resident/dashboard/', views.resident_dashboard, name='resident_dashboard'),
    path('resident/complaint/', views.submit_complaint, name='submit_complaint'),
    path('resident/document-request/', views.request_document, name='request_document'),
    path('resident/announcements/', views.view_announcements, name='view_announcements'),

    # ---------------- STAFF ----------------
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/complaint/respond/<int:id>/', views.respond_complaint, name='respond_complaint'),
    path('staff/document/<int:id>/status/<str:status>/', views.update_request_status, name='update_request_status'),
    path('staff/announcement/add/', views.add_announcement, name='add_announcement'),
]
