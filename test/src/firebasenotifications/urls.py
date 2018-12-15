from django.conf.urls import url
from firebasenotifications.views import DeviceTokenCreateView, DeviceTokenListView, SendMessage
urlpatterns = [
    url(r'add', DeviceTokenCreateView.as_view(), name='add-fcm-device-token'),
    url(r'tokenlist/', DeviceTokenListView.as_view(), name= 'fcm-device-token-list'),
    url(r'send/', SendMessage, name='send-fcm-message')
]