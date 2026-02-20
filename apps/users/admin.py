from django.contrib import admin
from apps.users.models import User, Conversation, Message

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ["isActive"]

admin.site.register(Conversation)
admin.site.register(Message)
