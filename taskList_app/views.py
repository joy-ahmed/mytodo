from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    avatar = None
    try:
        avatar = ProfileImg.objects.get(user=request.user).profileImg
    except:
        avatar = ""

    return render(request, 'home.html', {"avatar": avatar})


def howitworks(request):
    avatar = None
    try:
        avatar = ProfileImg.objects.get(user=request.user).profileImg.url
    except:
        avatar = ""
    return render(request, 'howitworks.html', {"avatar": avatar})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('all-task')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect("all-task")
        return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')


def signupPage(request):
    if request.user.is_authenticated:
        return redirect('all-task')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password_one = request.POST.get("password_one")
            password_two = request.POST.get("password_two")
            avatar = request.FILES["avatar"]
            if password_one == password_two:
                user = User(
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = make_password(password_one),
                )
                user.save()

                user_avatar = ProfileImg(
                    profileImg = avatar,
                    user = user
                )

                user_avatar.save()

                return redirect("login")
            else:
                return redirect('signup')
        return render(request, 'signup.html')



@login_required
def allTasks(request):
    avatar = None
    try:
        avatar = ProfileImg.objects.get(user=request.user).profileImg.url
    except:
        avatar = ""

    task = TaskList.objects.all()
    users = User.objects.all()

    return render(request, "tasklist.html", {"avatar": avatar, "tasks": task, "users": users})



def addTask(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        done = request.POST.get('done')

        user_id = request.POST.get('user')
        user = User.objects.get(pk=user_id) if user_id else None

        if done == 'on':
            done = True
        else:
            done = False

        task = TaskList(
            title = title,
            done = done,
            user = user
        )

        task.save()

        return redirect('all-task')
    

def deleteTask(request, task_id):
    if request.user.is_authenticated:
        task = TaskList.objects.get(id = task_id)
        if task.user == request.user or request.user.is_superuser:
            task.delete()
        else:
            messages.error(request, "You are not authorized for this action.")
        return redirect('all-task')
    else:
        return redirect('login')
    


def editTask(request, task_id):
    if request.user.is_authenticated:
        task = TaskList.objects.get(id=task_id)
        if task.user == request.user or request.user.is_superuser:
            if request.method == 'POST':
                title = request.POST.get('title')
                done = request.POST.get('done')
                user_id = request.POST.get('user')
                user = User.objects.get(pk=user_id)
                if done == 'on':
                    done = True
                else:
                    done = False

                task.title = title
                task.done = done
                task.user = user
                task.save()
                return redirect('all-task')
        else:
            messages.error(request, "You are not authorized for this action.")
        
    return redirect('all-task')
