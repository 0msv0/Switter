from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from . import models


class UserAdminCustom(UserAdmin):
    model = User
    field = ["username"]


admin.site.register(models.Reply)
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Relationship)
admin.site.register(models.Comment)
admin.site.register(models.Like)


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdminCustom)
