import json
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from API.models import User, Question, Conversation, Message
from API.serializers import UserModelSerializer, QuestionModelSerializer, UserBasicModelSerializer, \
    ConversationModelSerializer, MessageModelSerializer
from API.utils.auth import jwtQueryParamsBaseAuthentication
from API.utils.jwt_token import create_token


# Create your views here.
class UserAPIView(APIView):
    '''
    用户注册登录视图,通过code获取用户openid和session_key
    并通过openid确认用户是否注册,如果是,直接返回token
    如果不是,需要向用户请求发送用户主体信息,用于注册,再发送token
    '''

    APP_ID = 'wxae13e260929ad29e'
    APP_secret = '9b26e7c17c00a8c4e22d74ec4d928ac0'
    session_key = '',
    openID = ''

    def post(self,request):
        # 定义返回
        ret_data = {
            'status': 201,
            'msg':'ok'
        }
        # 如果没有获取到code,则返回错误信息
        if not 'code' in request.data or not 'userInfo' in request.data:
            ret_data['status'] = 204
            ret_data['msg'] = '信息获取缺失.'
            return Response(ret_data)
        code = request.data['code']
        user_info = request.data['userInfo']
        # 获取用户openID
        self.getOpenID(code)
        # 如果openID存在,则用户存在
        #如果openID不存在,则用户不存在,向用户请求注册,再分发token
        if User.objects.filter(openID=self.openID):
            # 1. 获取user实例
            user = User.objects.get(openID=self.openID)

            # 2. 需要判断用户信息是否更新，需要更新为用户最新数据
            if not user_info['nickName'] == user.nickName:
                user.nickName = user_info['nickName']
                user.save()
            if not user_info['avatarUrl'] == user.avatarUrl:
                user.avatarUrl = user_info['avatarUrl']
                user.save()
            # 3. 获取token
            ret_data['token'] = create_token({'id':user.id,'openID':user.openID})
            ret_data['user'] = UserBasicModelSerializer(instance=user).data
        else :
            ret_data['status'] = 203
            ret_data['msg'] = '未注册,请注册'
            ret_data['openID'] = self.openID
        return Response(ret_data)

    def getOpenID(self,code):
        url = ' https://api.weixin.qq.com/sns/jscode2session' \
              + '?appid=' + self.APP_ID \
              + '&secret=' + self.APP_secret \
              + '&js_code=' + code \
              + '&grant_type=authorization_code'
        response = json.loads(requests.get(url).content)
        self.session_key = response['session_key']
        self.openID = response['openid']


class UserRegisterAPIView(APIView):
    '''用户注册视图,仅提供post方法'''
    def post(self,request):
        # 定义返回
        ret_data = {
            'status': 201,
            'msg': 'ok'
        }
        if not 'userInfo' in request.data or not 'openID' in request.data:
            ret_data['status'] = 203
            ret_data['msg'] = '未获得注册信息,注册失败'
            return Response(ret_data)
        userInfo = request.data['userInfo']
        openID = request.data['openID']
        userInfo['openID'] = openID
        print(userInfo)
        # 反序列化
        serializer = UserModelSerializer(data=userInfo)
        # 数据有效化校验
        result = serializer.is_valid()
        print(result)
        if result:
            # 1. 注册到数据库
            user = serializer.save()
            # 2. 分发 token
            ret_data['user'] = UserBasicModelSerializer(instance=user).data
            ret_data['token'] = create_token({'id':user.id,'openID':user.openID})
            return Response(ret_data)
        else :
            ret_data['status'] = 204
            ret_data['msg'] = '注册失败,信息校验不合格'
            return Response(ret_data)

class QuestionModelAPIView(APIView):
    '''
    get:
    问题提供列表视图
    ### 现在只写从数据库获得的数据,之后从redis缓存中获得，公用的试图，不应该token验证
    '''

    def get(self,request):
        '''获取问题列表'''
        ret_data = {
            'status':201,
            'msg':'ok'
        }
        question_list = Question.objects.all()
        question_list_serializer = QuestionModelSerializer(instance=question_list,many=True)
        ret_data['question_list'] = question_list_serializer.data
        return Response(ret_data)


class QuestionCreateModelAPIView(APIView):
    """
    POST: 用于问题创建
    """
    authentication_classes = [jwtQueryParamsBaseAuthentication]

    def post(self, request):
        ret_data = {
            'status': 201,
            'msg': 'ok'
        }
        # 通过验证之后，可以获得用户的信息
        user_info = request.user
        if not 'question' in request.data:
            ret_data['status'] = 203
            ret_data['msg'] = '未获得问题!错误!'
            return Response(ret_data)
        question_data = request.data['question']
        serializer = QuestionModelSerializer(data=question_data)
        result = serializer.is_valid()
        if result:
            '''此处保存,因为存在外键,需要获取外键的对象,然后传递到反序列化的数据中,然后再保存'''
            uer = User.objects.get(id=user_info['id'],openID=user_info['openID'])
            serializer.validated_data['questioner'] = uer
            question_obj = serializer.save()
            print(question_obj)
        else:
            ret_data['status'] = 204
            ret_data['msg'] = '问题信息校验失败'
        return Response(ret_data)


class UserQAModelAPIView(APIView):
    """
    get:
    用于返回用户的需要获得的是回答还是问题
    参数   parameter
    值     myQuestion/myAnswer
    """

    authentication_classes = [jwtQueryParamsBaseAuthentication]
    value = ('myQuestion', 'myAnswer')

    def get(self,request):
        ret_data = {
            'status': 201,
            'msg': 'ok'
        }
        user = request.user
        if not 'parameter' in request.query_params:
            ret_data['status'] = 203
            ret_data['msg'] = '未传递参数'
            return Response(ret_data)
        parameter = request.query_params['parameter']
        if not parameter or not (parameter == self.value[0] or parameter == self.value[1]):
            ret_data['status'] = 203
            ret_data['msg'] = '参数传递有误'
            return Response(ret_data)
        if parameter == self.value[0]:
            # print("返回用户的问题")
            if Question.objects.exists():
                query_list = Question.objects.filter(questioner_id=user['id'])
            else:
                query_list = []
            if query_list is None:
                question_list  = []
            else:
                question_list_serializer = []
                for item in query_list:
                    item_serializer = QuestionModelSerializer(instance=item)
                    question_list_serializer.append(item_serializer.data)
                question_list = question_list_serializer
            ret_data['question_list'] = question_list
        elif parameter == self.value[1]:
            print('返回用户的回答，也就是会话')
            query_list = []
            if Conversation.objects.exists():
                query_list = Conversation.objects.filter(solvers=user['id'])
            else:
                query_list = []
            if query_list is None:
                answer_list = []
            else:
                answer_list_serializer = ConversationModelSerializer(instance=query_list,many=True)
                answer_list = answer_list_serializer.data
                ret_data['answer_list'] = answer_list
        return Response(ret_data)


class MessageForConversationModelAPIView(APIView):

    """回话的信息"""

    def get(self,request):
        ret_data = {
            'status':201,
            'msg':'ok'
        }
        if not 'conversation_id' in request.query_params:
            ret_data['status'] = 203
            ret_data['msg'] = '未获得会话id'
            return Response(ret_data)
        conversation_id = request.query_params['conversation_id']
        message_list = []
        if Conversation.objects.filter(id=conversation_id):
            conversation_obj = Conversation.objects.get(id=conversation_id)
            if Message.objects.exists():
                message_list = Message.objects.filter(conversation=conversation_obj)
                message_list_serializer = MessageModelSerializer(instance=message_list,many=True)
                message_list = message_list_serializer.data
        else:
            ret_data['status'] = 204
            ret_data['msg'] = '不存在的会话'
        ret_data['memssage_list'] = message_list

        return Response(ret_data)
