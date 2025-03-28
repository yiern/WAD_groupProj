import os
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse, HttpResponse
from rango.forms import *
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from tango_with_django_project import settings


def tNindex(request):
    courses = Courses.objects.all()
    top_notes = Note.objects.order_by('-views')[:5]
    
    return render(request, 'rango/tNindex.html', {
        'courses': courses,
        'top_notes': top_notes
    })

def tNcourse(request):
    courses = Courses.objects.all()
    
    return render(request, 'rango/tNcourse.html', {'courses': courses})

def tNlogin(request):
     # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
       
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:tNindex'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your ThinkNote account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/tNlogin.html')
   
def serve_docx(request, NoteID):
    # Fetch the note object
    note = get_object_or_404(Note, NoteID=NoteID)
    
    # Construct the file path
    file_path = os.path.join(settings.MEDIA_ROOT, note.file.name)
    
    # Serve the file with the correct headers
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        return response
    else:
        return HttpResponse("File not found", status=404)

def tNnote(request, NoteID):
    form = LikeForm()
    liked = False
    note = get_object_or_404(Note, NoteID=NoteID)

    if request.user.is_authenticated:
        try:
            if not note.viewed_by.filter(pk=request.user.pk).exists():
                note.views += 1
                note.viewed_by.add(request.user)
                note.save()
        except (AttributeError, TypeError):
            pass
        liked = note.liked_by.filter(pk=request.user.pk).exists()
        if request.method == 'POST':
            if note.liked_by.filter(pk=request.user.pk).exists():
                note.likes -= 1
                note.liked_by.remove(request.user)
                note.save()
                liked = True
                messages.success(request, 'Liked +1')
            else:
                note.likes += 1
                note.liked_by.add(request.user)
                note.save()
                liked = False
                messages.success(request, 'Disliked')
            return redirect(reverse('rango:tNnote', kwargs={'NoteID': NoteID}))
            
    return render(request, 'rango/tNnote.html', {'note': note, 'liked': liked, 'form': form})

def tNnotes(request,CourseID):
    notes_from_course = Note.objects.filter(CourseID = CourseID)

    return render(request, 'rango/tNnotes.html', {'course_notes':notes_from_course})

def tNregister(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        students_form = StudentForm(request.POST)

        if user_form.is_valid() and students_form.is_valid():
            # Save the User data
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            
            user.set_password(password)  
            user.save()

            # Save the Students data
            student = students_form.save(commit=False)
            student.user = user  
            student.save()

            registered = True
            return redirect('rango:tNlogin')  # Redirect to the login page after successful registration
        else:
            print(user_form.errors, students_form.errors)  # Print form errors for debugging
    else:
        user_form = UserForm()
        students_form = StudentForm()

    return render(request,
                  'rango/tNregister.html',
                  context={'user_form': user_form,
                           'students_form': students_form,
                           'registered': registered})

def tNsearch(request):
    query = request.GET.get('q', '')  # Get the search query
    search_results = None
    
    if query:
        search_results = Note.objects.filter(Topics__icontains=query)
    
    return render(request, 'rango/tNsearch.html', {
        'searchResults': search_results,
        'searchTitle': f"Results for '{query}'",
        'query': query
    })

@login_required
def tNupload(request, NoteID = None):

    if request.method == 'POST':
        # Print the contents of request.POST and request.FILES
        
        if NoteID is not None:
            edit = True
            creator = Note.objects.get(NoteID = NoteID)
            form = NoteForm(request.POST, request.FILES, user=request.user.students, edited=NoteID, CourseID = creator.CourseID,)  # request.user.students is the Students instance

        else:
            edit = False
            creator = None
            form = NoteForm(request.POST, request.FILES, user=request.user.students, edited=NoteID)  # request.user.students is the Students instance
        
        if form.is_valid():
            
            form.save()  # Save the form with the user field set
            messages.success(request, 'File uploaded successfully!')  # Add a success message

            return redirect('rango:tNupload')  # Redirect to the index page after successful upload
        else:

            # Render an empty form for GET requests
            form = NoteForm(user=request.user.students)
            messages.error(request, 'File not uploaded successfully')  # Add a success message
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
    else:
        if NoteID is not None:
            edit = True
            creator = get_object_or_404(Note, NoteID=NoteID)
            form = NoteForm(user=request.user.students, edited=creator.user, CourseID=creator.CourseID)
        else:
            edit = False
            creator = None
            form = NoteForm(user=request.user.students)
    
    return render(request, 'rango/tNupload.html', {'form': form, 'edit':edit, 'creator' : creator})

def tNuser(request):
    notes = Note.objects.filter(user=request.user.id)
    return render(request, 'rango/tNuser.html', {'notes': notes, 'username': request.user.username})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:tNindex'))



