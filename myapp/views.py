from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

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