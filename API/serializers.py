"""******************************** 开始
    author:惊修
    time:$
   ******************************* 结束"""
import json

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from API.models import User, Question, QuestionImage, Conversation, Message


class UserModelSerializer(ModelSerializer):
    """用户全信息序列化器"""
    class Meta:
        model = User
        fields = ['id','openID','nickName','city','province','country',
                  'avatarUrl','gender','created_time']


class UserBasicModelSerializer(ModelSerializer):
    """ 用户基本信息序列化器,用于信息的传递 """
    class Meta:
        model = User
        fields = ['id', 'nickName','avatarUrl']


class QuestionImageModelSerializer(ModelSerializer):
    class Meta:
        model = QuestionImage
        fields = ['question_id','image']


class QuestionModelSerializer(ModelSerializer):

    question_image = serializers.SerializerMethodField()
    questioner = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id','title','describe','question_image','questioner','created_time']

    def get_question_image(self,obj):
        instance = QuestionImage.objects.filter(question_id=obj.id)
        return QuestionImageModelSerializer(instance=instance,many=True).data

    def get_questioner(self,obj):
        questioner = User.objects.get(id=obj.questioner_id)
        return UserBasicModelSerializer(questioner).data


class MessageModelSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ConversationModelSerializer(ModelSerializer):

    class Meta:
        model = Conversation
        fields = ['question','solvers','isResolve','created_time']

    def get_message(self,obj):
        message_list = Message.objects.filter(conversation=obj)
        return MessageModelSerializer(instance=message_list,many=True).data