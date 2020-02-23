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
import requests

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
            mutable_post = request.POST.copy()
            mutable_post["applicant_id"] = request.session['uid']
            print(mutable_post)
            clgForm = CollegeForm(mutable_post, request.FILES)
            if clgForm.is_valid():
                clgForm.save()
                return HttpResponse("Hello")    

        elif request.POST.get("submit") == "dept":
            deptForm = DepartmentForm(request.POST)
            print(deptForm)
            if deptForm.is_valid():
                deptForm.save(commit=False)
                deptForm.college = College.objects.filter(applicant_id=request.session['uid'])[0]
                deptForm.save()
                return HttpResponse("Hello")
                

    clgForm = CollegeForm()
    deptForm = DepartmentForm()
    college = College.objects.filter(applicant_id=str(request.session['uid']))
    flag = True
    dept_list = []
    try:
        flag = True
        if len(college):
            dept_list = Department.objects.filter(college=College.objects.get(applicant_id= request.session['uid']))
        else:
            dept_list = []
    except:
        flag = False
        dept_list = []
    subForm = SubjectForm()
    syllabusForm = SyllabusForm()
    return render(request,'website_render.html',{"user_id": request.session['uid'],"college_id":college,"clgForm":clgForm,"deptForm":deptForm,"flag":flag,"subForm":subForm,"syllabusForm":syllabusForm,"dept_list":dept_list})

def user_login(request,college_id):

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
                    return render(request,'student_home.html')
                else:
                    return render(request,'teacher_home.html')

        else:
            return render(request,'login.html')
              
    return render(request,'login.html')

@login_required(login_url='index')
def user_logout(request,college_id):
    logout(request)
    return redirect("http:127.0.0.1:8000/college/"+college_id)

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

def login_page(request,college_id):
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
                sy["recommended_books"] = getBooks(subject.subject_name + syl.unit_name, 1)

                sub["syllabus"]["syllabus"].append(sy)

            dep["subjects"].append(sub)

        data["departments"].append(dep)

    data["upcoming_events"] = []

    upcomingEvents = UpcomingEvents.objects.filter(college = college_id)

    for event in upcomingEvents:
        e = {}
        
        e["event_id"] = event.event_id
        e["event_name"] = event.event_name
        e["event_description"] = event.event_description
        e["event_image"] = event.event_image
        e["start_date"] = event.start_date
        e["end_date"] = event.end_date

        data["upcoming_events"].append(e)

    return data

def college(request, college_id):
    data = getCollege(college_id)
    clg_news_img = getNews(data['college_name'])[0]
    clg_news = getNews(data['college_name'])[1:5]
    return render(request, 'index.html', {"data":data,"clg_news_img":clg_news_img,"clg_news":clg_news})
    # return HttpResponse(json.dumps(data, indent=4), content_type="application/json")

def forums(request, college_id, forum_id):
    messages = []
    msgs = ForumMessage.objects.filter(college = college_id, forum = forum_id)

    for m in msgs:
        message = {}
        message["message"] = m.message
        message["sent_at"] = m.sent_at
        if (m.isAnonymous):
            message["sent_by"] = "anonymous"
        else:
            message["sent_by"] = m.sent_by
        
        messages.append(message)

    return HttpResponse(json.dumps(messages, indent=4), content_type="application/json")

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
        n['date'] = result['date']
    
        if (i == 0):
            n["image"] = result['img']
        news.append(n)

        i += 1

    googleNews.clear()

    return news

def getBooks(query, num_books):
    r = requests.get("http://openlibrary.org/search.json", {'q': query})
    data = r.json()
    docs = data['docs']

    num = min(data['num_found'], num_books)

    books = []

    i = 0
    for doc in docs:
        if (i >= num):
            break

        book = {}
        book['title'] = doc['title']
        book['publisher'] = doc['publisher']
        book['authors'] = doc['author_name'] 
        books.append(book)
        i += 1

    return books


def predict_profanity(message):
    return predict([message])