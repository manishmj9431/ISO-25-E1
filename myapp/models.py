from django.db import models

# Create your models here.
class Colleges(models.Model):
    college_id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=50, null=False)
    university = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=200, null=False)
    contact_number = models.CharField(max_length=15, null=False)
    logo = models.ImageField(upload_to = 'logos/')
    domain = models.TextChoices('DepartmentType', 'Engineering Management All')
    about_us = models.TextField(max_length=1000, null=False)
    image1 = models.ImageField(upload_to = 'slider/', null=False)
    image2 = models.ImageField(upload_to = 'slider/', null=True)
    image3 = models.ImageField(upload_to = 'slider/', null=True)
    image4 = models.ImageField(upload_to = 'slider/', null=True)
    image5 = models.ImageField(upload_to = 'slider/', null=True)

class Departments(models.Model):
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50, null=False)
    vision_mission = models.TextField(max_length=1000, null=False)

class Teachers(models.Model):
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=50, null=False)

class Students(models.Model):
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    roll_number = models.CharField(primary_key=True, max_length=200)
    semester = models.IntegerField(null=False)

class Subjects(models.Model):
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50, null=False)
    semester = models.IntegerField(null=False)
    taught_by = models.ForeignKey(Teachers, on_delete=models.SET_NULL, null=True)

class Syllabus(models.Model):
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    unit = models.IntegerField(null=False)
    unit_name = models.CharField(max_length=10, null=False)
    topics = models.TextField(max_length=1000, null=False)

class SyllabusStatus(models.Model):
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    completed = models.IntegerField(null=False)
    given_by = models.ForeignKey(Students, on_delete=models.CASCADE, null=False)

class SyllabusStatusTeacher(models.Model):
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    completed = models.IntegerField(null=False)
    given_by = models.ForeignKey(Teachers, on_delete=models.CASCADE, null=False)