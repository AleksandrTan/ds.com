from django.contrib import admin
from django.contrib.auth.models import Permission, ContentType
from dsstore.models import Brends


admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(Brends)

# Register your models here.
