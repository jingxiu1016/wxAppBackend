from django.conf.urls import url
from API.consumers import ChatConsumers,AsyncChatConsumers

urlpatterns = [
    url(r'^chat/',AsyncChatConsumers.as_asgi())
]