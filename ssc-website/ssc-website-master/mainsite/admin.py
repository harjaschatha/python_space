from django.contrib import admin
from mainsite.models import *

class home_slideshow_photo_admin(admin.ModelAdmin):
	'''Admin for home_slideshow_photo'''
	fields=['name','associated_photo','description']
	list_display=['thumbnail','name','associated_photo','description']
	search_fields=['name','description']
class SlotAdminInline(admin.TabularInline):
	model=Slot
class notification_admin(admin.ModelAdmin):
	'''Admin for notification'''
	list_display=['title','publish_date','recent','pinned','category']
	list_filter=['publish_date','pinned']
	search_fields=['title','description']
	inlines=[SlotAdminInline]

admin.site.register(home_slideshow_photo,home_slideshow_photo_admin)
admin.site.register(notification,notification_admin)
admin.site.register(notification_category)
