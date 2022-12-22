from django.contrib import admin

# Register your models here.
from ad.models import Ads, Categories

admin.site.register(Ads)
admin.site.register(Categories)