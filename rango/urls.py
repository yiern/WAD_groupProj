from django.urls import path, reverse_lazy
from rango import views
from tango_with_django_project import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'rango'

urlpatterns = [
    path('tNindex', views.tNindex, name='tNindex'),
    path('tNcourse', views.tNcourse, name='tNcourse'),
    path('tNlogin', views.tNlogin, name='tNlogin'),
    path('tNnote', views.tNnote, name='tNnote'),
    path('tNregister', views.tNregister, name='tNregister'),
    path('tNsearch', views.tNsearch, name='tNsearch'),
    path('tNupload/<int:NoteID>/', views.tNupload, name='tNupload'),
    path('tNupload/', views.tNupload, name='tNupload'),
    path('tNuser', views.tNuser, name='tNuser'),
    path('tNnote/<int:NoteID>/', views.tNnote, name = 'tNnote'),
    path('tNnotes/<str:CourseID>/', views.tNnotes, name = "tNnotes"),
    path('serve_docx/<int:NoteID>/', views.serve_docx, name='serve_docx'),
    path('logout/', views.user_logout, name='logout'),
    path('tNedit_profile/', views.tNedit_profile, name='tNedit_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='rango/password_change.html',success_url=reverse_lazy('rango:password_change_done')  ), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='rango/password_change_done.html'), name='password_change_done'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

