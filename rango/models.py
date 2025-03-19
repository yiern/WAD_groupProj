import datetime
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.


    
class Students(models.Model):

    YearEnrolled = models.IntegerField()
    CurrentYearStudent = models.IntegerField(default= 1)
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    def __str__(self):
        return self.user.username
    

class Courses(models.Model):
    CourseID = models.CharField(primary_key= True, max_length=10)
    CourseName = models.CharField(max_length=200)
    def __str__(self):
        return self.CourseID + ": "+self.CourseName

class Enrolls(models.Model):
    user = models.ForeignKey(Students, on_delete=models.CASCADE)
    CourseID = models.ForeignKey(Courses, on_delete= models.CASCADE)

class Note(models.Model):
    user = models.ForeignKey(Students, on_delete= models.CASCADE)
    DateUploaded = models.DateTimeField(auto_now_add=True)
    CourseID = models.ForeignKey(Courses, on_delete= models.CASCADE)
    Topics = models.CharField(max_length=200)
    NoteID = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="Documents/")

class EditedNotes(models.Model):
    user = models.ForeignKey(Students, on_delete=models.CASCADE)
    DateUploaded = models.DateField(auto_now_add=True)
    CourseID = models.ForeignKey(Courses, on_delete=models.CASCADE)
    NoteID = models.ForeignKey(Note, on_delete=models.CASCADE)
    file = models.FileField(upload_to = "Edited_Note/", null= True)

 
