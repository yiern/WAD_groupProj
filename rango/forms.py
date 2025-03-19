
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
        fields = ('CourseID', 'Topics', 'file')  # Fields to include in the form

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from kwargs
        super(NoteForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
            # Save the form but don't commit to the database yet
            instance = super(NoteForm, self).save(commit=False)
            
            # Set the user field to the current user
            if self.user:
                instance.user = self.user
            
            if commit:
                instance.save()  # Save the instance to the database
            
            return instance