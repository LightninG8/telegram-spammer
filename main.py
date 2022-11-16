from pyrogram import Client # телеграм клиент
import shelve # запись информации в файл
import json
import asyncio
from pyrogram.types import InputPhoneContact
import inspect
import time
import threading

from window import *

class Sender():
  def __init__(self):
    self.config = json.load(open('config.json'))

    self.client = Client('telegram-spamer', self.config.get('api_id'), self.config.get('api_hash'), phone_number=self.config.get('api_phone'))

    self.loop = asyncio.get_event_loop()

    self.app = QApplication(sys.argv)
    self.window = MainWindow(
      self.config,
      self.updateSender,
      self.updateAccount,
      self.start
    )

    sys.exit(self.app.exec_())


  def updateSender(self): 
    self.window.update()
    self.client = Client('telegram-spamer', self.config.get('api_id'), self.config.get('api_hash'), phone_number=self.config.get('phone_number'))


  def start(self):
    thread = threading.Thread(target=self.loop.run_until_complete, args=(self._start(), ))
    thread.start()

  async def _start(self):
    async with self.client:
      self.window.log('Рассылка запущена')

      processed_messages = shelve.open('processed_messages.db', writeback=True)

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
        if messages_sended >= int(self.config.get('sender_messages_count')):
          self.window.log(f'Отправлено {messages_sended} сообщений')
          break

        # Если нашелся такой аккаунт
        if id:

          # Проверяем отправили ли мы сообщение этому контакту - пропускаем
          if str(id) in processed_messages and self.config.get('sender_unqiue'):
            self.window.log(f'Сообщение для {phone} уже было доставлено')
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
          processed_messages[str(id)] = True

          self.window.log(f'Сообщение для {phone} доставлено. Писем отправлено: {messages_sended}')
      

          # Задержка, чтобы не улететь в бан 
          delay = int(self.config.get('sender_delay'))
          self.window.log(f'Задержка { delay } секунд')
          await asyncio.sleep(delay)
        else:
          processed_messages[str(id)] = True
          self.window.log(f'Не получилось найти контакт {phone}')

  def updateAccount(self):
    return self.loop.run_until_complete(self._updateAccount())

  async def _updateAccount(self):
    async with self.client:
      # Обновляем имя и описание и аватар
      photo = await self.client.set_profile_photo(photo=self.config.get('account_avatar_file'))
      profile = await self.client.update_profile(
        first_name=self.config.get('account_firstname'),
        last_name=self.config.get('account_lastname'),
        bio=self.config.get('account_bio')
      )


if __name__ == "__main__":
  Sender()

