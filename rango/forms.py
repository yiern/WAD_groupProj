
from django import forms
from rango.models import *
from django.contrib.auth.models import User

    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ('YearEnrolled', 'CurrentYearStudent')

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('CourseID', 'Topics', 'file')
        
