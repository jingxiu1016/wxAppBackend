from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from rest_framework.exceptions import AuthenticationFailed
from API.models import User
from API.serializers import UserBasicModelSerializer
from API.utils.auth import authenticate_by_token


class ChatConsumers(WebsocketConsumer):
    """非异步版本"""

    def websocket_connect(self, message):
        self.accept()

    def websocket_disconnect(self, message):
        pass

    def websocket_receive(self, message):
        print(message)
        ret_data = {
            'status':201,
            'status_msg':'ok'
        }
        get_content = json.loads(message['text'])

        if not 'token' in get_content:
            ret_data['status_msg'] = '未获得token用于验证'
            ret_data['status'] = 203
            self.send(text_data=json.dumps(ret_data))
        else:
            get_token = get_content['token']
            """捕获异常"""
            try:
                result = authenticate_by_token(token=get_token)
            except AuthenticationFailed as e:
                exc_data = e.args[0]
                if exc_data['status'] == 1003:
                    ret_data['status'] = 202
                    ret_data['status_msg'] = 'token失效，请重新进入小程序'
                    self.send(text_data=json.dumps(ret_data))
                elif exc_data['status'] == 1004:
                    ret_data['status'] = 202
                    ret_data['status_msg'] = 'token无效，请重新进入小程序'
                    self.send(text_data=json.dumps(ret_data))
                elif exc_data['status'] == 1005:
                    ret_data['status'] = 202
                    ret_data['status_msg'] = 'token非法，请重新进入小程序'
                    self.send(text_data=json.dumps(ret_data))
            else:
                user_data = result[0]
                user = User.objects.get(id=user_data['id'],openID=user_data['openID'])
                user_serializer = UserBasicModelSerializer(instance=user)
                ret_data['message'] = get_content['message']
                ret_data['sender'] = user_serializer.data
                self.send(text_data=json.dumps(ret_data))


class AsyncChatConsumers(AsyncWebsocketConsumer):
    """异步版本"""

    async def websocket_connect(self, message):
        await self.accept()

    async def websocket_disconnect(self, code):
        pass

    async def websocket_receive(self, message):
        await self.sendMessage(message)

    async def sendMessage(self,message):
        ret_data = {
            'status': 201,
            'status_msg': 'ok'
        }
        get_content = json.loads(message['text'])

        if not 'token' in get_content:
            ret_data['status_msg'] = '未获得token用于验证'
            ret_data['status'] = 203
            await self.send(text_data=json.dumps(ret_data))
        else:
            get_token = get_content['token']
            """捕获异常"""
            try:
                result = authenticate_by_token(token=get_token)
            except AuthenticationFailed as e:
                exc_data = e.args[0]
                if exc_data['status'] == 1003:
                    ret_data['status'] = 202
                    ret_data['status_msg'] = 'token失效，请重新进入小程序'
                    await self.send(text_data=json.dumps(ret_data))
                elif exc_data['status'] == 1004:
                    ret_data['status'] = 202
                    ret_data['status_msg'] = 'token无效，请重新进入小程序'
                    await self.send(text_data=json.dumps(ret_data))
                elif exc_data['status'] == 1005:
                    ret_data['status'] = 202
                    ret_data['status_msg'] = 'token非法，请重新进入小程序'
                    await self.send(text_data=json.dumps(ret_data))
            else:
                user_data = result[0]
                user = User.objects.get(id=user_data['id'], openID=user_data['openID'])
                user_serializer = UserBasicModelSerializer(instance=user)
                ret_data['message'] = get_content['message']
                ret_data['sender'] = user_serializer.data
                await self.send(text_data=json.dumps(ret_data))