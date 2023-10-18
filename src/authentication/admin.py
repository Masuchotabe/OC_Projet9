from django.contrib import admin

from authentication.models import User
from reviews.models import Review, Ticket, UserFollows, UserBlocked

# Register your models here.

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Ticket)
admin.site.register(UserFollows)
admin.site.register(UserBlocked)
