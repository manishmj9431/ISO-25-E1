"""isohack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index,name="index"),
    path('', views.after_login,name="dashboard"),
    path('website_render',views.website_render,name="website_render"),
    path('login_page/', views.login_page,name="login_page"),
    path('user_login/', views.user_login,name="user_login"),   
    path('user_logout/', views.user_logout,name="user_logout"),   
    path('teacher_home/', views.teacher_home,name="teacher_home"),   
    path('student_home/', views.student_home,name="student_home"),
    path('collegeForm', views.collegeForm, name="collegeForm"),
    path('departmentForm', views.departmentForm, name="departmentForm"),
    path('subjectForm', views.subjectForm, name="subjectForm"),   
    path('college/<str:college_id>/', views.college, name="college"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   
