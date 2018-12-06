from django.test import TestCase

# Create your tests here.


from django.test import TestCase
from polls.models import PollItem, PollVoting, PollFav, Ptype, SuggestedPoll
from django.contrib.auth.models import User
import datetime
from django.urls import reverse


#list of asserts
# self.assertIs(test(), False)
# self.assertEqual(response.status_code, 200)
# self.assertContains(response, "No entry is available")
# self.assertQuerysetEqual(response.context['latest_question_list'], []) #[] meaning that its empty





# from polls.models import Animal

# class AnimalTestCase(TestCase):
#     def setUp(self):
#         Animal.objects.create(name="lion", sound="roar")
#         Animal.objects.create(name="cat", sound="meow")

#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         lion = Animal.objects.get(name="lion")
#         cat = Animal.objects.get(name="cat")
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')




def setup_ptype():

	user = User.objects.filter(pk=2)
	date = timezone.now()

	# Ptype.objects.create(
	# 	c_user=user,
	# 	title="testing",
	# 	year=2017,
	# 	location="testing",
	# 	topic="testing",
	# 	image="testing",
	# 	active=True,
	# 	date=date,
	# 	freepoll=True,
	# 	vote_count=0,
	# 	locked=False
	# 	)


	# PollItem.objects.create()
	# PollVoting.objects.create()
	# PollFav.objects.create()


	




def test():
	tester = False
	return tester


class test_ptype(TestCase):
	# def setUp(self):
	#     Ptype.objects.create(name="lion", sound="roar")

	def test_123(self):

		response = self.client.get(reverse('poll_topics'))

		print (response)

		self.assertIs(test(), False)

