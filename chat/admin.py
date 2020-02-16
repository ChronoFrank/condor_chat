from django.contrib import admin
from chat.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'avatar')


admin.site.register(UserProfile, UserProfileAdmin)