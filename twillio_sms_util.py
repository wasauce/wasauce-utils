#!/usr/bin/python2.5
import logging

# This util assumes that you have previously installed Twilio's python library
## The twilio library can be found here: http://www.twilio.com/docs/libraries/ 
import twilio

## I commonly employ a common settings file for my projects. It would contain
## these settings which I would import. If imported, one must comment out /
## delete the one off settings below

#from settings import STATUS_CALLBACK, TWILLIO_SID, TWILLIO_TOKEN

### One Off Settings
STATUS_CALLBACK = 1 #Replace with real value
TWILLIO_SID =  '' #Replace with real value
TWILLIO_TOKEN = '' #Replace with real value


class SmsService():
  """This class provides a means of sending SMS messages via Twillio.

     
  """  

  #Twillio credentials
  SID = TWILLIO_SID
  TOKEN = TWILLIO_TOKEN
  
  def __init__(self):
    self.account = twilio.Account(self.SID, self.TOKEN)
 
  def send_message(self, message):
    """Function that sends the message via twillio after length checking.
    """

    logging.info('Calling send_message')
    if message and type(message) is not dict:
      logging.warning('message is not a dictionary: %s' % message)
      return
    
    body = message.get('Body', '')

    #Logic to determine if the message needs to be broken into multiple SMS
    if len(body) >= 160:
      while len(body) > 0:
        if len(body) >= 160:
          send_body = body[:157] + '...'
        else:
          send_body = body
        message['Body'] = send_body

        #Call twillio to send the message
        self.account.request('/%s/Accounts/%s/SMS/Messages' % ('2010-04-01',
                             self.SID), 'POST', message)

        #Now repeat the process with the leftover characters from the message.
        body = body[157:]

    else:
      #Call twillio to send the message
      self.account.request('/%s/Accounts/%s/SMS/Messages' % ('2010-04-01',
                           self.SID), 'POST', message)

  def send_simple_message(self, from_number, to_number, message):
    """Function to send a message to Twillio.

       This is the primary function for sending a SMS via twillio. The function
       abstracts away the complexity of sending the message and checks the
       length, breaking up the message into multiple SMSes as needed.
    """
    logging.info('Sending message via send_simple_message')
    message = {
            'From': from_number,
            'To': to_number,
            'Body': message,
            # StatusCallback can be commented out if desired.
            'StatusCallback': STATUS_CALLBACK,      
            }
    logging.info('send_simple_message now calling send_message')
    self.send_message(message)
