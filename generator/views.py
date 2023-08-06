from datetime import datetime, time, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from .models import Class, Subject, Teacher, Lecture
import json
from random import shuffle
from colorama import Fore

# Create your views here.


def index(request):
    return redirect("generator:register")


def home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("classname"):
                class_obj = Class()
                class_obj.name = (
                    request.POST.get("classname") + " " + request.POST.get("division")
                )
                class_obj.author = request.user
                class_obj.sem_start = request.POST.get("sem-start")
                class_obj.sem_end = request.POST.get("sem-end")
                class_obj.start_time = request.POST.get("time-start")
                class_obj.end_time = request.POST.get("time-end")
                class_obj.break_start = request.POST.get("break-time-start")
                class_obj.break_end = request.POST.get("break-time-end")
                class_obj.save()
                request.session["class_id"] = class_obj.id
                return redirect("generator:form1", res_name=2)
        class_data = Class.objects.filter(author=request.user)
        print(class_data)

        context = {}

        for cls in class_data:
            subjects = cls.subjects.all()
            context[cls.name] = subjects

            print(Fore.RED)
            print(context)
            print(class_data)

            print(Fore.RESET)
        return render(
            request,
            "generator/main.html",
            {"classes": class_data, "subjects": context},
        )
    else:
        return redirect("generator:register")


def form1_view(request, res_name):
    if request.method == "POST":
        class_id = request.session["class_id"]
        if not class_id:
            return redirect("generator:home")
        class_obj = Class.objects.get(id=class_id)
        if request.POST.get("subject1"):
            for i in range(10):
                try:
                    subject = Subject()
                    subject.name = request.POST.get(f"subject{i+1}")
                    subject.no_lec = request.POST.get(f"lectures{i+1}")
                    subject.author = request.user
                    color = ["#FF9090", "#FFEA7D", "#ACCDFF", "#FFADED", "#ADA6FF"]
                    if request.POST.get(f"subject{i+1}") == "Science":
                        subject.color = "#FF9090"
                    elif request.POST.get(f"subject{i+1}") == "English":
                        subject.color = "#FFEA7D"
                    elif request.POST.get(f"subject{i+1}") == "Hindi":
                        subject.color = "#ADA6FF"
                    subject.save()
                    class_obj.subjects.add(subject.id)
                    class_obj.save()
                except:
                    break
            return redirect("generator:home")

    return render(request, "generator/main.html")


def generate_timetables(request, resname):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    class_obj = Class.objects.get(id=resname)

    teachers = Teacher.objects.filter(classes__has_key=class_obj.id)

    for day in days:
        subjects = class_obj.subjects.all()
        subject2 = list(subjects)
        shuffle(subject2)
        for subject in subject2:
            # Check if lecture already exists
            if Lecture.objects.filter(day=day, subject=subject).exists():
                continue
            teacher = None
            if teachers.exists():
                teacher = teachers.first()

            # Create lecture
            lecture = Lecture()
            lecture.day = day
            lecture.start_time = class_obj.start_time
            lecture.end_time = class_obj.end_time
            lecture.subject = subject
            lecture.teacher = teacher
            lecture.class_id = class_obj
            lecture.color = subject.color
            lecture.save()
            # ...rest of lecture creation...

    lectures = Lecture.objects.filter(class_id=class_obj)
    print(Fore.YELLOW)
    suffix = str(class_obj.start_time).split(":")[1]
    print(lectures)
    time = int(str(class_obj.start_time).split(":")[0])
    print(time)
    etime = int(str(class_obj.end_time).split(":")[0])
    print(etime)

    alltime = []

    for i in range(time, etime):
        alltime.append(str(i) + " : " + suffix)
    print(Fore.RESET)

    context = {"lectures": lectures, "alltime": alltime, "days": days}

    return render(request, "generator/timetable.html", context)


def form2_view(request, res_name):
    if request.method == "POST":
        teacher_id = request.session["teacher_id"]
        if not teacher_id:
            return redirect("generator:teacher")

        dict = {}
        teacher_obj = Teacher.objects.get(id=teacher_id)
        data = {}
        class_data = Class.objects.filter(author=request.user)
        for class1 in class_data:
            data[class1.name] = []
            for subject in request.POST.getlist("selected"):
                classname, sub = subject.split("-")
                data[classname].append(sub)

        context = json.dumps(data)
        teacher_obj.classes = context
        teacher_obj.save()
        print(context)

        return redirect("generator:teacher")
    class_data = Class.objects.filter(author=request.user)

    context = {}

    for cls in class_data:
        subjects = cls.subjects.all()
        context[cls.name] = subjects

    print(Fore.RED)
    print(context)
    print(class_data)

    print(Fore.RESET)
    return render(request, "generator/teachers.html", {"cxt": context})


def teacher(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("teachername"):
                teacher_obj = Teacher()
                teacher_obj.author = request.user
                teacher_obj.name = request.POST.get("teachername")
                teacher_obj.start_time = request.POST.get("time-start")
                teacher_obj.end_time = request.POST.get("time-end")
                teacher_obj.break_end = request.POST.get("break-start")
                teacher_obj.break_start = request.POST.get("break-end")
                teacher_obj.save()
                request.session["teacher_id"] = teacher_obj.id
                return redirect("generator:form2", res_name=2)
        teacher_data = Teacher.objects.filter(author=request.user)
        print(Fore.GREEN)
        # print(teacher_data[3].classes.all())
        a = {}
        for teacher in teacher_data:
            try:
                a[teacher.name] = json.loads(teacher.classes)

            except:
                pass
        print(a)
        print(Fore.RESET)
        return render(
            request, "generator/teachers.html", {"teachers": teacher_data, "classes": a}
        )
    else:
        return redirect("generator:register")


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("generator:home")
    context = {"form": form}
    return render(request, "generator/signup.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("../")
    else:
        return redirect("../")
