import pytest
from mixer.backend.django import mixer
from django.contrib.admin.sites import AdminSite
pytestmark = pytest.mark.django_db
from django.contrib.auth.models import User
from .. import admin
from .. import models

class TestAnalyticsAdmin:
	def test_ptype__str__(self):
		site = AdminSite()
		polls_admin = admin.ViewPollTypeUniqueAdmin(models.ViewPollTypeUnique, site)
		pobj = mixer.blend('polls.Ptype')

		uobj = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')
		obj = mixer.blend('analytics.ViewPollTypeUnique', p_type=pobj)

		result = polls_admin.__str__(obj)
		assert result == str(obj.p_type), 'Should return the title'


	def test_pitem__str__(self):
		site = AdminSite()
		polls_admin = admin.ViewPollItemsUniqueAdmin(models.ViewPollItemsUnique, site)
		pobj = mixer.blend('polls.PollItem')

		uobj = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')
		obj = mixer.blend('analytics.ViewPollItemsUnique', p_item=pobj)
		obj.userview.add(uobj)

		result = polls_admin.__str__(obj)
		assert result == str(obj.p_item), 'Should return the pollitem'

