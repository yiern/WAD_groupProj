import datetime
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=128, unique= True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default =0)
    slug = models.SlugField(unique= True)

    def save(self, *args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class users(models.Model):
    name = models.CharField(max_length=128,null=False,unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_descriptions = 'published recently?'
    
class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class UserProfile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank = True)
    picture = models.ImageField(upload_to='profile_images',blank = True)

    def __str__(self):
        return self.user.username


class Students(models.Model):
    UserID = models.CharField(unique= True, max_length = 200, primary_key= True)
    Name = models.CharField(max_length=200)
    YearEnrolled = models.IntegerField()
    CurrentYearStudent = models.IntegerField(default= 1)

class Courses(models.Model):
    CourseID = models.CharField(primary_key= True, max_length=10)
    CourseName = models.CharField(max_length=200)

class Enrolls(models.Model):
    UserID = models.ForeignKey(Students, on_delete=models.CASCADE)
    CourseID = models.ForeignKey(Courses, on_delete= models.CASCADE)

class Note(models.Model):
    UserID = models.ForeignKey(Students, on_delete= models.CASCADE)
    DateUploaded = models.DateTimeField(auto_now_add=True)
    CourseID = models.ForeignKey(Courses, on_delete= models.CASCADE)
    Topics = models.CharField(max_length=200)
    NoteID = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="Documents/")

class EditedNotes(models.Model):
    EditedID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Students, on_delete=models.CASCADE)
    DateUploaded = models.DateField(auto_now_add=True)
    CourseID = models.ForeignKey(Courses, on_delete=models.CASCADE)
    NoteID = models.ForeignKey(Note, on_delete=models.CASCADE)
    file = models.FileField(upload_to = "Edited_Note/", null= True)

