from patients.models import  *
from django.contrib import admin

class ClientAdmin(admin.ModelAdmin):
	list_display = ('study_group','id','signup_date','first_name','last_name','condition','pregnancy_status','validated','phone_number','phone_network')
	list_filter = ('study_group','condition')
	search_fields = ('id','first_name','last_name') 
	ordering = ('study_group','id')

admin.site.register(Nurse)
admin.site.register(Client,ClientAdmin)
admin.site.register(Message)
admin.site.register(Note)
admin.site.register(PhoneCall)
admin.site.register(Visit)
admin.site.register(PregnancyEvent)
