from django.contrib import admin
from chat.models import UserProfile, Message, Room


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'avatar')
    raw_id_fields = ('user', )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'timestamp', 'content')
    raw_id_fields = ('sender',)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'timestamp', 'is_goup')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Room, RoomAdmin)
