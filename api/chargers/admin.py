from django.contrib import admin
from api.chargers.models import Chargers, Publication, SpeedsType, ConnectionsType, CurrentsType


# Register your models here.
class ChargersAdmin(admin.ModelAdmin):
    search_fields = ('power', 'speed', 'connection_type', 'current_type')
    list_display = ('power', 'get_speed', 'get_connection_type', 'get_current_type')

    def get_speed (self, obj):
        return "\n".join([p.name for p in obj.speed.all()])

    def get_connection_type (self, obj):
        return "\n".join([p.name for p in obj.connection_type.all()])

    def get_current_type (self, obj):
        return "\n".join([p.name for p in obj.current_type.all()])


class PubliChargerAdmin(admin.ModelAdmin):
    search_fields = ('agent', 'identifier', 'access', 'available')
    list_display = ('agent', 'identifier', 'access', 'available')


class SpeedsTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'localization', 'direction', 'town')
    search_fields = ('title', 'description', 'localization', 'direction', 'town')


class LocalizationsAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude')
    search_fields = ('latitude', 'longitude')


class TownAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    search_fields = ('name', 'province')


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ConnectionsTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CurrentsTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Chargers, ChargersAdmin)
admin.site.register(SpeedsType, SpeedsTypeAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(ConnectionsType, ConnectionsTypeAdmin)
admin.site.register(CurrentsType, CurrentsTypeAdmin)
