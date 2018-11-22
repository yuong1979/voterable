from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from polls.models import PollItem, Ptype
from django.utils import timezone
import pytz

# Create your models here.

class ViewPollTypeUnique(models.Model):
	p_type = models.OneToOneField(Ptype, blank=True, default=None)
	userview = models.ManyToManyField(User, blank=True, default=None)
	vcount = models.IntegerField(default=0)#counting the number views
	ecount = models.IntegerField(default=0)#counting the number of entries on a poll type
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.p_type)

	def get_user_count(self):
		count = self.userview.count()
		return count

	def get_url(self):
		url = "/polls/?type=" + str(self.p_type.slug)
		return url

class ViewPollItemsUnique(models.Model):
	p_item = models.OneToOneField(PollItem, blank=True, default=None)
	userview = models.ManyToManyField(User, blank=True, default=None)
	vcount = models.IntegerField(default=0)#counting the number views
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.p_item)

	def get_user_count(self):
		count = self.userview.count()
		return count



class Ranking(models.Model):
	title = models.CharField(max_length=100, unique=True)
	low_score = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
	high_score = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True)
	add_days = models.IntegerField(default=0)


	def __str__(self):
		return str(self.title)



class ScorePollItemsByMonth(models.Model):
	p_item = models.ForeignKey(PollItem)
	year = models.IntegerField(default=0)
	month = models.CharField(max_length=3)
	posi = models.IntegerField(default=0)
	nega = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.p_item)




class ScoreUserByMonth(models.Model):
	Puser = models.ForeignKey(User)
	year = models.IntegerField(default=0)
	month = models.CharField(max_length=3)
	score = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.Puser)




class PostReport(models.Model):
	usercon = models.CharField(max_length=100)
	Puser = models.ForeignKey(User, default=None)
	p_item = models.ForeignKey(PollItem)
	postissue = models.CharField(max_length=30)
	postissuemsg = models.CharField(max_length=100)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.p_item)
