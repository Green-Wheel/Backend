from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from api.users.models import Users


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        return redirect("signin")


def signin(request):
    if request.user.is_authenticated:
        return redirect("Home")
    errors=[]
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        check_if_user_exists = Users.objects.filter(username=username).exists()
        if check_if_user_exists:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect("Home")
            else:
                errors.append("La contraseña no es correcta")
        else:
            errors.append("El usuario no existe")
    return render(request,"signin.html", {"errors":errors})
def signout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("signin")