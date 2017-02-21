from django.shortcuts import render
import json,random,re
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here
# yomamabot/fb_yomamabot/views.py
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.


def post_facebook_message(fbid, recevied_message):
    jokes = {
         'love': ["""I love you too"""],
         'day':    ["""It was nice , how was yours""",
                    """ Sorry man totally worthless to ask """],
         'stupid':   ["""I know I haven't used AI yet""",
                    """Look who is telling me that"""] 
         }
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    #tokens=recevied_message
    ans_text = ''
    for token in tokens:
        if token in jokes:
            ans_text = random.choice(jokes[token])
            break
    if not ans_text:
        ans_text = "I didn't understand! Please make use of words like 'love','day','stupid' in your messages for eg. 'I love you', 'how was your day?', 'you are stupid' for a proper answer"            
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=your token' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":ans_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print(status.json())

class trybotview(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '29031996':
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
                    # Print the message to the terminal
                    print(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])    
        return HttpResponse()



 

