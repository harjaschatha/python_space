from django.contrib import admin
from events.models import *

class PosterAdminInline(admin.TabularInline):
	model=Poster
	readonly_fields=['thumbnail']
class PhotoAdminInline(admin.TabularInline):
	model=Photo
	readonly_fields=['thumbnail']
class ScheduleAdminInline(admin.TabularInline):
	model=Schedule
class EventAdmin(admin.ModelAdmin):
	inlines=[ScheduleAdminInline,PosterAdminInline,PhotoAdminInline]
admin.site.register(Event,EventAdmin)
