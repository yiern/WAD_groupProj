import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')
from datetime import date
import django
django.setup()
#from rango.models import Category, Page, Note, Students,Courses,EditedNotes
from rango.models import *

def populate():
    python_pages = [
    {'title': 'Official Python Tutorial','url':'http://docs.python.org/3/tutorial/', 'views': 10,},
    {'title':'How to Think like a Computer Scientist','url':'http://www.greenteapress.com/thinkpython/', 'views':19},
    {'title':'Learn Python in 10 Minutes','url':'http://www.korokithakis.net/tutorials/python/', 'views': 25} 
    ]
    

    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', 'views':10},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/', 'views':10},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/','views':10} 
    ]

    other_pages = [
    {'title':'Bottle',
    'url':'http://bottlepy.org/docs/dev/','views':10},
    {'title':'Flask',
    'url':'http://flask.pocoo.org','views':10} 
    ]

    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
    'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
    'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} }

    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data['views'],cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'],p['views'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

    students = [
    {'UserID': "2907132C", 'name': 'Ian', 'YearEnrolled': 2024, 'CurrentYearStudent': 2},
    {'UserID': "2918234D", 'name': 'Sarah', 'YearEnrolled': 2023, 'CurrentYearStudent': 3},
    {'UserID': "2929345E", 'name': 'James', 'YearEnrolled': 2022, 'CurrentYearStudent': 4},
    {'UserID': "2930456F", 'name': 'Emily', 'YearEnrolled': 2024, 'CurrentYearStudent': 2},
    {'UserID': "2941567G", 'name': 'Michael', 'YearEnrolled': 2021, 'CurrentYearStudent': 5},
    {'UserID': "2952678H", 'name': 'Sophie', 'YearEnrolled': 2023, 'CurrentYearStudent': 3},
    {'UserID': "2963789I", 'name': 'Daniel', 'YearEnrolled': 2022, 'CurrentYearStudent': 4},
    {'UserID': "2974890J", 'name': 'Olivia', 'YearEnrolled': 2024, 'CurrentYearStudent': 2},
    {'UserID': "2985901K", 'name': 'Ethan', 'YearEnrolled': 2023, 'CurrentYearStudent': 3},
    {'UserID': "2996012L", 'name': 'Charlotte', 'YearEnrolled': 2021, 'CurrentYearStudent': 5}
    ]


    Courses = [
    {"CourseID": "EDUC3078P", "CourseName": "Educational Elective 3"},
    {"CourseID": "EDUC4084P", "CourseName": "Educational Elective 4"},
    {"CourseID": "T2G-SCI", "CourseName": "Transition to Glasgow: Sciences"},
    {"CourseID": "BIOL4A", "CourseName": "Advanced Biology A"},
    {"CourseID": "BIOL4B", "CourseName": "Advanced Biology B"},
    {"CourseID": "COMP1001", "CourseName": "Introduction to Computing Science"},
    {"CourseID": "MATH1001", "CourseName": "Calculus 1"},
    {"CourseID": "PHYS1001", "CourseName": "Physics 1"},
    {"CourseID": "CHEM1001", "CourseName": "Fundamentals of Chemistry"},
    {"CourseID": "PSYC1001", "CourseName": "Introduction to Psychology"}
    ]

    Enrolls = [
    {"UserID": "2907132C", "CourseID": "BIOL4A"},
    {"UserID": "2907132C", "CourseID": "MATH1001"},
    {"UserID": "2918234D", "CourseID": "COMP1001"},
    {"UserID": "2918234D", "CourseID": "PSYC1001"},
    {"UserID": "2929345E", "CourseID": "T2G-SCI"},
    {"UserID": "2929345E", "CourseID": "PHYS1001"},
    {"UserID": "2930456F", "CourseID": "EDUC3078P"},
    {"UserID": "2930456F", "CourseID": "EDUC4084P"},
    {"UserID": "2941567G", "CourseID": "CHEM1001"},
    {"UserID": "2941567G", "CourseID": "MATH1001"},
    {"UserID": "2952678H", "CourseID": "PSYC1001"},
    {"UserID": "2952678H", "CourseID": "BIOL4B"},
    {"UserID": "2963789I", "CourseID": "PHYS1001"},
    {"UserID": "2963789I", "CourseID": "BIOL4A"},
    {"UserID": "2974890J", "CourseID": "EDUC3078P"},
    {"UserID": "2974890J", "CourseID": "T2G-SCI"},
    {"UserID": "2985901K", "CourseID": "BIOL4B"},
    {"UserID": "2985901K", "CourseID": "CHEM1001"},
    {"UserID": "2996012L", "CourseID": "COMP1001"},
    {"UserID": "2996012L", "CourseID": "MATH1001"}
    ]
    
    Notes = [
    {"ID" : 1 ,"Owner": "2907132C", "CourseID": "BIOL4A", "Topics": "Evolution and Gene Pool", "file": "Documents/test1.docx"},
    {"ID" : 2 ,"Owner": "2918234D", "CourseID": "COMP1001", "Topics": "Fundamentals of Python Programming", "file": "Documents/test2.docx"},
    {"ID" : 3 ,"Owner": "2929345E", "CourseID": "MATH1001", "Topics": "Limits and Differentiation", "file": "Documents/test3.docx"},
    {"ID" : 4 ,"Owner": "2930456F", "CourseID": "PHYS1001", "Topics": "Newton’s Laws of Motion", "file": "Documents/test4.docx"}
    ]

    edited_notes = [
        {"CourseID" : "BIOL4A", "ID" : 1, "File" : "Edited_Note/etest1.docx", "EditedID" : "2996012L"},
        {"CourseID" : "COMP1001", "ID" : 2, "File" : "Edited_Note/etest2.docx", "EditedID" : "2929345E"},
        {"CourseID" : "MATH1001", "ID" : 3, "File" : "Edited_Note/etest3.docx", "EditedID" : "2918234D"},
        {"CourseID" : "PHYS1001", "ID" : 4, "File" : "Edited_Note/etest4.docx", "EditedID" : "2952678H"}
    ]


    for student in students:
        userID = student.get("UserID")
        name = student.get("name")
        yearEnrolled = student.get('YearEnrolled')
        CurrentYear = student.get('CurrentYearStudent')

        add_student(userID,name,yearEnrolled,CurrentYear)

    for course in Courses:

        courseID = course.get("CourseID")
        CourseName = course.get("CourseName")

        add_course(courseID,CourseName)
    
    for enroll in Enrolls:
        userID = enroll.get("UserID")
        CourseID = enroll.get("CourseID")

        add_enroll(userID,CourseID)

    for note in Notes:
        Id = note.get("ID")
        Owner = note.get("Owner")
        CourseID = note.get("CourseID")
        Topic = note.get("Topics")
        file = note.get("file")

        add_note(Id,Owner,CourseID,Topic,file)
    
    for edits in edited_notes:
        NoteID = edits['ID']
        CourseID = edits['CourseID']
        file = edits['File']
        EditedID = edits['EditedID']
        add_edit(NoteID,CourseID,file,EditedID)
    
    


def add_student(userID,name,yearEnrolled,CurrentYear):

    s = Students.objects.get_or_create(UserID = userID, Name = name, YearEnrolled = yearEnrolled, CurrentYearStudent = CurrentYear)[0]
    s.save()
    return s

def add_course(courseID,CourseName):
    c =Courses.objects.get_or_create(CourseID=courseID,CourseName = CourseName)[0]
    c.save()
    return c

def add_enroll(userID,CourseID):
    student = Students.objects.get(UserID = userID)
    course = Courses.objects.get(CourseID = CourseID)
    e = Enrolls.objects.get_or_create(UserID = student, CourseID = course)[0]
    e.save()
    return e

def add_note(Id,Owner,CourseID,Topic,file):
    Owner = Students.objects.get(UserID = Owner)
    CourseID = Courses.objects.get(CourseID = CourseID)
    if Id is not None:
        n = Note.objects.update_or_create( 
            UserID=Owner,  # Lookup field
            CourseID=CourseID,  # Lookup field
            defaults={
                'Topics': Topic,
                'file': file,
                'DateUploaded': date.today().isoformat()
            })[0]
    else:
         n = Note.objects.get_or_create(UserID = Owner, CourseID = CourseID, Topics = Topic, file = file, DateUploaded = date.today().isoformat())[0]
    n.save()
    return n

def add_edit(NoteID,CourseID,file, EditedID):

    NoteID = Note.objects.get(NoteID = NoteID)
    CourseID = Courses.objects.get(CourseID = CourseID)
    EditedID = Students.objects.get(UserID = EditedID)
    
    e = EditedNotes.objects.get_or_create(UserID = EditedID, DateUploaded = date.today().isoformat(), CourseID = CourseID, NoteID = NoteID, file = file)[0]
    e.save()

    return e



def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name, views = views, likes = likes)[0]
    c.save()
    return c

if __name__ == '__main__':
    print("populating rango")
    populate()