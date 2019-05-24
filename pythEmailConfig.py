import os
from dotenv import load_dotenv
load_dotenv()

ORG_EMAIL   = '@gmail.com'
FROM_EMAIL  = os.getenv('user_email') + ORG_EMAIL
FROM_PWD    = os.getenv('user_password')
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993