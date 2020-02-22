from django.contrib import admin
from myapp.models import *
# Register your models here.

admin.site.register(Colleges)
admin.site.register(Departments)
admin.site.register(Students)
admin.site.register(Teachers)
admin.site.register(Subjects)
admin.site.register(Syllabus)
admin.site.register(SyllabusStatus)
admin.site.register(SyllabusStatusTeacher)
