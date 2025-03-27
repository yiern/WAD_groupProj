from django.urls import path
from rango import views
from tango_with_django_project import settings
from django.conf.urls.static import static

app_name = 'rango'

urlpatterns = [
    path('', views.tNindex, name='tNindex'),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('restricted/', views.restricted, name='restricted'),
    
    path('course/', views.tNcourse, name='tNcourse'),
    path('note/<int:NoteID>/', views.tNnote, name='tNnote'),
    path('notes/<str:CourseID>/', views.tNnotes, name='tNnotes'),
    path('search/', views.tNsearch, name='tNsearch'),
    path('upload/', views.tNupload, name='tNupload'),  # For new uploads
    path('upload/<int:NoteID>/', views.tNupload, name='tNupload'),  # For edits (same name)
    path('user/', views.tNuser, name='tNuser'),
    path('serve_docx/<int:NoteID>/', views.serve_docx, name='serve_docx'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)