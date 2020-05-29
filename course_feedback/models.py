from django.db import models

# Create your models here.
rating=(
    (0,0),
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10),
)

class Course(models.Model):
    name=models.CharField(max_length=200) 
    teacher=models.CharField(max_length=200)
    count=models.IntegerField(default=0)
    marks=models.IntegerField(choices=rating)
    relevance=models.IntegerField(choices=rating)
    attendance=models.IntegerField(choices=rating)
    workload=models.IntegerField(choices=rating)
    style=models.IntegerField(choices=rating)

    def __str__(self):
        return self.name+" by "+self.teacher

class Feedback(models.Model):
    course= models.ForeignKey('course_feedback.Course', on_delete=models.CASCADE, related_name='feedback')
    user=models.CharField(max_length=200,default='admin')
    marks=models.IntegerField(choices=rating)
    relevance=models.IntegerField(choices=rating)
    attendance=models.IntegerField(choices=rating)
    workload=models.IntegerField(choices=rating)
    style=models.IntegerField(choices=rating)

    def __str__(self):
        return str(self.user)+" ( "+str(self.course)+" ) "




    



