from patients.models import AutomatedMessage, Condition, Nurse, Location, Client, Message
from django.contrib import admin

admin.site.register(Nurse)
admin.site.register(Location)
admin.site.register(Client)
admin.site.register(Message)
admin.site.register(AutomatedMessage)
admin.site.register(Condition)
