
from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField(Teacher, related_name='students')

    def __str__(self):
        return self.name

class Certificate(models.Model):
    certificate_id = models.CharField(max_length=10, unique=True)
    jwt_token = models.CharField(max_length=100, unique=True)
    student_name = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name