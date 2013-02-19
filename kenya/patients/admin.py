from patients.models import Condition, Nurse, Note, Client, Message, PhoneCall, Visit, PregnaceyEvent
from django.contrib import admin

admin.site.register(Nurse)
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(Condition)
admin.site.register(Note)
admin.site.register(PhoneCall)
admin.site.register(Visit)
admin.site.register(PregnaceyEvent)
