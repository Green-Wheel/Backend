from api.publications.models import Publication
from api.ratings.models import Ratings
from api.reports.models import Report, ReportReasons


def create_rating_report(rating_id,data, user_id):
    if Report.objects.filter(rating_id=rating_id, user_id=user_id).exists():
        raise Exception("You have already reported this rating")

    rating_data = Ratings.objects.get(id=rating_id)
    if rating_data.user_id == user_id:
        raise Exception("You cannot report your own rating")

    if not rating_data.active:
        raise Exception("You cannot report an inactive rating")

    report_type = ReportReasons.objects.get(id=data["reason"])

    report = Report()
    report.user = user_id
    report.rating = rating_id
    report.reason = report_type
    report.message = data["message"]
    report.save()

def create_publication_report(publication_id,data, user_id):
    if Report.objects.filter(publication_id=publication_id, user_id=user_id).exists():
        raise Exception("You have already reported this publication")

    publication_data = Publication.objects.get(id=publication_id)
    if publication_data.user_id == user_id:
        raise Exception("You cannot report your own publication")

    if not publication_data.active:
        raise Exception("You cannot report an inactive publication")

    report_type = ReportReasons.objects.get(id=data["reason"])

    report = Report()
    report.user = user_id
    report.publication = publication_id
    report.reason = report_type
    report.message = data["message"]
    report.save()

def create_user_report(reported_user,data, user_id):
    if Report.objects.filter(reported_user_id=reported_user, user_id=user_id).exists():
        raise Exception("You have already reported this user")

    if reported_user == user_id:
        raise Exception("You cannot report yourself")

    report_type = ReportReasons.objects.get(id=data["reason"])

    report = Report()
    report.user = user_id
    report.reported_user = reported_user
    report.reason = report_type
    report.message = data["message"]
    report.save()

def get_report_reasons():
    return ReportReasons.objects.all()