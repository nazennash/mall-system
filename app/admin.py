from django.contrib import admin
from .models import Category, Product, Order, Cart, UserProfile, Feedback, Advertisement, ForumPost, ForumComment, ForumTopic, MessageForum
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(UserProfile)
admin.site.register(Feedback)
admin.site.register(Advertisement)
admin.site.register(ForumPost)
admin.site.register(ForumComment)
admin.site.register(ForumTopic)
admin.site.register(MessageForum)