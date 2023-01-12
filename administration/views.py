from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from api.publications.models import Publication
from api.ratings.models import Ratings
from api.reports.models import Report, FeedbackReport, TypeResolution
from api.users.models import Users
from api.users.services import send_notification


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        reports = Report.objects.filter(closed=False)
        reports.order_by("-date_reported")
        resolutions = TypeResolution.objects.all()
        return render(request, "index.html", {"reports":reports,"resolutions": resolutions})
    else:
        return redirect("signin")

def users(request):
    if request.user.is_authenticated:
        users = Users.objects.all()
        users=users.order_by("id")
        return render(request, "users.html", {"users": users})
    else:
        return redirect("signin")

def change_user(request, user_id):
    if request.user.is_authenticated:
        user = Users.objects.get(id=user_id)
        if request.POST.get("is_staff"):
            user.is_staff=True
        else:
            user.is_staff = False
        if request.POST.get("is_active"):
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        return redirect("gestio_usuaris")
    else:
        return redirect("signin")


def solve_report(request, report_id):
    report = Report.objects.get(id=report_id)
    action = int(request.POST.get("action"))
    message = request.POST.get("message")

    feedback = FeedbackReport()
    feedback.message = message
    feedback.moderator = request.user
    feedback.report_id = report_id
    feedback.resolution = TypeResolution.objects.get(id=action)
    feedback.save()
    if action == 2:
        if report.rating:
            send_notification(report.rating.user,"Amonestacion de conducta -> Uno de tus comentarios ha sido reportado", message)
        elif report.publication:
            send_notification(report.publication.owner, "Amonestacion de publicacion", "La publicacion con titulo:\"" + report.publication.title + " ha infringido alguna norma. Por favor, modificala. Mensaje del moderador: " + message)
        elif report.reported_user:
            send_notification(report.reported_user,"Amonestacion de conducta -> Incumplimiento de la normativa", message)
    elif action==3:
        if report.rating:
            rating = Ratings.objects.get(id=report.rating.id)
            rating.active=False
            rating.save()
        elif report.publication:
            publication = Publication.objects.get(id = report.publication.id)
            publication.active=False
            publication.save()
        elif report.reported_user:
            user = Users.objects.get(id=report.reported_user.id)
            user.is_active=False
            user.save()
    report.closed=True
    report.save()
    return redirect("Home")

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
                if user.is_staff and user.is_active:
                    login(request,user)
                    return redirect("Home")
                else:
                    errors.append("No tienes permiso para acceder a esta página. Contacta con un administrador si se trata de un error.")
            else:
                errors.append("La contraseña no es correcta")
        else:
            errors.append("El usuario no existe")
    return render(request,"signin.html", {"errors":errors})
def signout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("signin")