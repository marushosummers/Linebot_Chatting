# -*- Coding: utf-8 -*-

import os
import urllib.request
import json

def lambda_handler(request, context):

    for event in request['events']:

        # endpoint
        url = 'https://api.line.me/v2/bot/message/reply'

        # request header
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ['CHANNEL_ACCESS_TOKEN']
        }

        # text or sticker
        message_type = event['message']['type']

        text = ""
        stickerId = ""
        packageId = ""

        if message_type == "text":
            text = docomo_chatting(event)

        elif message_type == "sticker":
            stickerId = event['message']['stickerId']
            packageId = event['message']['packageId']

        # request body
        body = {
            'replyToken': event['replyToken'],
            'messages': [
                {
                    "type": message_type,
                    "text": text,
                    "stickerId": stickerId,
                    "packageId": packageId
                }
            ]
        }

        # post
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
        with urllib.request.urlopen(req) as res:
            response_body = res.read().decode("utf-8")


    return {'statusCode': 200, 'body': '{}'}

def docomo_chatting(event):

    # endpoint
    endpoint = 'https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY=REGISTER_KEY'
    url = endpoint.replace('REGISTER_KEY', os.environ['DOCOMO_API_KEY'])

    # request json
    text = event['message']['text']
    headers = {"Content-Type":"application/json"}
    body ={
        "language":"ja-JP",
        "botId":"Chatting",
        "appId":os.environ['DOCOMO_APP_ID'],
        "voiceText": text,
        "clientData":{
        "option":{
            "mode":"dialog",
            "t":"kansai"
        }
        },
        "appRecvTime":"2018-09-01 00:00:00",
        "appSendTime":"2018-09-01 00:00:00"
        }

    # post
    r = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
    with urllib.request.urlopen(r) as r:
        response_body_str = r.read().decode("utf-8")
        response_body = json.loads(response_body_str)
    response = response_body['systemText']['expression']

    return response
