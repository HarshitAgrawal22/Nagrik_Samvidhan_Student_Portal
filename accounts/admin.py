from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import StudentResource
from .models import Student, Instructor, Course, Roadmap

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ("username", "first_name", "last_name", "email")
#     exclude = ("password", "last_login", "is_superuser", "groups", "user_permissions", "is_staff", "is_active", "date_joined")
    
    
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ("username", "first_name", "last_name", "email")
    search_fields = ("username", "first_name", "last_name", "email", "mobile_number")
    list_filter = ("college", "is_changed_password", "courses")
    exclude = ("password", "last_login", "is_superuser", "groups", "user_permissions", "is_staff", "is_active", "date_joined")


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    exclude = ("password", "last_login", "is_superuser", "groups", "user_permissions", "is_active", "date_joined")

    


class RoadmapInline(admin.TabularInline):
    model = Roadmap
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "instructor")
    inlines = [RoadmapInline]


admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Roadmap)