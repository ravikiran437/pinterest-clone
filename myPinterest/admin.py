from django.contrib import admin
from myPinterest.models import Pin,SavedPin,Likes,Comments
# Register your models here.

admin.site.register(Pin)
admin.site.register(SavedPin)
admin.site.register(Likes)
admin.site.register(Comments)