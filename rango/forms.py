
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
        self.edited = kwargs.pop('edited', None)  # Get the edited note creator from kwargs
        self.CourseID = kwargs.pop('CourseID', None)  # Get the CourseID from kwargs
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['CourseID'].empty_label = 'Select a Course'

        # If CourseID is provided, set it as a hidden field
        if self.CourseID:
            
            self.fields['CourseID'].initial = self.CourseID
            self.fields['CourseID'].widget = forms.HiddenInput()
        
    def save(self, commit=True):
        # Save the form but don't commit to the database yet
        instance = super(NoteForm, self).save(commit=False)
        
        # Set the user field to the current user
        if self.user:
            instance.user = self.user
        
        # Set the edited field to the provided creator (if any)
        if self.edited:
            instance.edited = self.edited
        
        if commit:
            instance.save()  # Save the instance to the database
        
        return instance

class LikeForm(forms.ModelForm):
    class Meta:
        model = NoteLiked
        fields = ()