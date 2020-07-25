from django.contrib import admin
from petitions.models import Petition, Signature

admin.site.register(Petition)
admin.site.register(Signature)
