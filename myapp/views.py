from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django.db.models import Avg
import json

# Create your views here.
def index(request):
    return render(request,'index.html',{})

def website_render(request):
    return render(request,'website_render.html',{})

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                val = "student"
                # request.session['member_cat'] = val
                # return HttpResponseRedirect(reverse('index'))
                if val == 'student':
                    return redirect('student_home')
                else:
                    return redirect('teacher_home')
        else:
            return render(request,'index.html',{})
              
    return render(request,'index.html',{})

@login_required(login_url='index')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def teacher_home(request):
    return render(request,'teacher_home.html')

def student_home(request):
    return render(request,'student_home.html')

@login_required(login_url='index')
def after_login(request):
    val = Profile.objects.get(user=request.user).category
    if val == 'student':
        return redirect('student_home')
        # return redirect('apply_project')
    else:
        return redirect('teacher_home')

def login_page(request):
    return render(request,'login.html')


collegeId = ''

def collegeForm(request):
    if request.method=='POST':
        college = College()
        
        college.college_name = request.POST['college_name']
        college.university = request.POST['university_name']
        college.address = request.POST['address']
        college.contact_number = request.POST['contact']
        college.logo = request.POST['logo']
        college.domain = request.POST['college_type']
        college.about_us = request.POST['about_us']

        college.save()

        collegeId = college.college_id
        print(college.college_id)
    # return redirect('website_render')
    return render(request, 'index.html', {"collegeId":collegeId})

departmentId = ''

def departmentForm(request):
    if request.method=='POST':
        department = Department()

        department.department_name = request.POST['department_name']
        department.vision_mission = request.POST['vision']
        department.college_id = College(college_id = "1")

        department.save()

        departmentId = department.department_id
        print(department.department_id)

    return render(request, 'index.html', {})

def subjectForm(request):
    if request.method=='POST':
        subject = Subjects()

        subject.college_id = College(college_id = "1")
        subject.department_id = Department(department_id = "1")
        subject.subject_name = request.POST['subject']
        subject.semester = request.POST['sem']
        
        subject.save()

        for i in range(5):
            syllabus = Syllabus()
            syllabus.college_id = College(college_id = "1")
            syllabus.department_id = Department(department_id = "1")
            syllabus.subject_id = subject
            syllabus.unit = i + 1
            syllabus.unit_name = str(i)
            syllabus.topics = request.POST['unit'+str(i + 1)]

            syllabus.save()

    return render(request, 'index.html', {})

def college(request, college_id):
    data = {}
    college = College.objects.get(college_id = college_id)
    data["college_id"] = college_id
    data["college_name"] = college.college_name
    data["university"] = college.university
    data["address"] = college.address
    data["contact_number"] = college.contact_number
    data["logo"] = college.logo.name
    # TODO: fix this
    # data["domain"] = college.domain.value
    data["about_us"] = college.about_us
    data["image1"] = college.image1.name
    data["image2"] = college.image2.name
    data["image3"] = college.image3.name
    data["image4"] = college.image4.name
    data["image5"] = college.image5.name
    data["departments"] = []

    departments = Department.objects.filter(college_id = college_id)

    for department in departments:
        dep = {}
        dep["department_id"] = department.department_id
        dep["department_name"] = department.department_name
        dep["vision_mission"] = department.vision_mission
        dep["subjects"] = []

        subjects = Subject.objects.filter(college_id = college_id, department_id = department.department_id)

        for subject in subjects:
            sub = {}
            sub["subject_id"] = subject.subject_id
            sub["subject_name"] = subject.subject_name
            sub["semester"] = subject.semester
            sub["taught_by"] = {}
            sub["taught_by"]["teacher_id"] = subject.taught_by.teacher_id
            sub["taught_by"]["teacher_name"] = subject.taught_by.teacher_name

            sub["syllabus"] = {}

            if (len(SyllabusStatus.objects.annotate(av=Avg('completed')).filter(college_id = college_id, department_id = department.department_id, subject_id = subject.subject_id)) == 0):
                sub["syllabus"]["completed"] = 0
            else:
                sub["syllabus"]["completed"] = SyllabusStatus.objects.annotate(av=Avg('completed')).filter(college_id = college_id, department_id = department.department_id, subject_id = subject.subject_id)

            sub["syllabus"]["syllabus"] = []

            syllabus = Syllabus.objects.filter(college_id = college_id, department_id = department.department_id, subject_id = subject.subject_id)

            for syl in syllabus:
                sy = {}
                sy["unit"] = syl.unit
                sy["unit_name"] = syl.unit_name
                sy["topics"] = syl.topics

                sub["syllabus"]["syllabus"].append(sy)

            dep["subjects"].append(sub)

        data["departments"].append(dep)

    #return render(request, 'index.html', {"college":college})
    return HttpResponse(json.dumps(data, indent=4), content_type="application/json")