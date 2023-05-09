from twilio.rest import Client
import os
from dotenv import load_dotenv
import json
import requests
load_dotenv()

def lambda_handler(event, context):
    print(event)
    message = json.loads(event['Records'][0]['Sns']['Message'])
    notification_composer(message)

def notification_composer(message):
    print(message)
    account = os.environ['account']
    threshold = os.environ['threshold']
    from_number = os.environ['from_number']
    destination_number = os.environ['destination_number']
    discord = os.environ['discord']
    whatsapp = os.environ['whatsapp']
    discord_webhook_url = os.environ['discord_webhook_url']
    
    if discord == "true":
        url = discord_webhook_url
        if(message["source"] == "aws.ec2"):
            state = message["detail"]["state"]
            instanceId = message["detail"]["instance-id"]
            region = message["region"]
            embed = {
            "description": f"Instância **{instanceId}** está **${state}** na região **${region}**. \n \n👀 Verifique sua conta agora mesmo: **https://us-east-1.console.aws.amazon.com/cost-management/home?region=us-east-1#/dashboard**",
            "title": "🚨Atenção!🚨"
            }
        else:
            embed = {
            "description": f"O seu gasto com a conta **{account}** da AWS passou de: **${threshold}** (dólares) 💰\n \n👀 Verifique sua conta agora mesmo: **https://us-east-1.console.aws.amazon.com/cost-management/home?region=us-east-1#/dashboard**",
            "title": "🚨Atenção!🚨"
            }
        data = {
            "username": "AWS Notificator",
            "embeds": [
                embed
                ],
        }
        headers = {
            "Content-Type": "application/json"
        }

        send_discord_message(url, embed, data, headers)
    else:
        print("Discord não habilitado!")
    if whatsapp == "true":
        if(message["source"] == "aws.ec2"):
            state = message["detail"]["state"]
            instanceId = message["detail"]["instance-id"]
            region = message["region"]
            message_body = f"🚨*Atenção!*🚨 \n Instância **{instanceId}** está **${state}** na região **${region}**. \n \n👀 Verifique sua conta agora mesmo: *https://us-east-1.console.aws.amazon.com/cost-management/home?region=us-east-1#/dashboard*"
        else:
            message_body = f"🚨*Atenção!*🚨 \n O seu gasto com a conta *{account}* da AWS passou de: *${threshold}* (dólares) 💰 \n \n👀 Verifique sua conta agora mesmo: *https://us-east-1.console.aws.amazon.com/cost-management/home?region=us-east-1#/dashboard*"
        send_whatsapp_message(message_body, from_number, destination_number)
    else:
        print("WhatsApp não habilitado!")

def send_whatsapp_message(message_body, from_number, destination_number):
    #Credenciais e parametros Twilio
    account_sid = os.environ.get("ACCOUNT_SID")
    auth_token = os.environ.get("AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    message = client.messages.create( 
                                  from_=from_number,
                                  body=message_body,
                                  to=destination_number
                              )
    print(f"Mensagem enviada para {destination_number} com sucesso! ID Twilio: " + message.sid)

def send_discord_message(url, embed, data, headers):
    result = requests.post(url, json=data, headers=headers)
    if 200 <= result.status_code < 300:
        print(f"Webhook enviado: {result.status_code}")
    else:
        print(f"Webhook não enviado: {result.status_code}, response:\n{result.json()}")