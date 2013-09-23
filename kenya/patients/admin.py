from patients.models import  *
from django.contrib import admin

class PregnancyEventInline(admin.StackedInline):
	model = PregnancyEvent

class ClientAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name','study_group','id','signup_date','condition','last_msg_client','last_msg_system',
	'pregnancy_status','validated','phone_number','phone_network')
	list_filter = ('study_group','condition')
	search_fields = ('id','first_name','last_name') 
	ordering = ('study_group','id')
	readonly_fields=('urgent','pending','last_msg_client','last_msg_system','signup_date','validated')
	inlines = [PregnancyEventInline]
	
class PregnancyEventAdmin(admin.ModelAdmin):
	list_display = ('date','outcome','location','client')

admin.site.register(Nurse)
admin.site.register(Client,ClientAdmin)
admin.site.register(Message)
admin.site.register(Note)
admin.site.register(PhoneCall)
admin.site.register(Visit)
admin.site.register(PregnancyEvent,PregnancyEventAdmin)
