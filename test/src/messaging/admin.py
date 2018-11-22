from django.contrib import admin

# Register your models here.
from messaging.models import Message

class MessageAdmin(admin.ModelAdmin):
	list_display = ('senduser', 'pollitem', 'content', 'likes', 'timestamp', 'active')
	inlines = [
	]
	class Meta:
		model = Message


admin.site.register(Message, MessageAdmin)