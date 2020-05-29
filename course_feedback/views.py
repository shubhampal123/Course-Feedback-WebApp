from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes ,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .tokens import *
from .forms import *
from .models import *

# Create your views here.
def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        
        return HttpResponse('Thank you for email confirmation')

    else:
        return HttpResponse('Activation link not working')

def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        #print(form.cleaned_data['email'])
    
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save() 

            # email confirmation 
            print('inside')
            mail_subject='Activate Course Feedback Web App account.'
            current_site=get_current_site(request)
            message=render_to_string('course_feedback/acc_active_email.html',{

                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })

            to_email=form.cleaned_data['email']

            email=EmailMessage(
                mail_subject,message,to=[to_email]
            )

            email.send()

            return HttpResponse('Confirm your email id')
        else:
            return render(request,'course_feedback/error.html',{'form':form})
    else:
        form=SignupForm()

        return render(request,'course_feedback/signup_form.html',{'form':form})


@login_required
def show_review(request,pk):
    course=Course.objects.filter(pk=pk)
    
    return render(request,'course_feedback/show_course_review.html',{'course':course[0]})

@login_required
def get_feedback(request):
    if request.method=='POST':
        form=ShowFeedbackForm(request.POST)
        if form.is_valid():
            id=form.cleaned_data['name']
            return show_review(request,id)

        else:
            return HttpResponse('Invalid Response')

    else:
        form=ShowFeedbackForm()
        return render(request,'course_feedback/choose_course_form.html',{'form':form})


@login_required
def sort_courses(request):
    if request.method=='POST':
        form=CourseForm(request.POST)
        if form.is_valid():
            courses=Course.objects.all()
            if form.cleaned_data['name']!='':
                courses=courses.filter(name=form.cleaned_data['name'])

            if form.cleaned_data['teacher']!='':
                courses=courses.filter(teacher=form.cleaned_data['teacher'])

            basis=[]
            if form.cleaned_data['count']!='':
                basis.append((form.cleaned_data['count'],'-count'))

            if form.cleaned_data['marks']!='':
                basis.append((form.cleaned_data['marks'],'-marks'))

            if form.cleaned_data['relevance']!='':
                basis.append((form.cleaned_data['relevance'],'-relevance'))
            
            if form.cleaned_data['attendance']!='':
                basis.append((form.cleaned_data['attendance'],'-attendance'))
            
            if form.cleaned_data['workload']!='':
                basis.append((form.cleaned_data['workload'],'-workload'))

            if form.cleaned_data['style']!='':
                basis.append((form.cleaned_data['style'],'-style'))

            basis.sort()

            base=[bas[1] for bas in basis]
            
            if len(basis)==1:
                courses=courses.order_by(base[0])
            
            if len(basis)==2:
                courses=courses.order_by(base[0],base[1])

            if len(basis)==3:
                courses=courses.order_by(base[0],base[1],base[2])

            if len(basis)==4:
                courses=courses.order_by(base[0],base[1],base[2],base[3])

            if len(basis)==5:
                courses=courses.order_by(base[0],base[1],base[2],base[3],base[4])

            if len(basis)==6:
                courses=courses.order_by(base[0],base[1],base[2],base[3],base[4],base[5])

            return render(request,'course_feedback/show_sorted_courses.html',{'courses':courses})
        else:
            return HttpResponse('Invalid Respone')
    else:
        form=CourseForm()
        return render(request,'course_feedback/course_form.html',{'form':form})

@login_required
def give_feedback(request):
    if request.method == 'POST':
        form=FeedbackForm(request.POST)
        if form.is_valid():
            feedback=form.save(commit=False)
            feedback_course=str(feedback.course).split()
            feedback_name=""
            feedback_teacher=""

            for i in range(len(feedback_course)):
                if feedback_course[i]=='by':
                    for j in range(i+1,len(feedback_course)):
                        feedback_teacher=feedback_teacher+feedback_course[j]
                        if(j+1!=len(feedback_course)):
                           feedback_teacher=feedback_teacher+' '
                    break 
                else:
                    feedback_name=feedback_name+feedback_course[i]
                    if(feedback_course[i+1]!='by'):
                        feedback_name=feedback_name+' '

            course=Course.objects.filter(name=feedback_name).filter(teacher=feedback_teacher)
            new_count=course[0].count+1
            new_relevance=(feedback.relevance+(course[0].count*course[0].relevance))/new_count
            new_style=(feedback.style+(course[0].count*course[0].style))/new_count
            new_marks=(feedback.marks+(course[0].count*course[0].marks))/new_count
            new_attendance=(feedback.attendance+(course[0].count*course[0].attendance))/new_count
            new_workload=(feedback.workload+(course[0].count*course[0].workload))/new_count

            pk=course[0].pk
            Course.objects.filter(pk=pk).update(count=new_count)
            Course.objects.filter(pk=pk).update(relevance=new_relevance)
            Course.objects.filter(pk=pk).update(style=new_style)
            Course.objects.filter(pk=pk).update(marks=new_marks)
            Course.objects.filter(pk=pk).update(attendance=new_attendance)
            Course.objects.filter(pk=pk).update(workload=new_workload) 

            feedback.save()
 
            return redirect('/')

        else:
            return HttpResponse('Invalid Response')

    else:
        form=FeedbackForm()

        return render(request,'course_feedback/feedback_form.html',{'form':form})


def home(request):
    return render(request,'course_feedback/show_home.html',{})
