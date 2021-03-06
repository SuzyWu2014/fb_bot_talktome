import json, requests
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
PAGE_ACCESS_TOKEN = ""

VERIFY_TOKEN = ''


def post_facebook_message(fbid, recevied_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {'fields': 'first_name', 'access_token': PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    response_text = 'Ahah~~\nHello ' + user_details['first_name'] + '!\nDid you just send: ' + recevied_message
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": response_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


class BotTalkToMeView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    # The get method is the same as before.. omitted here for brevity
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
