# """Send an email message from the user's account.
# """
# #
# # import base64
# # from apiclient import discovery
# # from email.mime.audio import MIMEAudio
# # from email.mime.base import MIMEBase
# # from email.mime.image import MIMEImage
# # from email.mime.multipart import MIMEMultipart
# # from email.mime.text import MIMEText
# # import mimetypes
# # import os
# #
# # from apiclient import errors
# #
# #
# # def CreateMessage(sender, to, subject, message_text):
# #   """Create a message for an email.
# #
# #   Args:
# #     sender: Email address of the sender.
# #     to: Email address of the receiver.
# #     subject: The subject of the email message.
# #     message_text: The text of the email message.
# #
# #   Returns:
# #     An object containing a base64url encoded email object.
# #   """
# #   message = MIMEText(message_text)
# #   message['to'] = to
# #   message['from'] = sender
# #   message['subject'] = subject
# #   print("Sending Message...")
# #   encoded_message = {'raw': base64.urlsafe_b64encode(bytes(message.as_string(), 'utf-8'))}
# #   return {'raw': encoded_message.decode()}
# #
# #
# # # https://developers.google.com/gmail/api/guides/sending
# # def send_message(service, user_id, message):
# #   """Send an email message.
# #   Args:
# #     service: Authorized Gmail API service instance.
# #     user_id: User's email address. The special value "me"
# #     can be used to indicate the authenticated user.
# #     message: Message to be sent.
# #   Returns:
# #     Sent Message.
# #   """
# #   try:
# #     message = (service.users().messages().send(userId=user_id, body=message)
# #                .execute())
# #     print('Message Id: %s' % message['id'])
# #     return message
# #   #except errors.HttpError, error:
# #   except:
# #     print('An error occurred: %s' % error)
# #
# #
# # raw_msg = CreateMessage('michaelpopedeveloper.bot.1@gmail.com', 'michaelpopedeveloper@gmail.com', "What's up", 'Hello World!')
# # send_message(service, "me", raw_msg)
#
#
import base64
import httplib2

from email.mime.text import MIMEText

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
  credentials = run(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)

# create a message to send
message = MIMEText("Message goes here.")
message['to'] = "michaelpopedeveloper@gmail.com"
message['from'] = "michaelpopedeveloper.bot.1@gmail.com"
message['subject'] = "Random subject"
body = {'raw': base64.b64encode(message.as_string())}

# send it
try:
  message = (gmail_service.users().messages().send(userId="me", body=body).execute())
  print('Message Id: %s' % message['id'])
  print(message)
except Exception as error:
  print('An error occurred: %s' % error)