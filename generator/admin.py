from django.contrib import admin
from .models import Class, Subject, Teacher, Lecture

# Register your models here.
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Lecture)
