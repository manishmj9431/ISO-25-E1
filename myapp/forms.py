from myapp.models import *
from django import forms

class CollegeForm(forms.ModelForm):

    class Meta:
        model = College
        fields = ('applicant_id', 'college_name','university','address','contact_number','logo','domain','about_us','image1','image2','image3','image4','image5')
        widgets = {'applicant_id': forms.HiddenInput()}


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('college', 'department_name','vision_mission','hod','count')
        widgets = {'college': forms.HiddenInput()}

class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ('subject_name','semester','taught_by')

class SyllabusForm(forms.ModelForm):

    class Meta:
        model = Syllabus
        fields = ('unit','unit_name','topics')