from patients.models import  *
from django.contrib import admin

class PregnancyEventInline(admin.StackedInline):
	model = PregnancyEvent

class ClientAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name','study_group','id','next_visit','condition','last_msg_client','last_msg_system',
	'pregnancy_status','validated','phone_number','phone_network')
	list_filter = ('study_group','condition')
	search_fields = ('id','first_name','last_name') 
	ordering = ('study_group','id')
	readonly_fields=('urgent','pending','last_msg_client','last_msg_system','signup_date','validated')
	inlines = [PregnancyEventInline]
	
class PregnancyEventAdmin(admin.ModelAdmin):
	list_display = ('date','outcome','location','client')
	
class MessageAdmin(admin.ModelAdmin):
	list_display = ('date','client_id','content','sent_by')
	list_filter = ('sent_by',)
	
class PhoneCallAdmin(admin.ModelAdmin):
	list_display = ('date','client_id','content','duration','reason')
	
class VisitAdmin(admin.ModelAdmin):
	list_display = ('date','client_id','comments')
	
class NoteAdmin(admin.ModelAdmin):
	list_display = ('date','client_id','content')

admin.site.register(Nurse)
admin.site.register(Client,ClientAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Note,NoteAdmin)
admin.site.register(PhoneCall,PhoneCallAdmin)
admin.site.register(Visit,VisitAdmin)
admin.site.register(PregnancyEvent,PregnancyEventAdmin)
