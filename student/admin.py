from django.contrib import admin
from .models import Session, Notification, Anonymous_Message, Notes, Feedback, Assignment, AssignmentSubmission

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("topic", "course", "instructor", "session_time", "is_completed")
    

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'expiration_date', 'is_fixed', 'is_alert')
    list_filter = ('type', 'is_fixed')
    search_fields = ('title', 'description')
    
@admin.register(Anonymous_Message)
class Anonymous_MessageAdmin(admin.ModelAdmin):
    list_display = ('student', 'instructor', 'message', "is_replied")
    search_fields = ('student', 'instructor', 'message')
    
@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject')
    search_fields = ('student',)
    
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date')
    search_fields = ('title', 'course')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', "status")
    search_fields = ('assignment', 'student', "status")
