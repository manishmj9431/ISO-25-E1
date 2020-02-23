from django.db import models
from django.contrib.auth.models import User

DOMAIN_CHOICES = (
   ('DepartmentType', 'DepartmentType'),
   ('Engineering Management All','Engineering Management All'),
)

# Create your models here.
class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    applicant_id = models.CharField(max_length=200, null=False)
    college_name = models.CharField(max_length=50, null=False)
    university = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=200, null=False)
    contact_number = models.CharField(max_length=15, null=False)
    logo = models.ImageField(upload_to = 'logos/')
    domain = models.TextField(max_length=100, choices=DOMAIN_CHOICES)
    about_us = models.TextField(max_length=1000, null=False)
    image1 = models.ImageField(upload_to = 'slider/', null=False)
    image2 = models.ImageField(upload_to = 'slider/', null=True)
    image3 = models.ImageField(upload_to = 'slider/', null=True)
    image4 = models.ImageField(upload_to = 'slider/', null=True)
    image5 = models.ImageField(upload_to = 'slider/', null=True)

class Department(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE,null=True)
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50, null=False)
    vision_mission = models.TextField(max_length=1000, null=False)

class Teacher(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=50, null=False)

class Student(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    roll_number = models.CharField(primary_key=True, max_length=200)
    semester = models.IntegerField(null=False)

class Subject(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50, null=False)
    semester = models.IntegerField(null=False)
    taught_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

class Syllabus(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unit = models.IntegerField(null=False)
    unit_name = models.CharField(max_length=10, null=False)
    topics = models.TextField(max_length=1000, null=False)

class SyllabusStatus(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    completed = models.IntegerField(null=False)
    given_by = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)

class SyllabusStatusTeacher(models.Model):
    college_id = models.ForeignKey(College, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    completed = models.IntegerField(null=False)
    given_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False)