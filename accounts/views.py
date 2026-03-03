from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ROLE BASED REDIRECT
            if user.is_superuser:
                return redirect("/adminpanel/")

            elif hasattr(user, "staff"):
                return redirect("/staff/")

            elif hasattr(user, "student"):
                return redirect("/student/")

            else:
                return redirect("/")

        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")
