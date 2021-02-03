from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.timezone import now
# Create your models here.

gender = (('1','男'),('2','女'))
mark = (('text','文本'),('image','图片'))

class User(models.Model):
    '''微信用户模型'''
    openID = models.CharField(max_length=50,blank=False,unique=True,verbose_name='用户标识符')
    nickName = models.CharField(max_length=30,blank=False,verbose_name='昵称')
    gender = models.CharField(max_length=5,blank=False,choices=gender,default=gender[0],verbose_name='性别')
    city = models.CharField(max_length=20,blank=True,verbose_name='城市')
    province = models.CharField(max_length=20,blank=True,verbose_name='省份')
    country = models.CharField(max_length=20,blank=True,verbose_name='国家')
    avatarUrl = models.URLField(blank=True,verbose_name='头像地址')
    created_time = models.DateTimeField(blank=False,default=now,verbose_name='注册时间')


    class Meta:
        db_table = 'User'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ('-created_time',)

    def __str__(self):
        return self.nickName


# class Label(models.Model):
#     """问题的标签模型"""
#     pass



class Question(models.Model):
    '''问题模型'''
    questioner = models.ForeignKey(User,blank=False,on_delete=models.CASCADE,verbose_name='提问者')
    title = models.CharField(max_length=100,blank=False,verbose_name='标题')
    describe = models.TextField(blank=False,verbose_name='描述')
    created_time = models.DateTimeField(default=now,blank=False,verbose_name='发表时间')

    class Meta:
        db_table = 'Question'
        verbose_name = '问题'
        verbose_name_plural = '问题'
        ordering = ('-created_time',)

    def __str__(self):
        return self.title


class QuestionImage(models.Model):
    '''图片模型'''
    question = models.ForeignKey(Question,blank=False,on_delete=models.CASCADE,verbose_name='关联问题')
    image = models.ImageField(upload_to='question/%Y/%m/%d',verbose_name='图片')

    class Meta:
        db_table = 'QuestionImage'
        verbose_name = '问题图片'
        verbose_name_plural = '问题图片'

    def __str__(self):
        return str(self.image)


class Conversation(models.Model):
    """会话模型"""
    question = models.ForeignKey(Question,blank=False,on_delete=models.CASCADE,verbose_name='关联问题')
    solvers = models.ForeignKey(User,blank=False,on_delete=models.CASCADE,verbose_name='答疑者')
    isResolve = models.BooleanField(default=False,blank=False,verbose_name='是否解决')
    created_time = models.DateTimeField(default=now,verbose_name='创建时间')

    class Meta:
        db_table = 'Conversation'
        verbose_name = '会话'
        verbose_name_plural = '会话'
        ordering = ('-created_time',)

    def __str__(self):
        return self.solvers.nickName + '&' + self.question.questioner.nickName


class Message(models.Model):
    """用于会话的消息模型"""
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE,verbose_name='关联会话')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='发送者')
    message = models.TextField(blank=False,verbose_name='消息')
    mark = models.CharField(max_length=20,choices=mark,default=mark[0],blank=False,verbose_name='消息类型')
    created_time = models.DateTimeField(default=now,verbose_name='创建时间')

    class Meta:
        db_table = 'Message'
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ('-created_time',)

    def __str__(self):
        return self.mark+":"+ self.message