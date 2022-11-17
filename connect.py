from pyrogram import Client
import json

def saveConfig(config):
  with open("config.json", "w") as jsonfile:
    json.dump(config, jsonfile) # Writing to the file
    jsonfile.close()


config = json.load(open('config.json'))
try:
  client = Client('telegram-spammer', config.get('api_id'), config.get('api_hash'), phone_number=config.get('api_phone'))
except:
  print('error')

with client:
  data = config
  
  data['is_connected'] = client.is_connected

  saveConfig(data)

