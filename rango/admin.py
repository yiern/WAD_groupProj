from django.contrib import admin
from rango.models import Category, Page
from .models import Question, Choice
from rango.models import UserProfile


# Register your models here.

class ChoiceAdmin(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]


    inlines = [ChoiceAdmin]

    list_display = ('question_text', 'pub_date', 'was_published_recently')
    search_fields = ['question_text']
    list_filter = ['pub_date']

class PageAdmin(admin.ModelAdmin):
   list_display = ('title','category','url')
   search_fields = ['title']

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Question, QuestionAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(UserProfile)