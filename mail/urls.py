from django.conf.urls import url, include
from rest_framework import routers
from mail.views import *

router = routers.DefaultRouter()
router.register(r'account', MailAccountViewSet, 'mailaccount')
router.register(r'alias',   MailAliasViewSet,   'mailalias')

urlpatterns = [
    url(r'^', include(router.urls)),
]
