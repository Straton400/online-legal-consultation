from django.contrib import admin
from .models import Lawyer, Client, Consultation, LawyerProfile

admin.site.register(Lawyer)
admin.site.register(Client)
admin.site.register(Consultation)
admin.site.register(LawyerProfile)