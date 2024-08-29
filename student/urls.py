from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="student"),
    
    # ========================= SESSION WORK =========================
    
    path("my_sessions/", views.my_sessions, name="my_sessions"),    
    
    # ========================= LEARNING WORK =========================
    
    path("playground", views.playground, name="playground"),
    path("reading_material", views.reading_material, name="reading_material"),
    path("roadmap", views.roadmap, name="roadmap"),
    path("view_roadmap/<int:course_id>", views.view_roadmap, name="view_roadmap"),
    
    path("assignments", views.assignments, name="assignments"),
    path("submit_assignment/<int:assignment_id>", views.submit_assignment, name="submit_assignment"),
    path("assignments/<int:assignment_id>/submission", views.view_submission, name="view_submission"),
    path("delete_submission/<int:submission_id>", views.delete_submission, name="delete_submission"),
        
    # ========================= PROFILE WORK =========================
    path("my_profile/", views.my_profile, name="my_profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('upload_profile', views.upload_profile, name='upload_profile'),
    path("change_password", views.change_password, name="change_password"),
    
    # ======================== HELP DESK WORK ========================
    
    path("notifications/", views.notifications, name="notifications"),
    path("anonymous_message/", views.anonymous_message, name="anonymous_message"),
    path("new_message", views.new_message, name="new_message"),
    path("feedback", views.feedback, name="feedback"),
    
]
 
