from django.db import models
from django.contrib.postgres.fields import JSONField


class Question(models.Model):
    text = models.TextField()
    course_id = models.CharField(max_length=50, default='2024_june_math')  
    exam_type = models.CharField(max_length=20)  
    options = models.JSONField() 
    correct_option = models.CharField(max_length=5)

    def __str__(self):
        return self.text
