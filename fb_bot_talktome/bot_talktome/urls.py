from django.conf.urls import include, url
from .views import BotTalkToMeView


urlpatterns = [url(r'^fb8fff701ecdbd726ebcd303cad88a058c83ac3f631eb00055/?$', BotTalkToMeView.as_view())]
