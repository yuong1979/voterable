from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework import generics
from .models import DeviceToken
from .serializer import DeviceTokenSerializer
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import requests


class DeviceTokenCreateView(generics.CreateAPIView):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer

    def post(self, request, *args, **kwargs):
        data = dict(request.data.dict())
        if int(data['user_id']) != self.request.user.id:
            return JsonResponse({'message':'not allowed'},status=500)
        serializer = DeviceTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if self.add_to_topic(data['device_token']) != 200:
            return JsonResponse({'message':'Subscription to topic failed'}, status=500)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def add_to_topic(self, token):
        headers = {
            'Authorization': 'key={}'.format(settings.SERVER_KEY),
            'Content-Type': 'application/json'
        }
        send_url = f' https://iid.googleapis.com/iid/v1/{token}/rel/topics/{settings.TOPIC_NAME}'
        r = requests.post(send_url, headers=headers)
        return r.status_code


class DeviceTokenListView(generics.ListAPIView):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer


@csrf_exempt
def SendMessage(request):
    headers = {
        'Authorization': 'key={}'.format(settings.SERVER_KEY),
        'Content-Type': 'application/json'
    }

    data = {
        "to": f"/topics/{settings.TOPIC_NAME}",
        "priority": "high",
        "notification": {
            "body": settings.MESSAGE_BODY,
            "title": settings.MESSAGE_TITLE,
            "click_action": settings.CLICK_ACTION
        },
    }

    if request.method == 'POST':
        data = requests.POST['data']
    r = requests.post('https://fcm.googleapis.com/fcm/send',data=json.dumps(data), headers=headers)
    return JsonResponse({'message_sent':data,'fcm_response':r.text,'status_code':r.status_code})