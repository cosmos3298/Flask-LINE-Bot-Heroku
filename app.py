import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# import google sheet library
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheet Testing groud 
scopes = ['https://spreadsheets.google.com/feeds']
json_creds = os.getenv("GOOGLE_CREDENTIALS")

creds_dict = json.loads(json_creds)
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
gc = gspread.authorize(creds)

sht =  gc.open_by_key('1kWXfTRtDYIIXa3Dr-0ack5-LHYKH5_7ahB8BCIhbWHw')
wst = sht.worksheet("表單回應 1")
# getgsvalue = workbook.get('A15')[0][0]
# Testing groud End


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}" + "." +" I'm a mockingjay. haha!\n ")
    line_bot_api.reply_message(event.reply_token, reply)
