from patients.models import  *
from django.contrib import admin

class PregnancyEventInline(admin.StackedInline):
	model = PregnancyEvent
	
class VisitsInline(admin.TabularInline):
	model = Visit
	
class MessageInline(admin.TabularInline):
	model = Message

class ClientAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name','study_group','id','anc_num','next_visit','condition','last_msg_client','last_msg_system',
	'repeat_msg','pregnancy_status','validated','phone_number','send_time','send_day')
	list_filter = ('study_group','condition','send_time','send_day')
	search_fields = ('id','first_name','last_name') 
	ordering = ('study_group','id')
	readonly_fields=('urgent','pending','last_msg_client','last_msg_system','signup_date','validated','repeat_msg')
	inlines = [PregnancyEventInline,VisitsInline,MessageInline]
	
class PregnancyEventAdmin(admin.ModelAdmin):
	list_display = ('date','outcome','location','client')
	
class MessageAdmin(admin.ModelAdmin):
	list_display = ('date','client_id','content','sent_by')
	list_filter = ('sent_by',)
	
class PhoneCallAdmin(admin.ModelAdmin):
	list_display = ('date','client_id','content','duration','reason')
	
class VisitAdmin(admin.ModelAdmin):
	list_display = ('client_id','date','scheduled_date','comments')
	
class NoteAdmin(admin.ModelAdmin):
	list_display = ('date','client_id','content')

admin.site.register(Nurse)
admin.site.register(Client,ClientAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Note,NoteAdmin)
admin.site.register(PhoneCall,PhoneCallAdmin)
admin.site.register(Visit,VisitAdmin)
admin.site.register(PregnancyEvent,PregnancyEventAdmin)
