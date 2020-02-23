from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from django.db.models import Avg
import json
from django.urls import reverse
from myapp.forms import *
from GoogleNews import GoogleNews
from profanity_check import predict, predict_prob

# Create your views here.
def index(request):
    return render(request,'index.html',{})

def about(request):
    return render(request,'about.html',{})

def website_render(request):
    clg = College.objects.filter(applicant_id=request.session['uid'])
    if len(clg):
        college = getCollege(clg[0].college)

    if request.method == "POST":
        print(request.POST.get("submit"))
        if request.POST.get("submit") == "clg":
            print(request.POST)
            clgForm = CollegeForm(request.POST, request.FILES)
            if clgForm.is_valid():
                clgForm.save()

        elif request.POST.get("submit") == "dept":
            deptForm = DepartmentForm(request.POST)
            print(deptForm)
            if deptForm.is_valid():
                deptForm.save()
                return HttpResponse("Hello")
                

    clgForm = CollegeForm()
    deptForm = DepartmentForm()
    college_id = College.objects.get(applicant_id=str(request.session['uid']))
    flag = True
    dept_list = []
    try:
        flag = True
        dept_list = Department.objects.filter(college=College.objects.get(applicant_id= request.session['uid']))
    except:
        flag = False
        dept_list = []
    subForm = SubjectForm()
    syllabusForm = SyllabusForm()
    return render(request,'website_render.html',{"user_id": request.session['uid'],"college_id":college_id,"clgForm":clgForm,"deptForm":deptForm,"flag":flag,"subForm":subForm,"syllabusForm":syllabusForm,"dept_list":dept_list})

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
            return render(request,'index.html')
              
    return render(request,'index.html',{})

@login_required(login_url='index')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("admin_index"))

##########################

def admin_user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                # print()
                request.session['uid'] = User.objects.get(username=username).id 
                # return HttpResponseRedirect(reverse('index'))
                return redirect('website_render')
        else:
            return render(request,'admin/admin_index.html',{"invalidDetails":True})
              
    return render(request,'admin/admin_index.html',{})

@login_required(login_url='index')
def admin_user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("admin_user_login"))

def admin_login_page(request):
    return render(request,'admin/admin_index.html')

##########################
def teacher_home(request):
    return render(request,'teacher_home.html')

def student_home(request):
    return render(request,'student_home.html')

@login_required(login_url='index')
def after_login(request):
    val = "student"
    if val == 'student':
        return redirect('student_home')
        # return redirect('apply_project')
    else:
        return redirect('teacher_home')

def login_page(request):
    return render(request,'login.html')

def getCollege(college_id):
    data = {}

    college = College.objects.get(college = college_id)
    
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

    departments = Department.objects.filter(college = college_id)

    for department in departments:
        dep = {}
        dep["department_id"] = department.department_id
        dep["department_name"] = department.department_name
        dep["vision_mission"] = department.vision_mission
        dep["subjects"] = []

        subjects = Subject.objects.filter(college = college_id, department = department.department_id)

        for subject in subjects:
            sub = {}
            sub["subject_id"] = subject.subject_id
            sub["subject_name"] = subject.subject_name
            sub["semester"] = subject.semester
            sub["taught_by"] = {}
            sub["taught_by"]["teacher_id"] = subject.taught_by.teacher_id
            sub["taught_by"]["teacher_name"] = subject.taught_by.teacher_name

            sub["syllabus"] = {}

            if (len(SyllabusStatus.objects.annotate(av=Avg('completed')).filter(college = college_id, department = department.department_id, subject = subject.subject_id)) == 0):
                sub["syllabus"]["completed"] = 0
            else:
                sub["syllabus"]["completed"] = SyllabusStatus.objects.annotate(av=Avg('completed')).filter(college = college_id, department = department.department_id, subject = subject.subject_id)

            sub["syllabus"]["syllabus"] = []

            syllabus = Syllabus.objects.filter(college = college_id, department = department.department_id, subject = subject.subject_id)

            for syl in syllabus:
                sy = {}
                sy["unit"] = syl.unit
                sy["unit_name"] = syl.unit_name
                sy["topics"] = syl.topics

                sub["syllabus"]["syllabus"].append(sy)

            dep["subjects"].append(sub)

        data["departments"].append(dep)

    return data

def college(request, college_id):
    data = getCollege(college_id)
    
    # return render(request, 'index.html', {"data":data})
    return HttpResponse(json.dumps(data, indent=4), content_type="application/json")

def getNews(query):
    googleNews = GoogleNews()
    googleNews.search(query)

    news = []

    i = 0

    number = min([len(googleNews.result()), 6])

    for result in googleNews.result():
        if (i > number):
            break

        n = {}
        n["title"] = result['title']
        n["description"] = result['desc']
        n["link"] = result['link']
    
        if (i == 0):
            n["image"] = result['img']
        news.append(n)

        i += 1

    googleNews.clear()

    return news

def predict_profanity(message):
    return predict([message])