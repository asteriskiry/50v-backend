import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Participant


class ParticipantAdmin(admin.ModelAdmin):
    empty_value_display = "Ei täytetty"
    data_hierarchy = "ctime"
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    list_display = ("first_name", "last_name", "email", "is_invited", "is_in_reserve")
    list_filter = ("is_invited", "is_in_reserve", "is_attending_sillis", "is_greeting")
    fields = (
        "ctime",
        "mtime",
        "first_name",
        "last_name",
        "starting_year",
        "email",
        "is_asteriski_member",
        "is_alcohol_free",
        "is_vege",
        "excretory_diets",
        "is_attending_sillis",
        "avecs_name",
        "other_info",
        "is_greeting",
        "is_invited",
        "is_in_reserve",
        "party_representing",
        "dont_show_name",
        "is_consenting",
    )
    readonly_fields = ("ctime", "mtime")
    actions = ("export_as_csv",)

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        verbose_names = [field.verbose_name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(verbose_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Vie Exceliin valitut"


admin.site.register(Participant, ParticipantAdmin)
