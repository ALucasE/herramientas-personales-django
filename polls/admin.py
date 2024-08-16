from django.contrib import admin
from .models import Choice, Poll, Vote

# Register your models here.
class choiceTabularInline(admin.TabularInline):
    model=Choice
    readonly_fields =  ["votes",]


class PollAdmin(admin.ModelAdmin):
    list_display = ["title", "pub_date", "creator"]
    list_filter = ["pub_date"]
    search_fields = ["title"]
    inlines = [choiceTabularInline]
    readonly_fields =  ["pub_date", "creator"]

admin.site.register(Poll, PollAdmin)


admin.site.register(Choice)

admin.site.register(Vote)