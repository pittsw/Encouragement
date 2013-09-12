from backend.models import *
from django.contrib import admin

class AutomatedMessageAdmin(admin.ModelAdmin):
	list_display = ('note','send_base','send_offset','list_groups','message')
	list_filter = ('send_base','groups')
	search_fields = ('note',)

admin.site.register(AutomatedMessage,AutomatedMessageAdmin)
admin.site.register(Email)
admin.site.register(MessageGroup)
admin.site.register(Condition)
admin.site.register(StudyGroup)
admin.site.register(MessageBase)
admin.site.register(LanguageGroup)

