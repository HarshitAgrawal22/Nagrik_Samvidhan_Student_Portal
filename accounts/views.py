from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from icecream import ic
from .models import Student, Instructor

# ===================================== LOGIN ==============================


def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")

        if Student.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                try:
                    auth.login(request, user)
                    return redirect("student")
                except:
                    messages.error(request, "Invalid Password")
                    return redirect("login")

            else:
                messages.error(request, "Invalid Password")
                return redirect("login")

        elif Instructor.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("administration")

            else:
                messages.error(request, "Invalid Password")
                return redirect("login")

        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("login")
    ic(request)
    return render(request, "accounts/index.html")


# ===================================== REGISTER ==============================


def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        first_name = request.POST.get("name").split(" ")[0].strip().title()
        last_name = request.POST.get("name").split(" ")[1].strip().title()
        email = request.POST.get("email").strip().lower()
        mobile_number = request.POST.get("mobile_number")
        gender = request.POST.get("gender")
        college = request.POST.get("college")
        password = request.POST.get("password")
        ic(
            username,
            first_name,
            last_name,
            email,
            mobile_number,
            gender,
            college,
            password,
        )
        if Student.objects.filter(username=username).exists():
            ic("username alrady exists")
            messages.error(request, "Username already exists!")
            return redirect("register")

        if Student.objects.filter(email=email).exists():
            ic("email alrady exists")
            messages.error(request, "Email already exists!")
            return redirect("register")

        if Student.objects.filter(mobile_number=mobile_number).exists():
            ic("mobilee alrady exists")
            messages.error(request, "Mobile Number already exists!")
            return redirect("register")

        if (
            len(mobile_number) != 10
            or not mobile_number.isdigit()
            or mobile_number[0] in "012345"
        ):
            messages.error(request, "Invalid Mobile Number!")
            ic("number problem ")
            return redirect("register")

        new_user = Student.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            gender=gender,
            college=college,
        )
        new_user.set_password(password)
        new_user.save()

        messages.success(
            request,
            "Account created successfully! Please login. Use password 'angaarhai' to login.",
        )
        ic("going to login ")
        return redirect("login")

    return render(request, "accounts/index.html")


# =================================== logout ============================


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("login")


# ====================== check Email availability ====================


def check_username_availability(request):
    username = request.GET.get("username", "")
    data = {"is_available": not Student.objects.filter(username=username).exists()}
    return JsonResponse(data)


# ====================== block student ====================


@login_required(login_url="login")
@staff_member_required(login_url="login")
def block_student(request, id):
    student = Student.objects.get(id=id)
    student.is_active = not student.is_active
    student.save()

    messages.success(request, f"{student.username} is blocked successfully!")

    return redirect("all_students")


# ====================== unblock student ====================


@login_required(login_url="login")
@staff_member_required(login_url="login")
def unblock_student(request, id):
    student = Student.objects.get(id=id)
    student.is_active = not student.is_active
    student.save()

    messages.success(request, f"{student.username} is unblocked successfully!")

    return redirect("all_students")


# ============================ 404 ===============


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)
