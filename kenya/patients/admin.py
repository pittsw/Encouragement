from patients.models import AutomatedMessage, Condition, Nurse, Location, Note, Client, Message, Interaction, PhoneCall
from django.contrib import admin

admin.site.register(Nurse)
admin.site.register(Location)
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(AutomatedMessage)
admin.site.register(Condition)
admin.site.register(Note)
admin.site.register(PhoneCall)