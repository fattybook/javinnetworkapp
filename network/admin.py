from django.contrib import admin
from .models import User, Follow, Post
# Register your models here.

class FollowAdmin(admin.ModelAdmin):
    filter_horizontal = ("followers","following",)

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("liked_post",)
admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)    