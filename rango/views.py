import os
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse, HttpResponse
from rango.forms import *
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
#from docx2pdf import convert
from django.contrib import messages 
from tango_with_django_project import settings


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))

def index(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    

    visitor_cookie_handler(request)

    response = render(request, 'rango/tNindex.html', context=context_dict)

    return response

def tNindex(request):

    courses = Courses.objects.all()
    notes = Note.objects.all()

    return render(request, 'rango/tNindex.html', {'courses' : courses, 'notes':notes})

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

def tNnote(request,NoteID):

    
    note = Note.objects.get(NoteID = NoteID)

    return render(request, 'rango/tNnote.html', {'note': note})

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
    return render(request, 'rango/tNsearch.html')

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
    
    notes = Note.objects.filter(user = request.user.id)

    return render(request, 'rango/tNuser.html', {'notes':notes,})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:tNindex'))


def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)



def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
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
                return redirect(reverse('rango:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
    
        return render(request, 'rango/login.html')

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Get the number of visits from the server-side cookie
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    # Get the last visit time from the server-side cookie or set it to the current time if it doesn't exist
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie with the current time
        request.session['last_visit'] = str(datetime.now())
    else:
        # Keep the last visit cookie unchanged
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits
