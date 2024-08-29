from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from accounts.models import Student, Instructor, Course

# ========================================= SESSIONS =========================================

class Session(models.Model):

    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, null=True, on_delete=models.CASCADE)
    
    topic = models.CharField(max_length=20)
    session_time = models.DateTimeField()
    link = models.URLField()
    recorded_session_link = models.URLField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    def get_meeting_status(self):
        now = timezone.now()
        if self.session_time > now:
            return {
                "color": "success",
                "status": "Upcoming"
            }

        elif self.is_completed:
            return {
                "color": "dark",
                "status": "Finished"
            }

        elif self.session_time < now:
            return {
                "color": "info",
                "status": "Ongoing"
            }

        else:
            return {
                "color": "danger",
                "status": "Error"
            }

# ========================================== NOTIFICATIONS =========================================
    
class Notification(models.Model):
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_fixed = models.BooleanField(default=False)
    is_alert = models.BooleanField(default=False)
    
    type_choices = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
        ('success', 'Success'),
    ]
    
    type = models.CharField(max_length=20, choices=type_choices, default='info')
    expiration_date = models.DateTimeField(null=True, blank=True)

    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    
    def is_active(self):
        if self.expiration_date:
            return timezone.now() < self.expiration_date
        return True
        
    def __str__(self):
        return self.title

# ======================================= Anonymous Message ========================================

class Anonymous_Message(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    is_replied = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.message
    
    # set the value of replied at automatically when reply is added
    
    def save(self, *args, **kwargs):
        if self.reply:
            self.is_replied = True
            self.replied_at = timezone.now()
        super(Anonymous_Message, self).save(*args, **kwargs)

# ======================================= READING MATERIAL ===================================

class Notes(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="notes/")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Note"
    verbose_name_plural = "Notes"
    
# =========================================== FEEDBACK ============================================

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return 'Message from ' + self.student.username
    
# ====================================== ASSIGNMENTS ============================================


class Assignment(models.Model):
    ASSIGNMENT_TYPES = [
        ('Coding', 'Coding'),
        ('Text', 'Text'),
        ('File', 'File'),
        ('Image', 'Image'),
        ('Link', 'Link')        
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    assignment_type = models.CharField(max_length=10, choices=ASSIGNMENT_TYPES)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        
# ====================================== ASSIGNMENT SUBMISSION ============================================

class AssignmentSubmission(models.Model):
    
    status_choices = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignments')
    
    submission_text = models.TextField(null=True, blank=True)
    submission_file = models.FileField(
        upload_to='assignments/files/', 
        null=True, blank=True, 
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'zip'])]
    )
    submission_image = models.ImageField(
        upload_to='assignments/images/', 
        null=True, blank=True, 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    submission_code = models.TextField(null=True, blank=True)
    submission_link = models.URLField(null=True, blank=True)
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    extra_info = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.assignment.title} - {self.student.username}'

    def save(self, *args, **kwargs):
        # Ensure only the relevant field is filled based on assignment type
        if self.assignment.assignment_type == 'Text' and not self.submission_text:
            raise ValueError('Text submission is required for this assignment.')
        elif self.assignment.assignment_type == 'File' and not self.submission_file:
            raise ValueError('File submission is required for this assignment.')
        elif self.assignment.assignment_type == 'Image' and not self.submission_image:
            raise ValueError('Image submission is required for this assignment.')
        elif self.assignment.assignment_type == 'Coding' and not self.submission_code:
            raise ValueError('Code submission is required for this assignment.')
        elif self.assignment.assignment_type == 'Link' and not self.submission_link:
            raise ValueError('Link submission is required for this assignment.')
        super().save(*args, **kwargs)
        
    def get_color_based_on_status(self):
        if self.status == 'Pending':
            return 'warning'
        elif self.status == 'Accepted':
            return 'success'
        elif self.status == 'Rejected':
            return 'danger'
        else:
            return 'info'

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']
        verbose_name = 'Assignment Submission'
        verbose_name_plural = 'Assignment Submissions'
        
