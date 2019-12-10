
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def getAddresses():
  """get the admin email addresses from a file"""
  emails = []
  HOME = os.environ["HOME"]
  filename = "%s/.admin_emails" % (HOME)
  try:
    inf = open(filename,"r")
    for line in inf:
      if not line.startswith("#"):
        emails.append(line.strip())
    inf.close()
  except FileNotFoundError:
    print("No .admin_emails file found...")
  return emails

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'really-secret-key'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  ADMINS = getAddresses()
  WORKOUTS_PER_PAGE = 5
