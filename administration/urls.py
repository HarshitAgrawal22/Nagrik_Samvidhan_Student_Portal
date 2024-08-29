from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="administration"),
    path("instructor_sessions/", views.instructor_sessions, name="instructor_sessions"),
    
    # ========================= ASSIGNMENTS WORK ==========================
    
    path("instructor_assignments/", views.instructor_assignments, name="instructor_assignments"),
    path("add_assignment/", views.add_assignment, name="add_assignment"),
    path("submissions/<int:id>/", views.view_submissions, name="view_submissions"),
    path("delete_assignment/<int:id>/", views.delete_assignment, name="delete_assignment"),
    
    
    # ========================= SESSIONS WORK=========================
    
    path("add_session/", views.add_session, name="add_session"),
    path("edit_session/<int:id>/", views.edit_session, name="edit_session"),
    path("mark_session_completed/<int:id>/", views.mark_session_completed, name="mark_session_completed"),
    path('upload-recorded-session/', views.upload_recorded_session, name='upload_recorded_session'),
    
    # ========================= DATA WORK ============================
    
    path("all_students/", views.all_students, name="all_students"),

    # ========================= NOTIFICATIONS WORK ==========================
    
    path("notifications/", views.notifications, name="instructor_notifications"),
    path("delete_notification/<int:id>/", views.delete_notification, name="delete_notification"),
    path("edit_notification/<int:id>/", views.edit_notification, name="edit_notification"),
    
    # ========================= ANONYMOUS MESSAGES WORK ==========================
    
    path("messages/", views.instructor_anonymous_message, name="instructor_anonymous_message"),
    path("reply_message/<int:id>/", views.reply_message, name="reply_message"),
    path("edit_reply/<int:id>/", views.edit_reply, name="edit_reply"),
    
    # ========================= PROFILE WORK =========================
    path("instructor_profile/", views.instructor_profile, name="instructor_profile"),
    path("edit_instructor_profile/", views.edit_instructor_profile, name="edit_instructor_profile"),
    path('upload_instructor_profile', views.upload_instructor_profile, name='upload_instructor_profile'),
    path("change_instructor_password", views.change_instructor_password, name="change_instructor_password"),
    
]