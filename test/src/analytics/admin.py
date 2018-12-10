from django.contrib import admin
from analytics.models import ViewPollItemsUnique, ViewPollTypeUnique, Ranking, ScorePollItemsByMonth, ScoreUserByMonth, PostReport



class ViewPollItemsUniqueAdmin(admin.ModelAdmin):
    list_display = ('p_item', 'vcount', 'updated', 'timestamp')

    def __str__(self,obj):
        return obj.__str__()

class ViewPollTypeUniqueAdmin(admin.ModelAdmin):
    list_display = ('p_type', 'id', 'vcount', 'ecount', 'updated', 'timestamp')

    def __str__(self,obj):
        return obj.__str__()
        
class RankingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'low_score', 'high_score', 'add_days')


class ScorePollItemsByMonthAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'year', 'month', 'posi', 'nega', 'score', 'updated')

class ScoreUserByMonthAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'year', 'month', 'score', 'updated')

class PostReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'Puser', 'usercon', 'postissue','postissuemsg', 'timestamp')

admin.site.register(ViewPollItemsUnique, ViewPollItemsUniqueAdmin)
admin.site.register(ViewPollTypeUnique, ViewPollTypeUniqueAdmin)
admin.site.register(Ranking, RankingAdmin)
admin.site.register(ScorePollItemsByMonth, ScorePollItemsByMonthAdmin)
admin.site.register(ScoreUserByMonth, ScoreUserByMonthAdmin)
admin.site.register(PostReport, PostReportAdmin)

