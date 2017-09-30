from django.contrib import admin
from .models import (Agent, Website, Adspace, Contract, Ad, Stat,
RequestForAdv)

admin.site.register(Agent)
admin.site.register(Website)
admin.site.register(Adspace)
admin.site.register(Ad)
admin.site.register(Stat)
admin.site.register(Contract)
admin.site.register(RequestForAdv)
