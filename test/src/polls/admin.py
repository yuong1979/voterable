from django.contrib import admin
from django import forms
from polls.models import PollItem, PollFav, Ptype, SuggestedPoll, PollVoting


class PollModelForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ('title', 'user_submit', 'description', 'score')
        model = PollItem


class PtypeAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'location', 'topic', 'subtopic', 'active', 'freepoll', 'c_user', 'date', 'vote_count','locked')
    search_fields = ['title']
    list_filter = ('location', 'topic')

    def __str__(self,obj):
        return obj.__str__()

class PollAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'allowed', 'published', 'user_submit', 'score', 'date', 'modifieddate')
    search_fields = ['title']
    forms = PollModelForm


class PollVotingAdmin(admin.ModelAdmin):
    list_display = ('id','vote_user','poll','vote')
    list_filter = ['vote_user']



class PollFavAdmin(admin.ModelAdmin):
    list_display = ('id','fav_user')


class SuggestedPollAdmin(admin.ModelAdmin):
    list_display = ('id', 'typePoll', 'title', 'user_submit', 'allowed', 'date', 'score')
    list_filter = ('typePoll', 'allowed')


# class SuggestVoteAdmin(admin.ModelAdmin):
#     list_display = ('id','spoll','updated','date')
    # list_display = ('id','vote_user','spoll','updated','date')


admin.site.register(Ptype, PtypeAdmin)
admin.site.register(PollItem, PollAdmin)
admin.site.register(PollVoting, PollVotingAdmin)
admin.site.register(PollFav, PollFavAdmin)

admin.site.register(SuggestedPoll, SuggestedPollAdmin)
# admin.site.register(SuggestVote, SuggestVoteAdmin)


