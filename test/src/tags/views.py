import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
# Create your views here.
from rest_framework.decorators import action
from tags.models import TagPoll, runtagcount
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from polls.models import Ptype
from tags.forms import TagSearchForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from users.models import PUser
from tags.models import TagPoll, runtagcount


@action(detail=True, methods=["GET"],url_name="search",url_path="/search/")
def Tagsearch(request):

	search = request.GET.get('search')

	# update the number of tags count to only count the number of active tags
	context = {}

	# exclude inactive polls
	exin = Ptype.objects.filter(active=True)
	taglist = TagPoll.objects.filter(active=True, polltype__in=exin).distinct()

	# ptype = Ptype.objects.filter(active=True)
	taglist = taglist.exclude(title="").order_by('title')

	if search:
		taglist = taglist.filter(title__icontains=search)
		# taglist = taglist.filter(title__istartswith=search)

	return_data = []

	i=0

	for tag in taglist:
		# print(type(tag.get_absolute_url()))
		return_data.append({
			'title': taglist.values()[i]['title'],
			'counter': taglist.values()[i]['counter'],
			'url': tag.get_absolute_url()
		})
		i+=1

	context["taglist"] = list(return_data)

	return HttpResponse(json.dumps(context), content_type="application/json")



class TagAllView(ListView, FormView):
	template_name = 'tags/tags_search.html'
	model = TagPoll
	form_class = TagSearchForm

	def dispatch(self, *args, **kwargs):
		dispatch = super(TagAllView, self).dispatch(*args, **kwargs)

		#redirect to user create checkbox on terms and conditions not checked but user has signed in
		if self.request.user.is_authenticated:
			try: 
				test = PUser.objects.get(user_id=self.request.user.id)
			except:
				return redirect('PUserCreate')

		return dispatch


	def get_context_data(self, **kwargs):
		context = super(TagAllView, self).get_context_data(**kwargs)
		# context ={}
		search = self.request.GET.get('search')

		#update the number of tags count to only count the number of active tags
		runtagcount()

		# exclude inactive polls
		exin = Ptype.objects.filter(active=True)
		taglist = TagPoll.objects.filter(active=True, polltype__in=exin).distinct()

		# ptype = Ptype.objects.filter(active=True)
		taglist = taglist.exclude(title="").order_by('title')

		if search:
			taglist = taglist.filter(title__icontains=search)

		context["taglist"] = taglist

		return context




class TagView(DetailView):
	model = TagPoll
	template_name = 'tags/tags_all.html'

	def dispatch(self, *args, **kwargs):
		dispatch = super(TagView, self).dispatch(*args, **kwargs)
		#redirect to user create checkbox on terms and conditions not checked but user has signed in
		if self.request.user.is_authenticated:
			try: 
				test = PUser.objects.get(user_id=self.request.user.id)
			except:
				return redirect('PUserCreate')

		return dispatch

	# def get_object(self, *args, **kwargs):
	# 	obj = super(TagView, self).get_object(*args, **kwargs)
	# 	return obj


	def get_context_data(self, **kwargs):
		context = super(TagView, self).get_context_data(**kwargs)

		tag = self.object
		context["tag"] = tag

		if self.request.user.is_authenticated:
			#see of the tag has been favorited by the user
			favtag = TagPoll.objects.filter(title=tag, tagfav=self.request.user).first()
			if favtag is None:
				context["fav"] = False
			else:
				context["fav"] = True
		else:
			context["fav"] = False


		tag_lst = TagPoll.objects.filter(title=tag)
		p_lst = tag_lst.values_list("polltype",flat=True)

		bydatelist = Ptype.objects.filter(active=True, id__in=p_lst).order_by('-date')

		context["tag"] = tag
		context["bydatelist"] = bydatelist

		return context



@csrf_exempt # ok to exempt no input
def api_fav(request):

	if request.POST:

		if request.user.is_authenticated:
			tag_id =  request.POST.get('tag_id')
			tagitem_obj = TagPoll.objects.get(id=tag_id)
			tag_fav = TagPoll.objects.filter(title=tagitem_obj, tagfav=request.user)

			if tag_fav:
				# remove favorite
				tag_fav.first().tagfav.remove(request.user)
				result = "unfavorited"
				# messages.info(request, "Unfavorited!")

			else:
				# add favorite
				fav = TagPoll.objects.get_or_create(title=tagitem_obj)[0]
				fav.save()
				fav.tagfav.add(request.user)
				result = "favorited"
				# messages.info(request, "Favorited!")

			return JsonResponse({"result": result})
		else:
			return JsonResponse({"result": "error", "msg": "login_requred"})
	else:
		return redirect('/')


