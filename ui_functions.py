import json

## ==> GUI FILE



from PyQt5.QtWidgets import QFileDialog


def saveConfig(config):
  with open("config.json", "w") as jsonfile:
    json.dump(config, jsonfile) # Writing to the file
    jsonfile.close()


class UIFunctions():
    def changePage(self, page, button):
      self.ui.stackedWidget.setCurrentWidget(page)
  

    def saveApiSettings(self):
      data = self.config

      data['api_id'] = self.ui.input_api_id.text()
      data['api_hash'] = self.ui.input_api_hash.text()
      data['api_phone'] = self.ui.input_api_phone.text()

      saveConfig(data)  
    
    def saveSenderSettings(self):
      data = self.config

      data['sender_message'] = self.ui.sender_message.toPlainText()
      data['sender_delay'] = self.ui.sender_delay.text()
      data['sender_attachment_type'] = self.ui.sender_attachment_type.currentIndex()
      data['sender_messages_count'] = self.ui.sender_messages_count.text()
      data['sender_unqiue'] = self.ui.sender_unqiue.isChecked()

      saveConfig(data)
      


    def inputFile(self, key, label):
      path = (QFileDialog.getOpenFileName())[0]

      label.setText(path.split('/')[-1])

      # Save in config
      data = self.config

      data[key] = path

      saveConfig(data)

    def saveAccountSettings(self):
      data = self.config

      data['account_firstname'] = self.ui.account_firstname.text()
      data['account_lastname'] = self.ui.account_lastname.text()
      data['account_bio'] = self.ui.account_bio.toPlainText()

      saveConfig(data)
    
    def startSender(self):
      self.start()

    def refreshApiStatus(self):
      self.update()

    def clearProcessedMessages(self):
      self.clearProcessedMessages()

