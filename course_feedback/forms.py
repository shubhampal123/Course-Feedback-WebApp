from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def check_nsit(value):
    s=str(value)
    ns=""
    for i in range(len(s)):
        if s[i]=='@':
            for j in range(i+1,len(s)):
                ns=ns+s[j]
            break 
    
    if ns!='nsit.net.in':
        raise ValidationError(
            _('%(value)s is not nsit email id'),
            params={'value':value},
        )
        return ValidationError(
            _('%(value)s is not nsit email id'),
            params={'value':value},
        )

    return value
    
    
class SignupForm(UserCreationForm):
    email=forms.EmailField(required=True,max_length=200,validators=[check_nsit])

    class Meta:
        model=User
        fields=('username','email','password1','password1',)

class FeedbackForm(forms.ModelForm):

    class Meta:
        model=Feedback
        fields=('course','marks','relevance','attendance','workload','style',)

rating=(
    ('','-'),
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
)
def get_name():
    courses=Course.objects.all() 
    name=[]
    name.append(('','-'))
    for i in range(len(courses)):
        name.append((courses[i].name,courses[i].name))

    name.sort()

    ret_name=[]
    for (a,b) in name:
        if (a,b) not in ret_name:
            ret_name.append((a,b))
    
    
    return ret_name

def get_teacher():
    courses=Course.objects.all() 
    teacher=[]
    teacher.append(('','-'))
    for i in range(len(courses)):
        teacher.append((courses[i].teacher,courses[i].teacher))

    teacher.sort()
    ret_teacher=[]
    for (a,b) in teacher:
        if (a,b) not in ret_teacher:
            ret_teacher.append((a,b))
    
    
    return ret_teacher

def get_choices():
    return rating

def get_course_choices():
    courses=Course.objects.all().order_by('name')
    choices=[]
    for i in range(len(courses)):
        choices.append((courses[i].pk,courses[i].name+' by '+courses[i].teacher))
     
    return choices



class CourseForm(forms.Form):
    name=forms.ChoiceField(required=False,widget=forms.Select,choices=get_name()) 
    teacher=forms.ChoiceField(required=False,widget=forms.Select,choices=get_teacher()) 
    count=forms.ChoiceField(required=False,widget=forms.Select,choices=get_choices())
    marks=forms.ChoiceField(required=False,widget=forms.Select,choices=get_choices())
    relevance=forms.ChoiceField(required=False,widget=forms.Select,choices=get_choices())
    attendance=forms.ChoiceField(required=False,widget=forms.Select,choices=get_choices())
    workload=forms.ChoiceField(required=False,widget=forms.Select,choices=get_choices())
    style=forms.ChoiceField(required=False,widget=forms.Select,choices=get_choices())
    
class ShowFeedbackForm(forms.Form):
    name=forms.ChoiceField(widget=forms.Select,choices=get_course_choices())


    
 
