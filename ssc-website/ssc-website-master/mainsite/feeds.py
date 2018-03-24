from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils import timezone
import mainsite

class Admission_feed(Feed):
	'''Feed class to implement the college admission notices
	'''
	title="Admission notices from college"
	link="/sitenews/"
	description="Updates regarding college admission notices"
	
	def items(self):
		notice_categ=mainsite.models.notification_category.objects.all()[2]
		return mainsite.models.notification.objects.filter(publish_date__lte=timezone.now()).filter(category=notice_categ).order_by('-publish_date')[:10]
	def item_title(self,item):
		return item.title
	def item_description(self,item):
		return item.description
	def item_link(self,item):
		return reverse('notice_detail',args=[item.pk])
class Notifications_feed(Feed):
	'''
	Feed class to implement the college Notifications class
	'''
	title="Notifications from college"
	link="/sitenews/"
	description="Updates on changes and additions to notifications by the college."

	def items(self):
		notice_categ=mainsite.models.notification_category.objects.first()
		return mainsite.models.notification.objects.filter(publish_date__lte=timezone.now()).filter(category=notice_categ).order_by('-publish_date')[:10]
	def item_title(self,item):
		return item.title

	def item_description(self,item):
		return item.description

	# item_link is only needed if NewsItem has no get_absolute_url method.
	def item_link(self,item):
		return reverse('notice_detail',args=[item.pk])
class Principal_feed(Feed):
	'''
	Feed class to implement a RSS feed for principal's desk
	'''
	title="Notifications from Principal's Desk"
	link="/sitenews/"
	description="Updates on changes and additions to the Principal's Desk."

	def items(self):
		notice=mainsite.models.notification_category.objects.all()[1]
		return mainsite.models.notification.objects.filter(publish_date__lte=timezone.now()).filter(category=notice).order_by('-publish_date')[:10]
	def item_title(self,item):
		return item.title

	def item_description(self,item):
		return item.description

	# item_link is only needed if NewsItem has no get_absolute_url method.
	def item_link(self,item):
		return reverse('notice_detail',args=[item.pk])
