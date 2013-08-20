from backend.models import *
from django.contrib import admin

class AutomatedMessageAdmin(admin.ModelAdmin):
	list_display = ('__unicode__','send_base','send_offset','message','note')
	list_filter = ('send_base','groups')
	search_fields = ('send_offset',)

admin.site.register(AutomatedMessage,AutomatedMessageAdmin)
admin.site.register(Email)
admin.site.register(AutoTask)
admin.site.register(MessageGroup)
admin.site.register(Condition)
admin.site.register(StudyGroup)
admin.site.register(MessageBase)
admin.site.register(LanguageGroup)

