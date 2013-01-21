from patients.models import AutomatedMessage, Condition, Nurse, Note, Client, Message, PhoneCall, Visit
from django.contrib import admin

admin.site.register(Nurse)
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(AutomatedMessage)
admin.site.register(Condition)
admin.site.register(Note)
admin.site.register(PhoneCall)
admin.site.register(Visit)
