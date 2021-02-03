from django.contrib import admin
from API.models import User,Question,QuestionImage,Conversation,Message
# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(QuestionImage)
admin.site.register(Conversation)
admin.site.register(Message)