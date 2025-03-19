from django.contrib import admin
from .models import *
from rango.models import *

# Register the Students model
@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'YearEnrolled', 'CurrentYearStudent')
    search_fields = ('user__username',)


# Register other models
@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('CourseID', 'CourseName')
    search_fields = ('CourseID', 'CourseName')

@admin.register(Enrolls)
class EnrollsAdmin(admin.ModelAdmin):
    list_display = ('user', 'CourseID')
    search_fields = ('user__username', 'CourseID__CourseID')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'CourseID', 'Topics', 'DateUploaded')
    search_fields = ('user__username', 'CourseID__CourseID', 'Topics')

@admin.register(EditedNotes)
class EditedNotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'CourseID', 'NoteID', 'DateUploaded')
    search_fields = ('user__username', 'CourseID__CourseID', 'NoteID__NoteID')



