from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings


class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sem_start = models.DateField()
    sem_end = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_start = models.TimeField()
    break_end = models.TimeField()
    subjects = models.ManyToManyField("Subject")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    no_lec = models.IntegerField(default=0)
    color = models.CharField(max_length=10, default="#ffffff")

    def __str__(self):
        return self.name


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_start = models.TimeField()
    break_end = models.TimeField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    classes = models.JSONField(null=True)


class Lecture(models.Model):
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, null=True)
    day = models.CharField(max_length=10, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    class_id = models.ForeignKey("Class", on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=10, default="#ffffff")
