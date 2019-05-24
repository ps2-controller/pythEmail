import smtplib
import time
import imaplib
import email
import pythEmailConfig as pythEmailConfig
import re

SMTP_SERVER = pythEmailConfig.SMTP_SERVER
FROM_EMAIL = pythEmailConfig.FROM_EMAIL
FROM_PWD = pythEmailConfig.FROM_PWD

from_bodies = b''
to_bodies = b''

def get_body_before_gmail_reply_date(msg):
  body_before_gmail_reply = msg
  # regex for date format like "On Thu, Mar 24, 2011 at 3:51 PM"
  matching_string_obj = re.search(r"\w+\s+\w+[,][]\s+\w+\s+\d+[,]\s+\d+\s+\w+\s+\d+[:]\d+\s+\w+.*", msg.decode("utf-8"))
  wrote_identifier = re.search("wrote:", msg.decode("utf-8"))
  forwarded_identifier = re.search("-Forwarded", msg.decode("utf-8"))
  if matching_string_obj:
    # split on that match, group() returns full matched string
    body_before_gmail_reply_list = msg.decode("utf-8").split(matching_string_obj.group())
    print(body_before_gmail_reply_list)
    # string before the regex match, so the body of the email
    body_before_gmail_reply = str.encode(body_before_gmail_reply_list[0])
  if wrote_identifier:
    body_before_gmail_reply_list = msg.decode("utf-8").split("wrote:")
    print(body_before_gmail_reply_list)
    body_before_gmail_reply = str.encode(body_before_gmail_reply_list[0])
  return body_before_gmail_reply

def build_from_bodies():
  global from_bodies
  try:
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login("anurag.angara@gmail.com","pessimist")
    print('hi')
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    j = 0

    for i in reversed(id_list):
      j += 1
      if j > 2:
        break
      # print(j)
      typ, data = mail.fetch(i, '(RFC822)' )

      for response_part in data:
        if isinstance(response_part, tuple):
          msg_body = b''
          msg = email.message_from_string(response_part[1].decode('utf-8'))
          if msg.is_multipart():
              for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                  msg_body = part.get_payload(decode=True)
                  break
          else: 
            msg_body = msg.get_payload(decode=True)
          email_subject = msg['subject']
          email_from = msg['from']
          # # from_address = email_from.split("<")[1].split(">")[0]
          # if from_address == FROM_EMAIL:
          #   from_bodies += msg_body
          #   print(from_bodies)
          # else:
          from_bodies += msg_body
          # print('From : ' + email_from + '\n')
          # print('Subject : ' + email_subject + '\n')

  except Exception as e:
    print(str(e))

def build_to_bodies():
  global to_bodies
  try:
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login("anurag.angara@gmail.com","pessimist")
    print('hi')
    mail.select('"[Gmail]/Sent Mail"')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    j = 0

    for i in reversed(id_list):
      j += 1
      if j > 15:
        break
      # print(j)
      typ, data = mail.fetch(i, '(RFC822)' )

      for response_part in data:
        if isinstance(response_part, tuple):
          msg_body = b''
          msg = email.message_from_string(response_part[1].decode('utf-8'))
          if msg.is_multipart():
              for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                  msg_body = part.get_payload(decode=True)
                  break
          else: 
            msg_body = msg.get_payload(decode=True)
          email_subject = msg['subject']
          email_from = msg['from']
          just_msg_body = get_body_before_gmail_reply_date(msg_body)
          # # from_address = email_from.split("<")[1].split(">")[0]
          # if from_address == FROM_EMAIL:
          #   from_bodies += msg_body
          #   print(from_bodies)
          # else:
          to_bodies += just_msg_body
          # print('From : ' + email_from + '\n')
          # print('Subject : ' + email_subject + '\n')

  except Exception as e:
    print(str(e))

def count_sent_just(from_bodies):
  search_word = "Would"
  from_bodies_str = from_bodies.decode('utf-8')
  N = len(search_word)
  M = len(from_bodies_str)
  res = 0
  for i in range(N - M + 1): 
    j = 0
    for j in range(M): 
      if (from_bodies_str[i + j] != search_word[j]): 
        break
    if (j == M - 1): 
      res += 1
      j = 0
  print(res)
  return res 

build_from_bodies()
build_to_bodies()
count_sent_just(from_bodies)
# print(to_bodies)