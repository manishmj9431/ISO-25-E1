from myapp.models import *


class CollegeForm(forms.ModelForm):

    class Meta:
        model = College
        fields = ('college_name','university','address','contact_number','logo','domain','about_us','image1','image2','image3')
    
class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('department_name','vision_mission')