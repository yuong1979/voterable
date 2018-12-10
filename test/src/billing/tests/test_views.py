import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from django.contrib.auth.models import User
from .. import views
pytestmark = pytest.mark.django_db
from polls.views import PollDetailView
from django.test import Client
from django.test import TestCase
from polls.models import PollItem, Ptype
from users.models import PUser
from polls.views import PollsListView

from datetime import datetime, timedelta




class TestBillingViews(TestCase):

	def setUp(self):
		self.client = Client()

		#create user who is not signed in or not
		self.user = User.objects.create_user(
			username='normaluser', email='s@gmail.com', password='secret123')

		self.basicuser = User.objects.create_user(
			username='basicuser', email='s@gmail.com', password='secret123')

		self.premiumuser = User.objects.create_user(
			username='premiumuser', email='s@gmail.com', password='secret123')

		self.adminuser = User.objects.create_user(
			username='adminuser', email='s@gmail.com', password='secret123', is_staff=True)


		obj_puser = mixer.blend('users.PUser', user=self.user)
		obj_puser_basic = mixer.blend('users.PUser', user=self.basicuser, member=True)
		obj_puser_premium = mixer.blend('users.PUser', user=self.premiumuser, pmember=True)
		obj_puser_staff = mixer.blend('users.PUser', user=self.adminuser)


		obj_transactionb = mixer.blend('billing.Transaction', user=self.basicuser)
		obj_transactionp = mixer.blend('billing.Transaction', user=self.premiumuser)

		obj_pricetodays02 = mixer.blend('billing.PriceToDays', active=True, subplan="Plan02", cashprice=20, daystoadd=30)
		obj_pricetodays03 = mixer.blend('billing.PriceToDays', active=True, subplan="Plan03", cashprice=40, daystoadd=60)
		obj_pricetodays04 = mixer.blend('billing.PriceToDays', active=True, subplan="Plan05", cashprice=60, daystoadd=90)

		obj_puser_basic.substartdate = datetime.now()
		obj_puser_basic.subenddate = datetime.now() + timedelta(days=365)
		obj_puser_basic.member = True
		obj_puser_basic.save()

		obj_puser_premium.substartdatep = datetime.now()
		obj_puser_premium.subenddatep = datetime.now() + timedelta(days=365)
		obj_puser_premium.memberp = True
		obj_puser_premium.save()






	def test_transaction_view(self):

		path = reverse('SelectPlan')

		#cannot be viewed by users not signed in
		res = self.client.get(path)
		assert res.status_code == 302, 'Cannot be viewed by users not logged in'

		#can be viewed by users who are signed in
		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 200, 'Can be viewed by users logged in'



	def test_checkout_view(self):

		path = reverse('StripeCheckOut')

		res = self.client.get(path)
		assert res.status_code == 302, 'Cannot be viewed by users not logged in'

		self.client.login(username="normaluser", password="secret123")

		res = self.client.get(path)
		assert res.status_code == 404, 'User cannot view without a selected plan'

		session = self.client.session
		session['subtype_id'] = 1
		session.save()

		res = self.client.get(path)
		assert res.status_code == 200, 'Can be viewed by users logged in with a selected plan'





	def test_successsub_view(self):

		path = reverse('SuccessSub')

		res = self.client.get(path)
		assert res.status_code == 302, 'Cannot be viewed by users not logged in'

		self.client.login(username="normaluser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 404, 'Normal User cannot view without a selected plan'

		self.client.login(username="basicuser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 404, 'Basic User cannot view without a selected plan'

		self.client.login(username="premiumuser", password="secret123")
		res = self.client.get(path)
		assert res.status_code == 404, 'Premium User cannot view without a selected plan'


		# session = self.client.session
		# session['subtype_id'] = 1
		# session.save()


		# self.client.login(username="normaluser", password="secret123")
		# res = self.client.get(path)
		# assert res.status_code == 404, 'Normal User cannot view without a selected plan'

		# self.client.login(username="basicuser", password="secret123")
		# res = self.client.get(path)
		# assert res.status_code == 200, 'Basic User cannot view without a selected plan'

		# self.client.login(username="premiumuser", password="secret123")
		# res = self.client.get(path)
		# assert res.status_code == 200, 'Premium User cannot view without a selected plan'





		# # self.client.login(username="normaluser", password="secret123")
		# # assert res.status_code == 200, 'Normal User cannot view - error'

		# self.client.login(username="basicuser", password="secret123")
		# session = self.client.session
		# session['subtype_id'] = 1
		# session.save()
		# print (session.keys())
		# print (session.values())
		# assert res.status_code == 200, 'Basic User can view'

		# self.client.login(username="premiumuser", password="secret123")
		# assert res.status_code == 200, 'Premium User can view'




		# # need to include the normal user trying to access will fail
		# self.client.login(username="normaluser", password="secret123")


		# session = self.client.session
		# session['subtype_id'] = 1
		# session.save()


		# res = self.client.get(path)
		# assert res.status_code == 200, 'Basic User cannot view without a selected plan'

		# self.client.login(username="basicuser", password="secret123")
		# res = self.client.get(path)
		# assert res.status_code == 404, 'Basic User cannot view without a selected plan'

		# self.client.login(username="premiumuser", password="secret123")
		# res = self.client.get(path)
		# assert res.status_code == 404, 'Premium cannot view without a selected plan'



