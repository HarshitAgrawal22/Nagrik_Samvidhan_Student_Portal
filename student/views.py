from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.views import logout as account_logout
from django.utils import timezone
from django.db.models import Q

from accounts.models import Student, Instructor, Course
from student.models import Session, Notification, Anonymous_Message, Notes, Feedback, Assignment, AssignmentSubmission


# ========================================= DASHBOARD =========================================

@login_required(login_url="login")
def dashboard(request):
    

    sessions = Session.objects.filter(course__in=request.user.student.courses.all(), is_completed=False)
    last_3_completed_sessions = [session for session in Session.objects.order_by("-session_time").filter(is_completed=True) if session.recorded_session_link is not None][:3]
    
#    fetch only those notifications which are sent my the instructors of the courses the student is enrolled in
    notifications = Notification.objects.filter(expiration_date__gt=timezone.now(), is_alert=True)
    
    total_assignments = Assignment.objects.filter(course__in=request.user.student.courses.all()).count()
    completed_assignments = AssignmentSubmission.objects.filter(student=request.user.student).count()
    
    assignment_percentage = int((completed_assignments / total_assignments) * 100) if total_assignments != 0 else 0
    
    is_birthday = False
    if request.user.student.dob:
    
        
        if request.user.student.dob.day == timezone.now().day and request.user.student.dob.month == timezone.now().month:
            is_birthday = True
            
        
    
    parameters = {
        "sessions": sessions,
        "last_3_completed_sessions": last_3_completed_sessions,
        "notifications": notifications,
        "completed_assignments": completed_assignments,
        "assignment_percentage": assignment_percentage,
        "left_assignments": total_assignments - completed_assignments,
        "is_birthday": is_birthday
    }
    
    return render(request, "student/index.html", parameters)

# ========================================= MY SESSIONS =========================================

@login_required(login_url="login")
def my_sessions(request):
    
    sessions = Session.objects.filter(course__in=request.user.student.courses.all()).order_by("-session_time")
    
    query = request.POST.get("query")
    if query:
        sessions = sessions.filter(
            Q(topic__icontains=query)|
            Q(course__name__icontains=query) |
            Q(instructor__first_name__icontains=query) |
            Q(instructor__last_name__icontains=query) |
            Q(id__icontains=query)
            )
        
    parameters = {
        "sessions": sessions,
        "query": query 
    }
    
    return render(request, "student/my_sessions.html", parameters)

# ========================================= NOTIFICATIONS =========================================

@login_required(login_url="login")
def notifications(request):
    
    notifications = Notification.objects.order_by("-expiration_date")
    
    parameters = {
        "notifications": notifications
    }
    
    return render(request, "student/notifications.html", parameters)


# ========================================= ANONYMOUS MESSAGES =========================================

@login_required(login_url="login")
def anonymous_message(request):
    
    my_messages = Anonymous_Message.objects.filter(student=request.user.student)
    
    parameters = {
        "my_messages": my_messages
    }
    
    return render(request, "student/anonymous_message.html", parameters)


# ======================================= NEW MESSAGE ==================================================

@login_required(login_url="login")
def new_message(request):

    courses = request.user.student.courses.all()
    my_instructors = Instructor.objects.filter(course__in=courses).distinct()
    
    if request.method == "POST":
        instructor_id = request.POST.get("instructor")
        message = request.POST.get("message")
        
        instructor = Instructor.objects.get(id=instructor_id)
        
        if Anonymous_Message.objects.filter(student=request.user.student, instructor=instructor, is_replied=False).exists():
            messages.error(request, "You have already sent a message to this instructor! Wait until they reply!")
            return redirect("anonymous_message")
        
        Anonymous_Message.objects.create(
            student=request.user.student,
            instructor=instructor,
            message=message
        )
        
        messages.success(request, "Message sent successfully!")
        
        return redirect("anonymous_message")  
    
    parameters = {
        "my_instructors": my_instructors
    }
    
    return render(request, "student/new_message.html", parameters)


# ========================================== PLAYGROUND ===============================================

@login_required(login_url="login")
def playground(request):
    return render(request, "student/playground.html")

# =========================================== READING MATERIAL ========================================

@login_required(login_url="login")
def reading_material(request):
    
    notes = Notes.objects.filter(course__in=request.user.student.courses.all())
    
    parameters = {
        "notes": notes
    }
    
    return render(request, "student/reading_material.html", parameters)


# =========================================== ASSIGNMENTS =============================================

@login_required(login_url="login")
def assignments(request):
    
    assignments= Assignment.objects.filter(course__in=request.user.student.courses.all())
    student = request.user.student
    submissions = AssignmentSubmission.objects.filter(student=student)
    
    submitted_assignments = submissions.values_list('assignment_id', flat=True)
    current_time = timezone.now()

    
    parameters = {
        "assignments": assignments,
        "student": student,
        "submitted_assignments": submitted_assignments,
        "current_time": current_time,
        "submissions": submissions
    }
    
    return render(request, "student/assignments.html", parameters)


# =========================================== SUBMIT ASSIGNMENT =============================================

@login_required(login_url="login")
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student
    
    if AssignmentSubmission.objects.filter(assignment=assignment, student=student).exists() or assignment.due_date < timezone.now():
        messages.error(request, "Beta jab tumne URL dekha bhi nhi tha tbse isse khel rhe hain hum🔥")
        return redirect('assignments')

    if request.method == 'POST':
        submission = AssignmentSubmission(
            assignment=assignment,
            student=student,
        )
        
        if assignment.assignment_type == 'Coding':
            submission.submission_code = request.POST.get('submission_code')
        elif assignment.assignment_type == 'Text':
            submission.submission_text = request.POST.get('submission_text')
        elif assignment.assignment_type == 'File':
            submission.submission_file = request.FILES.get('submission_file')
        elif assignment.assignment_type == 'Image':
            submission.submission_image = request.FILES.get('submission_image')
        elif assignment.assignment_type == 'Link':
            submission.submission_link = request.POST.get('submission_link')
        
        submission.extra_info = request.POST.get('extra_info')
        
        try:
            submission.save()
            messages.success(request, "Assignment submitted successfully.")
            return redirect('assignments')
        except ValueError as e:
            messages.error(request, str(e))
    
    
    parameters = {
        "assignment": assignment,
        'student': student
    }
    
    return render(request, "student/submit_assignment.html", parameters)


# =========================================== VIEW SUBMISSION =============================================

@login_required(login_url="login")
def view_submission(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = get_object_or_404(AssignmentSubmission, assignment=assignment, student=request.user)
    
    parameters = {
        'assignment': assignment,
        'submission': submission
    }
    
    return render(request, 'student/view_submission.html', parameters)

# =========================================== DELETE SUBMISSION =============================================

@login_required(login_url="login")
def delete_submission(request, submission_id):
    
    # check if the deadline is passed
    
    if AssignmentSubmission.objects.get(id=submission_id).assignment.due_date < timezone.now():
        messages.error(request, "You cannot delete the submission after the deadline.")
        return redirect('assignments')
    
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)
    submission.delete()
    
    messages.success(request, "Submission deleted successfully.")
    
    return redirect('assignments')

# =========================================== ROADMAP =============================================

@login_required(login_url="login")
def roadmap(request):
    
    courses = request.user.student.courses.all()
    
    parameters = {
        "courses": courses
    }
    
    return render(request, "student/roadmap.html", parameters)


# =========================================== VIEW ROADMAP =============================================

@login_required(login_url="login")
def view_roadmap(request, course_id):
        
    course = Course.objects.get(id=course_id)
    roadmaps = course.roadmap_set.all()
    
    parameters = {
        "course": course,
        "roadmaps": roadmaps
    }
    
    return render(request, "student/view_roadmap.html", parameters)






# ==============================================================================================
# ========================================= MY PROFILE =========================================
# ==============================================================================================

@login_required(login_url="login")
def my_profile(request):    
    return render(request, "student/my_profile.html")

# ========================================= EDIT PROFILE =========================================

@login_required(login_url="login")
def edit_profile(request):
    
    student = Student.objects.get(id=request.user.id)
    
    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.email = request.POST.get("email")
        student.gender = request.POST.get("gender")
        student.college = request.POST.get("college")
        student.linkedin_id = request.POST.get("linkedin_id")
        student.github_id = request.POST.get("github_id")
        
        if request.POST.get("dob"):
            student.dob = request.POST.get("dob")
        
        if request.POST.get("mobile_number").isdigit() and len(request.POST.get("mobile_number")) == 10:
            student.mobile_number = request.POST.get("mobile_number")
        else:
            messages.error(request, "Invalid mobile number!")
            return redirect("edit_profile")
            
        
        student.save()
        
        messages.success(request, "Profile updated successfully!")
        
        return redirect("my_profile")
    
    parameters = {
        "student": student
    }
    
    return render(request, "student/edit_profile.html", parameters)

# ========================================= UPLOAD PROFILE =========================================

@login_required(login_url="login")
def upload_profile(request):

    if request.method == 'POST':

        student = Student.objects.get(id=request.user.id)

        student.profile_pic = request.FILES['profile_pic']
        
        if student.profile_pic.size > 5242880:
            messages.error(request, 'Profile Picture size should be less than 5MB')
            return redirect('my_profile')
        
        student.save()

        messages.success(request, 'Profile Picture Updated Successfully')

        return redirect('my_profile')
    
# ========================================= CHANGE PASSWORD =========================================

@login_required(login_url="login")
def change_password(request):
        
    student = Student.objects.get(id=request.user.id)
    
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    confirm_password = request.POST.get("confirm_password")
    
    if student.check_password(old_password):
        
        if new_password == confirm_password and old_password != new_password:
            
            student.set_password(new_password)
            student.is_changed_password = True
            student.save()
            
            messages.success(request, "Password changed successfully! Please login Again!")
            
            return account_logout(request)
        
        elif old_password == new_password:
            messages.error(request, "New password should be different from old password!")
            return redirect("my_profile")
        
        else:
            messages.error(request, "New password and confirm password do not match!")
            return redirect("my_profile")
    
    else:
        messages.error(request, "Old password is incorrect!")
        return redirect("my_profile")


# ========================================= FEEDBACK =========================================

@login_required(login_url="login")
def feedback(request):
    
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        
        Feedback.objects.create(
            student=request.user.student,
            subject=subject,
            message=message
        )
        
        messages.success(request, "Feedback sent successfully!")
        
        return redirect("feedback")
    
    return render(request, "student/feedback.html")


