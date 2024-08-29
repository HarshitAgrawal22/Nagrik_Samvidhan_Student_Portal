from django.db import models
from django.contrib.auth.models import User



# ================================================= Instructor ==========================================

class Instructor(User):
    profile_pic = models.ImageField(
        upload_to="teacher_profile", blank=True, null=True, default="/student_profile/default.jpg")

    gender = models.CharField(max_length=19)
    linkedin_id = models.URLField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    
    college = models.CharField(max_length=100, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Instructors"
        verbose_name = "Instructor"
         
    def __str__(self):
        return self.username
    


# =================================================== Course ==========================================
    
class Course(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=50, blank=True, null=True)
    
    thumbnail = models.ImageField(
        upload_to="subject_image", blank=True, null=True)
    
    def __str__(self):
        return self.name


# =================================================== Student ==========================================

class Student(User):
    mobile_number = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    college = models.CharField(max_length=100, blank=True, null=True)
    
    dob = models.DateField(blank=True, null=True)
    is_changed_password = models.BooleanField(default=False)
    
    profile_pic = models.ImageField(
        upload_to="student_profile/", blank=True, null=True, default="/student_profile/default.jpg")
    
    linkedin_id = models.URLField(blank=True, null=True)
    github_id = models.URLField(blank=True, null=True)
    
    courses = models.ManyToManyField(Course, blank=True)
    
    def __str__(self):
        return self.username
    
    def get_profile_score(self):
        score = 30
        
        if self.dob:
            score += 20
        
        if self.linkedin_id:
            score += 30
        
        if self.github_id:
            score += 20
        
        return score

    class Meta:
        verbose_name_plural = "Students"
        verbose_name = "Student"
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = False
            self.set_password('angaarhai')
        super().save(*args, **kwargs)

# ================================== ROADMAP ==================================

class Roadmap(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    
    def __str__(self):
        return self.topic