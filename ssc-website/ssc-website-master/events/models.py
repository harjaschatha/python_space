from django.core.urlresolvers import reverse
from django.db import models
from django import forms
from office.models import deptsoc


from datetime import date
from calendar import HTMLCalendar as HTMLCalender
from django.utils.html import conditional_escape as esc
from itertools import groupby

class Location(models.Model):
	'''
	Locations where events need to be booked
	'''
	def __unicode__(self):
		return str(self.name)
		
	name=models.CharField(max_length=40)
	
	projector=models.BooleanField(default=False)#has projector
	ac=models.BooleanField(default=False)#has ac
	lights=models.BooleanField(default=False)#has lights
	board=models.BooleanField(default=True)#has black/white board

class Event(models.Model):
	'''
	Event in college
	'''
	def __unicode__(self):
		return self.name
	name=models.CharField(max_length=40)
	nickname=models.CharField(max_length=10)#nickname for url
	description=models.TextField(blank=True)
	organizer=models.ForeignKey(deptsoc)#who has organized this
	start=models.DateTimeField()
	end=models.DateTimeField()
	def get_absolute_url(self):
		return reverse('event_detail',args=[self.nickname])
		
class Schedule(models.Model):
	'''Schedule for an event
	'''
	title=models.CharField(max_length=50)
	description=models.TextField(blank=True)
	location=models.ForeignKey(Location,related_name='location')
	start=models.DateTimeField()
	end=models.DateTimeField()
	event=models.ForeignKey(Event,related_name='event')
	

class Poster(models.Model):
	'''
	Posters for event
	'''
	tag=models.CharField(max_length=20,blank=True)
	picture=models.ImageField(upload_to='events/posters/%y/%m/%d')
	event=models.ForeignKey(Event)
	def thumbnail(self):
	        if self.picture:
	        	addr=self.picture.url
	        	addr.strip('/')
	                return u'<img src="'+addr+'" width=60 height=60 />'
	        else:
	        	return u'No image file found'
	thumbnail.short_description ='Thumbnail'
	thumbnail.allow_tags=True
	
class Photo(models.Model):
	'''
	Photos of events
	'''
	tag=models.CharField(max_length=20,blank=True)
	picture=models.ImageField(upload_to='events/photos/%y/%m/%d')
	event=models.ForeignKey(Event)
	def thumbnail(self):
	        if self.picture:
	        	addr=self.picture.url
	        	addr.strip('/')
	                return u'<img src="'+addr+'" width=60 height=60 />'
	        else:
	        	return u'No image file found'
	thumbnail.short_description ='Thumbnail'
	thumbnail.allow_tags=True	
	
	
	
class EventCalender(HTMLCalender):
	'''
	creates a calender with the provided events.
	Reference from
	
		http://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/
		
		https://docs.python.org/2/library/calendar.html#calendar.HTMLCalendar
	'''
	def __init__(self,events):
		super(EventCalender, self).__init__()
	        self.events = self.group_by_day(events)
	def group_by_day(self,events):
		'''
		groups by day
		'''
		field=lambda event: event.start.day
		return dict(
		            [(day, list(items)) for day, items in groupby(events, field)]
		                    )
	def formatmonth(self,year,month):
		self.year,self.month=year,month
		return super(EventCalender,self).formatmonth(year,month)
	def formatday(self,day,weekday):
		if day != 0:
	            cssclass = self.cssclasses[weekday]
	            if date.today() == date(self.year, self.month, day):
	                cssclass += ' today'
	            if day in self.events:
	                cssclass += ' filled'
	                body = ['<ul>']
	                for event in self.events[day]:
	                    body.append('<li>')
	                    body.append('<a href="%s">' % event.get_absolute_url())
	                    body.append(esc(event.name))
	                    body.append('</a></li>')
	                body.append('</ul>')
	                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
	            return self.day_cell(cssclass, day)
	        return self.day_cell('noday', '&nbsp;')
	def day_cell(self, cssclass, body):
	        return '<td class="%s">%s</td>' % (cssclass, body)
