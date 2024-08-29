from django.db import models

class Flames(models.Model):
    name = models.CharField(max_length=100)
    whatsapp_number = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
# ============================================================================================
# ============================================================================================
# ============================================================================================

class ScholarshipTest(models.Model):
    name = models.CharField(max_length=255)

class Question(models.Model):
    test = models.ForeignKey(ScholarshipTest, on_delete=models.CASCADE)
    question_text = models.TextField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    audio = models.URLField(blank=True, null=True)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1)

class StudentSubmission(models.Model):
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    submission_time = models.DateTimeField(auto_now_add=True)
    