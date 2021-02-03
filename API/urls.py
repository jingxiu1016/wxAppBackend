"""******************************** 开始
    author:惊修
    time:$
   ******************************* 结束"""

from django.urls import path
from API.views import UserAPIView
from API.views import UserRegisterAPIView
from API.views import QuestionModelAPIView
from API.views import QuestionCreateModelAPIView
from API.views import UserQAModelAPIView
from API.views import MessageForConversationModelAPIView
app_name = 'API'

urlpatterns = [
    path('login', UserAPIView.as_view(), name='login'),
    path('register',UserRegisterAPIView.as_view(),name='register'),
    path('questionList',QuestionModelAPIView.as_view(),name='questionList'),
    path('questionCreate',QuestionCreateModelAPIView.as_view(),name='questionCreate'),
    path('getQA',UserQAModelAPIView.as_view(),name='getAQ'),
    path('message',MessageForConversationModelAPIView.as_view(),name='message')

]
