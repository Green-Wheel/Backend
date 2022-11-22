# Register your models here.
from django.contrib import admin
from api.bookings.models import Bookings


# Register your models here.
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'publication', 'start_date', 'end_date', 'created')
    search_fields = ('user', 'publication', 'start_date', 'end_date', 'created')


admin.site.register(Bookings, BookingsAdmin)
