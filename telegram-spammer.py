from pyrogram import Client # телеграм клиент
import shelve # запись информации в файл
import json
import asyncio
from pyrogram.types import InputPhoneContact
import inspect
import time
import threading
import os
import subprocess

from window import *

def saveConfig(config):
  with open("config.json", "w") as jsonfile:
    json.dump(config, jsonfile) # Writing to the file
    jsonfile.close()


class Sender():
  def __init__(self):

    self.config = json.load(open('config.json'))

    self.processed_messages = shelve.open('processed_messages.db', writeback=True)
    
    self.loop = asyncio.get_event_loop()

    self.app = QApplication(sys.argv)
    self.window = MainWindow(
      self.connectSender,
      self.disconnectSender,
      self.updateAccount,
      self.start,
      self.clearProcessedMessages
    )

    try:
      self.client = Client('telegram-spammer', self.config.get('api_id'), self.config.get('api_hash'), phone_number=self.config.get('api_phone'))
    except:
      self.window.log('Ошибка подключения к telegram')


    sys.exit(self.app.exec_())


  def connectSender(self):     
    os.system('start python connect.py')

    try:
      self.client = Client('telegram-spammer', self.config.get('api_id'), self.config.get('api_hash'), phone_number=self.config.get('api_phone'))
    except:
      self.window.log('Ошибка подключения к telegram')

  def disconnectSender(self):
    try:
      path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'telegram-spammer.session')
      os.remove(path)

      data = self.config

      data['is_connected'] = False

      saveConfig(data)
    except:
      print('error')

  def start(self):
    thread = threading.Thread(target=self.loop.run_until_complete, args=(self._start(), ))
    thread.start()

  async def _start(self):
    try:
      self.client = Client('telegram-spammer', self.config.get('api_id'), self.config.get('api_hash'), phone_number=self.config.get('api_phone'))
    except:
      self.window.log('Ошибка подключения к telegram')

    # try:
    self.config = json.load(open('config.json'))
    self.window.update()
    self.window.log('Рассылка запущена')
    async with self.client:
      phones = [line.strip() for line in open(self.config.get('sender_contacts_file_path'))]

      # Счётчик отправленных сообщений
      messages_sended = 0

      # Удалить все контакты
      async def delete_all_contacts():
        contacts = await self.client.get_contacts();
        
        ids = list(map(lambda x: x.id, contacts));
        await self.client.delete_contacts(ids);

      # Добавить контакт
      async def get_user_id(phone):
        result = (await self.client.import_contacts([
            InputPhoneContact(phone, phone)
        ]))

        # Если контакт нашёлся
        if len(result.users):
          contact = result.users[0]

          await self.client.delete_contacts(contact.id);
          return contact.id
        else:
          return ''

      for phone in phones:
        id = await get_user_id(phone);

        # Если отправили нужное количество сообщений - выход
        sender_messages_count = self.config.get('sender_messages_count') or len(phones)

        if messages_sended >= int(sender_messages_count):
          self.window.log(f'Отправлено {messages_sended} сообщений')
          break

        # Если нашелся такой аккаунт
        if id:

          # Проверяем отправили ли мы сообщение этому контакту - пропускаем
          if str(id) in self.processed_messages and self.config.get('sender_unqiue'):
            self.window.log(f'Номер {phone} уже был обработан')
            continue

          # Отправляем сообщение в зависимости от типа вложения
          if self.config.get('sender_attachment_type') == 1:
            await self.client.send_photo(
              id,
              self.config.get('sender_attacment_file_path'),
              caption=inspect.cleandoc(self.config.get('sender_message'))
            )
          elif self.config.get('sender_attachment_type') == 2:
            await self.client.send_video(
              id,
              self.config.get('sender_attacment_file_path'),
              caption=inspect.cleandoc(self.config.get('sender_message'))
            )
          else:
            await self.client.send_message(
              id,
              inspect.cleandoc(self.config.get('sender_message'))
            )

          messages_sended += 1
          self.processed_messages[str(id)] = True

          self.window.log(f'Сообщение для {phone} доставлено. Писем отправлено: {messages_sended}')
      

          # Задержка, чтобы не улететь в бан 
          delay = int(self.config.get('sender_delay'))
          self.window.log(f'Задержка { delay } секунд')
          await asyncio.sleep(delay)
        else:
          self.processed_messages[str(id)] = True
          self.window.log(f'Не получилось найти контакт {phone}')
    # except:
    #   self.window.log('Ошибка запуска рассылки')

  def updateAccount(self):
    return self.loop.run_until_complete(self._updateAccount())

  async def _updateAccount(self):
    try:
      self.client = Client('telegram-spammer', self.config.get('api_id'), self.config.get('api_hash'), phone_number=self.config.get('api_phone'))
    except:
      self.window.log('Ошибка подключения к telegram')

    # try:
    self.window.update()
    self.config = json.load(open('config.json'))

    async with self.client:
      # Обновляем имя и описание и аватар
      photo = self.config.get('account_avatar_file')
      first_name = self.config.get('account_firstname')
      last_name = self.config.get('account_lastname')
      bio = self.config.get('account_bio')
  
      print(photo, first_name, last_name, bio)
      if photo:
        await self.client.set_profile_photo(photo=photo)
      
      # if first_name:
      #   await self.client.update_profile(
      #     first_name=first_name
      #   )
      # if last_name:
      #   await self.client.update_profile(
      #     last_name=last_name
      #   )
      # if bio:
      #   await self.client.update_profile(
      #     bio=bio
      #   )

      # if first_name and last_name:
      #   await self.client.update_profile(
      #     first_name=first_name,
      #     last_name=last_name,
      #   )
      # if first_name and bio:
      #   await self.client.update_profile(
      #     first_name=first_name,
      #     bio=bio
      #   )
      # if last_name and bio:
      #   await self.client.update_profile(
      #     last_name=last_name,
      #     bio=bio
      #   )

      # if first_name and last_name and bio:
      await self.client.update_profile(
        first_name=first_name,
        last_name=last_name,
        bio=bio
      )
    # except:
    #   self.window.log('Ошибка изменения данных аккаунта')

  def clearProcessedMessages(self):
    self.processed_messages.clear()
    self.window.log('Список отправленых сообщений очищен')



if __name__ == "__main__":
  Sender()

