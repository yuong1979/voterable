from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from django.core.urlresolvers import reverse_lazy
from users.models import PUser
from django.db.models import Q
from users.forms import PUserAddForm, PUserEditForm
# from variables.models import FunctionType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from mixins.mixins import UserChangeManagerMixin
import datetime
from polls.models import Ptype, PollItem
from django.contrib.auth.models import User
from analytics.models import ViewPollTypeUnique, ViewPollItemsUnique, Ranking
from django.db.models import Sum

class PUserDetail(DetailView):
    model = PUser
    success_url = '/puser/'
    template_name = 'PUser/user_details.html'


    def get_context_data(self, *args, **kwargs):

        context = super(PUserDetail, self).get_context_data(*args, **kwargs)

        user = self.object.user
        user = User.objects.get(id = user.id)

        context["user"] = self.object

        context["pollsCreated"] = Ptype.objects.filter(c_user=user).count()
        context["pollsECreated"] = PollItem.objects.filter(user_submit=user).count()


        user = PUser.objects.get(user=user)

        context["points"] = user.score
        context["rank"] = user.rank



        # context["votes_poll_entries"] =  PollItem.objects.filter(user_submit=user).aggregate(Sum('score')).get('score__sum')

        # pvote = PollItem.objects.filter(user_submit=user).aggregate(Sum('score')).get('score__sum')

        # if pvote is None:
        #     context["votes_poll_entries"] = 0
        # else:
        #     context["votes_poll_entries"] = pvote

        # # get user created pitems
        # created_items = PollItem.objects.filter(user_submit=user)
        # # get list of views that belong to the pytypes created by user
        # pitem_list = ViewPollItemsUnique.objects.filter(p_item__in=created_items)
        # # get user created polls
        # context["votes_poll_entries_views"] = pitem_list.values_list('userview',flat=True).distinct().count()
        # context["points"] = context["votes_poll_entries_views"] + context["votes_poll_entries"]

        # pt = context["points"]

        # if pt < 0:
        #     pt = 0

        # #vlookup ranking table
        # rk = Ranking.objects.get(low_score__lte=pt, high_score__gte=pt)

        # context["rank"] = rk

        # # saving the data inside user profile
        # user = PUser.objects.get(user=user)
        # user.rank = str(rk)
        # user.score = pt
        # user.save()


        return context






class PUserCreate(CreateView):
    model = PUser
    form_class = PUserAddForm
    # fields = ['name']
    # success_url = '/company/'
    template_name = 'PUser/create.html'
    # function = FunctionType.objects.filter(title="Employer").first()



    def form_valid(self, form):

        i = form.save(commit=False)
        i.user = self.request.user
        # i.function = self.function
        i.save()

        valid_data = super(PUserCreate, self).form_valid(form)
        
        #Create a Puser        
        user = PUser.objects.get_or_create(user=self.request.user)[0]


        # on the puser account - they are not banned as default
        # on the create, update poll, create, update poll entry, if puser = banned, exit and tell user he is banned

        #add one day of free trial for complete content?
        user.freedays = user.freedays + 1
        user.save()
        messages.success(self.request, "You have been given 1 days of premium package free trial, activate anytime.")

        return valid_data

    def get_success_url(self):
        user = self.request.user
        obj = get_object_or_404(PUser, user=user)
        pk = obj.pk
        # url = reverse('PUserDetail', kwargs={'pk': pk})
        messages.info(self.request, "Your profile has been created.")
        return reverse('Home')




class PUserUpdate(UserChangeManagerMixin,UpdateView): #if user is request user or staff can change
    model = PUser
    form_class = PUserEditForm
    # fields = ['name']
    # success_url = '/company/'
    template_name = 'PUser/update.html'


    def dispatch(self, *args, **kwargs):
        dispatch = super(PUserUpdate, self).dispatch(*args, **kwargs)

        #exit if user did not create poll and is not a staff
        if not (self.object.user == self.request.user) and not (self.request.user.is_staff):
            return redirect('Home')

        return dispatch


    def get_success_url(self):
        user = self.request.user
        obj = get_object_or_404(PUser, user=user)
        pk = obj.pk
        # url = reverse('PUserDetail', kwargs={'pk': pk})
        messages.info(self.request, "Your profile has been updated.")
        return reverse('Home')



# class PUserList(ListView):
#     model = PUser
#     template_name = 'PUser/list.html'

#     def get_queryset(self, *args, **kwargs):
#         qs = super(PUserList, self).get_queryset(**kwargs).filter()
#         query = self.request.GET.get("q")
#         if query:
#             qs = qs.filter(
#                 Q(name__icontains=query)|
#                 Q(description__icontains=query)
#                 ).order_by("-name")
#             return qs
#         else:
#             return qs




class PUserSecretList(ListView):
    model = PUser
    template_name = 'PUser/list.html'

    def get_queryset(self, *args, **kwargs):
        qs = super(PUserSecretList, self).get_queryset(**kwargs).filter()

        qs = qs.filter(trial=True)

        return qs




