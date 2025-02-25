from django.contrib import admin

from airport.models import (
    Ticket,
    Order,
    Country,
    City,
    Airport,
    Airplane,
    AirplaneType,
    Crew,
    Route
)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInline,)


admin.site.register(City)
admin.site.register(Country)
admin.site.register(Airport)
admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Crew)
admin.site.register(Route)
