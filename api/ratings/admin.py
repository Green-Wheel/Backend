from django.contrib import admin
from api.ratings.models import Ratings


# Register your models here.
class RatingsAdmin(admin.ModelAdmin):
    list_display = ('rate', 'comment', 'booking')
    search_fields = ('rate', 'comment', 'booking')


admin.site.register(Ratings, RatingsAdmin)
